import asyncio
import re
import logging
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from winrt.windows.devices.bluetooth import BluetoothLEDevice
from winrt.windows.devices.bluetooth.genericattributeprofile import GattCommunicationStatus
from winrt.windows.devices.enumeration import DeviceInformation
from winrt.windows.storage.streams import DataReader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BATTERY_SERVICE_UUID = '0000180f-0000-1000-8000-00805f9b34fb'
BATTERY_LEVEL_UUID = '00002a19-0000-1000-8000-00805f9b34fb'

MOUSE_BRANDS_KEYWORDS = {
    "xiaomi": ["dmms", "mi ", "xiaomi"],
    "logitech": ["logitech", "mx master", "g pro", "m720", "m590"],
    "razer": ["razer", "deathadder", "viper", "basilisk"],
    "corsair": ["corsair", "dark core", "m65", "ironclaw"],
    "steelseries": ["steelseries", "rival", "sensei", "prime"],
    "fun60": ["fun60"],
    "monsgeek": ["monsgeek", "mons"],
    "royuan": ["royuan"],
}

KEYBOARD_BRANDS_KEYWORDS = {
    "fun60": ["fun60"],
    "monsgeek": ["monsgeek", "mons"],
    "royuan": ["royuan"],
    "logitech": ["logitech", "mx keys", "g pro x", "k380"],
    "razer": ["razer", "blackwidow", "huntsman", "ornata"],
    "corsair": ["corsair", "k70", "k100", "k55"],
}

class BluetoothWorker(QThread):
    battery_found = pyqtSignal(str, float, bool, str, str)

    def __init__(self, mouse_brand="xiaomi", keyboard_brand="fun60"):
        super().__init__()
        self.running = True
        self.seen_addresses = set()
        self.mouse_brand = mouse_brand
        self.keyboard_brand = keyboard_brand

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.scan_loop())

    async def scan_loop(self):
        while self.running:
            try:
                await self.scan_devices()
            except Exception as e:
                logger.error(f"Scan error: {e}")
            await asyncio.sleep(5)

    async def scan_devices(self):
        try:
            devices = await DeviceInformation.find_all_async()
            self.seen_addresses.clear()

            for device in devices:
                if not device.name:
                    continue

                if not self.is_ble_device(device.id):
                    continue

                name_lower = device.name.lower()
                device_type = None
                device_name = None

                # Check mouse brands
                mouse_keywords = MOUSE_BRANDS_KEYWORDS.get(self.mouse_brand, [])
                for kw in mouse_keywords:
                    if kw in name_lower:
                        device_type = "mouse"
                        device_name = device.name
                        break

                # Check keyboard brands
                if not device_type:
                    keyboard_keywords = KEYBOARD_BRANDS_KEYWORDS.get(self.keyboard_brand, [])
                    for kw in keyboard_keywords:
                        if kw in name_lower:
                            device_type = "keyboard"
                            device_name = device.name
                            break

                if device_type:
                    addr_hex = self.extract_ble_address(device.id)
                    if addr_hex and addr_hex not in self.seen_addresses:
                        self.seen_addresses.add(addr_hex)
                        logger.info(f"Scanning {device_name} ({addr_hex})")
                        await self.read_battery(device_name, addr_hex, device_type)
        except Exception as e:
            logger.error(f"Device scan error: {e}")

    def is_ble_device(self, device_id):
        id_lower = device_id.lower()
        return 'bthle' in id_lower or 'bluetoothle' in id_lower

    def extract_ble_address(self, device_id):
        # Format 1: BTHLE\Dev_XXXXXXXXXXXX\...
        match = re.search(r'Dev_([0-9a-fA-F]{12})', device_id)
        if match:
            return match.group(1).lower()

        # Format 2: BluetoothLE#BluetoothLE<MAC>-<MAC>
        match = re.search(r'bluetoothle#bluetoothle(.+?)-', device_id.lower())
        if match:
            mac_str = match.group(1).replace(':', '').replace('-', '')
            if len(mac_str) == 12:
                return mac_str

        # Format 3: BTHLEDevice#{GUID}_Dev_VID&XXXX_PID&XXXX_..._XXXXXXXXXXXX
        match = re.search(r'_([0-9a-fA-F]{12})#', device_id)
        if match:
            return match.group(1).lower()

        return None

    async def read_battery(self, name, addr_hex, device_type):
        try:
            addr_int = int(addr_hex, 16)
            bt_device = await BluetoothLEDevice.from_bluetooth_address_async(addr_int)
            if not bt_device:
                logger.warning(f"Cannot connect to {name}")
                return

            services_result = await bt_device.get_gatt_services_async()
            if services_result.status == GattCommunicationStatus.SUCCESS:
                for service in services_result.services:
                    if str(service.uuid) == BATTERY_SERVICE_UUID:
                        chars = await service.get_characteristics_async()
                        for char in chars.characteristics:
                            if str(char.uuid) == BATTERY_LEVEL_UUID:
                                read_result = await char.read_value_async()
                                if read_result.status == GattCommunicationStatus.SUCCESS:
                                    reader = DataReader.from_buffer(read_result.value)
                                    battery = reader.read_byte()
                                    logger.info(f"{name}: {battery}%")
                                    self.battery_found.emit(name, battery / 100.0, True, device_type, name)
                                    return
            else:
                logger.warning(f"GATT services unavailable for {name}")
        except Exception as e:
            logger.error(f"Read battery error for {name}: {e}")

class BluetoothMonitor(QObject):
    battery_updated = pyqtSignal(str, float, bool, str)

    def __init__(self, mouse_brand="xiaomi", keyboard_brand="fun60"):
        super().__init__()
        self.worker = BluetoothWorker(mouse_brand, keyboard_brand)
        self.worker.battery_found.connect(self.on_battery_found)
        self.worker.start()

    def stop(self):
        self.worker.running = False
        self.worker.wait(1000)

    def on_battery_found(self, name, level, connected, device_type, real_name):
        if device_type == "mouse":
            self.battery_updated.emit("Mouse", level, connected, real_name)
        elif device_type == "keyboard":
            self.battery_updated.emit("Keyboard", level, connected, real_name)
