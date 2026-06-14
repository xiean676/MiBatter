from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenu,
                              QLabel, QColorDialog, QFontDialog, QDialog, QDialogButtonBox,
                              QComboBox, QSpinBox, QLineEdit, QListWidget, QListWidgetItem,
                              QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt, QPoint, QSettings
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QMouseEvent, QLinearGradient, QFont
from battery_card import BatteryCard
from bluetooth_monitor import BluetoothMonitor

THEMES = {
    "dark_glass": {
        "name": "Dark Glass",
        "name_zh": "深色玻璃",
        "bg_colors": [QColor(30, 30, 30, 180), QColor(20, 20, 20, 200)],
        "border": QColor(255, 255, 255, 30),
        "text": QColor(255, 255, 255),
        "accent": QColor(100, 200, 255),
        "menu_bg": "rgba(30, 30, 30, 230)",
    },
    "light_glass": {
        "name": "Light Glass",
        "name_zh": "浅色玻璃",
        "bg_colors": [QColor(245, 245, 250, 220), QColor(230, 235, 245, 240)],
        "border": QColor(200, 200, 220, 150),
        "text": QColor(40, 40, 50),
        "accent": QColor(80, 120, 200),
        "menu_bg": "rgba(245, 245, 250, 240)",
    },
    "blue_neon": {
        "name": "Blue Neon",
        "name_zh": "蓝色霓虹",
        "bg_colors": [QColor(10, 15, 40, 220), QColor(5, 10, 30, 240)],
        "border": QColor(0, 150, 255, 80),
        "text": QColor(180, 220, 255),
        "accent": QColor(0, 180, 255),
        "menu_bg": "rgba(10, 15, 40, 240)",
    },
    "purple_glow": {
        "name": "Purple Glow",
        "name_zh": "紫色光晕",
        "bg_colors": [QColor(30, 10, 50, 220), QColor(20, 5, 40, 240)],
        "border": QColor(180, 100, 255, 80),
        "text": QColor(220, 180, 255),
        "accent": QColor(180, 100, 255),
        "menu_bg": "rgba(30, 10, 50, 240)",
    },
    "green_fresh": {
        "name": "Green Fresh",
        "name_zh": "绿色清新",
        "bg_colors": [QColor(10, 30, 20, 220), QColor(5, 25, 15, 240)],
        "border": QColor(100, 255, 150, 80),
        "text": QColor(180, 255, 200),
        "accent": QColor(100, 255, 150),
        "menu_bg": "rgba(10, 30, 20, 240)",
    },
    "sunset_orange": {
        "name": "Sunset Orange",
        "name_zh": "日落橙",
        "bg_colors": [QColor(40, 15, 10, 220), QColor(30, 10, 5, 240)],
        "border": QColor(255, 150, 80, 80),
        "text": QColor(255, 200, 160),
        "accent": QColor(255, 150, 80),
        "menu_bg": "rgba(40, 15, 10, 240)",
    },
}

MOUSE_BRANDS = {
    "xiaomi": {"en": "Xiaomi", "zh": "小米", "models": ["Mi DMMS2", "Mi Wireless Mouse"]},
    "logitech": {"en": "Logitech", "zh": "罗技", "models": ["MX Master", "G Pro", "M720"]},
    "razer": {"en": "Razer", "zh": "雷蛇", "models": ["DeathAdder", "Viper", "Basilisk"]},
    "corsair": {"en": "Corsair", "zh": "海盗船", "models": ["Dark Core", "M65", "Ironclaw"]},
    "steelseries": {"en": "SteelSeries", "zh": "赛睿", "models": ["Rival", "Sensei", "Prime"]},
    "other": {"en": "Other", "zh": "其他", "models": []},
}

KEYBOARD_BRANDS = {
    "fun60": {"en": "FUN60", "zh": "FUN60", "models": ["FUN60 BT"]},
    "monsgeek": {"en": "MonsGeek", "zh": " MonsGeek", "models": ["MonsGeek Keyboard"]},
    "royuan": {"en": "ROYUAN", "zh": "ROYUAN", "models": ["ROYUAN Keyboard"]},
    "logitech": {"en": "Logitech", "zh": "罗技", "models": ["MX Keys", "G Pro X", "K380"]},
    "razer": {"en": "Razer", "zh": "雷蛇", "models": ["BlackWidow", "Huntsman"]},
    "corsair": {"en": "Corsair", "zh": "海盗船", "models": ["K70", "K100"]},
    "other": {"en": "Other", "zh": "其他", "models": []},
}

LANG = {
    "en": {
        "settings": "Settings",
        "theme": "Theme",
        "mouse_settings": "Mouse Settings",
        "keyboard_settings": "Keyboard Settings",
        "language": "Language",
        "quit": "Quit",
        "custom_theme": "Custom Theme",
        "customize": "Customize",
        "new_theme": "New Theme",
        "delete_theme": "Delete Theme",
        "theme_name": "Theme Name",
        "text_color": "Text Color",
        "accent_color": "Accent Color",
        "bg_color": "Background Color",
        "border_color": "Border Color",
        "font_size": "Font Size",
        "apply": "Apply",
        "cancel": "Cancel",
        "save": "Save",
        "delete_confirm": "Delete this theme?",
        "english": "English",
        "chinese": "简体中文",
        "custom_themes": "Custom Themes",
    },
    "zh": {
        "settings": "设置",
        "theme": "主题",
        "mouse_settings": "鼠标设置",
        "keyboard_settings": "键盘设置",
        "language": "语言",
        "quit": "退出",
        "custom_theme": "自定义主题",
        "customize": "自定义",
        "new_theme": "新建主题",
        "delete_theme": "删除主题",
        "theme_name": "主题名称",
        "text_color": "文字颜色",
        "accent_color": "强调色",
        "bg_color": "背景颜色",
        "border_color": "边框颜色",
        "font_size": "字体大小",
        "apply": "应用",
        "cancel": "取消",
        "save": "保存",
        "delete_confirm": "确定删除此主题？",
        "english": "English",
        "chinese": "简体中文",
        "custom_themes": "自定义主题",
    },
}


class ColorButton(QPushButton):
    def __init__(self, color=QColor(255, 255, 255), parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(60, 30)
        self.update_style()

    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({self.color.red()}, {self.color.green()}, {self.color.blue()}, {self.color.alpha()});
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
            }}
            QPushButton:hover {{
                border: 1px solid white;
            }}
        """)

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color
        self.update_style()


class CustomThemeDialog(QDialog):
    def __init__(self, parent=None, theme_name="", theme_data=None, lang="en"):
        super().__init__(parent)
        self.lang = lang
        self.t = lambda k: LANG[lang].get(k, k)

        self.setWindowTitle(self.t("customize"))
        self.setFixedSize(350, 450)

        self.theme_data = theme_data or THEMES["dark_glass"]

        layout = QVBoxLayout(self)

        # Theme name
        name_label = QLabel(self.t("theme_name"))
        name_label.setFont(QFont("SF Pro Display", 10))
        self.name_input = QLineEdit(theme_name)
        self.name_input.setPlaceholderText("My Theme")
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        # Background color
        bg_label = QLabel(self.t("bg_color"))
        bg_label.setFont(QFont("SF Pro Display", 10))
        self.bg_color_btn = ColorButton(self.theme_data['bg_colors'][0])
        self.bg_color_btn.clicked.connect(lambda: self.pick_color(self.bg_color_btn))
        layout.addWidget(bg_label)
        layout.addWidget(self.bg_color_btn)

        # Text color
        text_label = QLabel(self.t("text_color"))
        text_label.setFont(QFont("SF Pro Display", 10))
        self.text_color_btn = ColorButton(self.theme_data['text'])
        self.text_color_btn.clicked.connect(lambda: self.pick_color(self.text_color_btn))
        layout.addWidget(text_label)
        layout.addWidget(self.text_color_btn)

        # Accent color
        accent_label = QLabel(self.t("accent_color"))
        accent_label.setFont(QFont("SF Pro Display", 10))
        self.accent_color_btn = ColorButton(self.theme_data['accent'])
        self.accent_color_btn.clicked.connect(lambda: self.pick_color(self.accent_color_btn))
        layout.addWidget(accent_label)
        layout.addWidget(self.accent_color_btn)

        # Border color
        border_label = QLabel(self.t("border_color"))
        border_label.setFont(QFont("SF Pro Display", 10))
        self.border_color_btn = ColorButton(self.theme_data['border'])
        self.border_color_btn.clicked.connect(lambda: self.pick_color(self.border_color_btn))
        layout.addWidget(border_label)
        layout.addWidget(self.border_color_btn)

        # Font size
        font_label = QLabel(self.t("font_size"))
        font_label.setFont(QFont("SF Pro Display", 10))
        self.font_spin = QSpinBox()
        self.font_spin.setRange(10, 24)
        self.font_spin.setValue(self.theme_data.get("font_size", 12))
        layout.addWidget(font_label)
        layout.addWidget(self.font_spin)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def pick_color(self, btn):
        color = QColorDialog.getColor(btn.get_color(), self, self.t("text_color"))
        if color.isValid():
            btn.set_color(color)

    def get_result(self):
        name = self.name_input.text().strip() or "My Theme"
        bg = self.bg_color_btn.get_color()
        return name, {
            "name": name,
            "name_zh": name,
            "bg_colors": [bg, QColor(bg.red() - 10, bg.green() - 10, bg.blue() - 10, bg.alpha() + 20)],
            "border": self.border_color_btn.get_color(),
            "text": self.text_color_btn.get_color(),
            "accent": self.accent_color_btn.get_color(),
            "menu_bg": f"rgba({bg.red()}, {bg.green()}, {bg.blue()}, 230)",
            "font_size": self.font_spin.value(),
        }


class BatteryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(320, 240)
        self.move(100, 100)

        self.drag_position = QPoint()
        self.settings = QSettings("BatteryWidget", "Config")
        self.current_theme = self.settings.value("theme", "dark_glass")
        self.current_lang = self.settings.value("lang", "en")
        self.mouse_brand = self.settings.value("mouse_brand", "xiaomi")
        self.keyboard_brand = self.settings.value("keyboard_brand", "fun60")
        self.mouse_real_name = ""
        self.keyboard_real_name = ""
        self.custom_themes = self.load_custom_themes()

        self.setup_ui()

    def load_custom_themes(self):
        saved = self.settings.value("custom_themes", {})
        result = {}
        for name, data in saved.items():
            result[name] = {
                "name": name,
                "name_zh": name,
                "bg_colors": [QColor(data.get("bg", "#1e1e1e")), QColor(data.get("bg2", "#141414"))],
                "border": QColor(data.get("border", "#ffffff")),
                "text": QColor(data.get("text", "#ffffff")),
                "accent": QColor(data.get("accent", "#64c8ff")),
                "menu_bg": data.get("menu_bg", "rgba(30, 30, 30, 230)"),
                "font_size": data.get("font_size", 12),
            }
        return result

    def save_custom_themes(self):
        data = {}
        for name, theme in self.custom_themes.items():
            data[name] = {
                "bg": theme['bg_colors'][0].name(),
                "bg2": theme['bg_colors'][1].name(),
                "border": theme['border'].name(),
                "text": theme['text'].name(),
                "accent": theme['accent'].name(),
                "menu_bg": theme['menu_bg'],
                "font_size": theme.get('font_size', 12),
            }
        self.settings.setValue("custom_themes", data)

    def get_active_theme(self):
        if self.current_theme in self.custom_themes:
            return self.custom_themes[self.current_theme]
        return THEMES.get(self.current_theme, THEMES["dark_glass"])

    def t(self, key):
        return LANG[self.current_lang].get(key, key)

    def get_device_display_name(self, device_type):
        if device_type == "mouse":
            brand_info = MOUSE_BRANDS.get(self.mouse_brand, MOUSE_BRANDS["other"])
            lang = self.current_lang
            if self.mouse_brand == "other" and self.mouse_real_name:
                return self.mouse_real_name
            return f"{brand_info[lang]} {brand_info['models'][0]}" if brand_info['models'] else brand_info[lang]
        else:
            brand_info = KEYBOARD_BRANDS.get(self.keyboard_brand, KEYBOARD_BRANDS["other"])
            lang = self.current_lang
            if self.keyboard_brand == "other" and self.keyboard_real_name:
                return self.keyboard_real_name
            return f"{brand_info[lang]} {brand_info['models'][0]}" if brand_info['models'] else brand_info[lang]

    def setup_ui(self):
        theme = self.get_active_theme()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(5)

        header_layout = QHBoxLayout()
        header_layout.addStretch()

        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setFixedSize(28, 28)
        self.settings_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: rgba({theme['text'].red()}, {theme['text'].green()}, {theme['text'].blue()}, 0.7);
                font-size: 18px;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background: rgba({theme['accent'].red()}, {theme['accent'].green()}, {theme['accent'].blue()}, 0.3);
                color: white;
            }}
        """)
        self.settings_btn.clicked.connect(self.show_settings_menu)
        header_layout.addWidget(self.settings_btn)

        main_layout.addLayout(header_layout)

        mouse_name = self.get_device_display_name("mouse")
        keyboard_name = self.get_device_display_name("keyboard")

        self.mouse_card = BatteryCard(mouse_name, theme)
        self.keyboard_card = BatteryCard(keyboard_name, theme)

        main_layout.addWidget(self.mouse_card)
        main_layout.addWidget(self.keyboard_card)

        self.monitor = BluetoothMonitor(
            mouse_brand=self.mouse_brand,
            keyboard_brand=self.keyboard_brand
        )
        self.monitor.battery_updated.connect(self.update_battery)

    def update_battery(self, name, level, connected, real_name=""):
        if name == "Mouse":
            self.mouse_card.set_battery(level, connected)
            if self.mouse_brand == "other" and real_name:
                self.mouse_real_name = real_name
                self.mouse_card.update_name(real_name)
        elif name == "Keyboard":
            self.keyboard_card.set_battery(level, connected)
            if self.keyboard_brand == "other" and real_name:
                self.keyboard_real_name = real_name
                self.keyboard_card.update_name(real_name)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        theme = self.get_active_theme()
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, theme['bg_colors'][0])
        gradient.setColorAt(1, theme['bg_colors'][1])
        painter.fillPath(path, gradient)

        painter.setPen(theme['border'])
        painter.drawPath(path)

        painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            btn_rect = self.settings_btn.geometry()
            if btn_rect.contains(event.position().toPoint()):
                return
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def show_settings_menu(self):
        theme = self.get_active_theme()
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background: {theme['menu_bg']};
                border: 1px solid rgba({theme['border'].red()}, {theme['border'].green()}, {theme['border'].blue()}, 0.3);
                border-radius: 10px;
                padding: 5px;
            }}
            QMenu::item {{
                color: rgb({theme['text'].red()}, {theme['text'].green()}, {theme['text'].blue()});
                padding: 8px 20px;
                border-radius: 5px;
            }}
            QMenu::item:selected {{
                background: rgba({theme['accent'].red()}, {theme['accent'].green()}, {theme['accent'].blue()}, 0.3);
            }}
            QMenu::separator {{
                height: 1px;
                background: rgba({theme['border'].red()}, {theme['border'].green()}, {theme['border'].blue()}, 0.3);
                margin: 5px 10px;
            }}
        """)

        # Theme submenu
        theme_menu = menu.addMenu(self.t("theme"))

        # Built-in themes
        for key, t in THEMES.items():
            theme_name = t["name_zh"] if self.current_lang == "zh" else t["name"]
            action = theme_menu.addAction(theme_name)
            action.setData(("theme", key))
            if key == self.current_theme:
                action.setCheckable(True)
                action.setChecked(True)

        # Custom themes
        if self.custom_themes:
            theme_menu.addSeparator()
            for name in self.custom_themes:
                action = theme_menu.addAction(name)
                action.setData(("theme", name))
                if name == self.current_theme:
                    action.setCheckable(True)
                    action.setChecked(True)

        theme_menu.addSeparator()

        # New theme
        new_action = theme_menu.addAction(self.t("new_theme"))
        new_action.setData(("new_theme", True))

        # Delete theme (only if custom theme is selected)
        if self.current_theme in self.custom_themes:
            delete_action = theme_menu.addAction(self.t("delete_theme"))
            delete_action.setData(("delete_theme", self.current_theme))

        # Language submenu
        lang_menu = menu.addMenu(self.t("language"))
        en_action = lang_menu.addAction("English")
        en_action.setData(("lang", "en"))
        zh_action = lang_menu.addAction("简体中文")
        zh_action.setData(("lang", "zh"))
        if self.current_lang == "en":
            en_action.setCheckable(True)
            en_action.setChecked(True)
        else:
            zh_action.setCheckable(True)
            zh_action.setChecked(True)

        menu.addSeparator()

        # Mouse brand submenu
        mouse_menu = menu.addMenu(self.t("mouse_settings"))
        for key, info in MOUSE_BRANDS.items():
            action = mouse_menu.addAction(info[self.current_lang])
            action.setData(("mouse", key))
            if key == self.mouse_brand:
                action.setCheckable(True)
                action.setChecked(True)

        # Keyboard brand submenu
        keyboard_menu = menu.addMenu(self.t("keyboard_settings"))
        for key, info in KEYBOARD_BRANDS.items():
            action = keyboard_menu.addAction(info[self.current_lang])
            action.setData(("keyboard", key))
            if key == self.keyboard_brand:
                action.setCheckable(True)
                action.setChecked(True)

        menu.addSeparator()
        quit_action = menu.addAction(self.t("quit"))

        action = menu.exec(self.settings_btn.mapToGlobal(self.settings_btn.rect().bottomLeft()))

        if action and action.data():
            data = action.data()
            if isinstance(data, tuple) and len(data) == 2:
                action_type, value = data
                if action_type == "theme":
                    self.change_theme(value)
                elif action_type == "lang":
                    self.change_lang(value)
                elif action_type == "mouse":
                    self.mouse_brand = value
                    self.settings.setValue("mouse_brand", value)
                    self.restart_monitor()
                elif action_type == "keyboard":
                    self.keyboard_brand = value
                    self.settings.setValue("keyboard_brand", value)
                    self.restart_monitor()
                elif action_type == "new_theme":
                    self.new_custom_theme()
                elif action_type == "delete_theme":
                    self.delete_custom_theme(value)
        elif action == quit_action:
            from PyQt6.QtWidgets import QApplication
            QApplication.quit()

    def new_custom_theme(self):
        dialog = CustomThemeDialog(self, lang=self.current_lang)
        if dialog.exec():
            name, theme_data = dialog.get_result()
            self.custom_themes[name] = theme_data
            self.save_custom_themes()
            self.current_theme = name
            self.settings.setValue("theme", name)
            self.apply_theme()

    def delete_custom_theme(self, name):
        reply = QMessageBox.question(
            self,
            self.t("delete_theme"),
            self.t("delete_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if name in self.custom_themes:
                del self.custom_themes[name]
                self.save_custom_themes()
                if self.current_theme == name:
                    self.current_theme = "dark_glass"
                    self.settings.setValue("theme", "dark_glass")
                    self.apply_theme()

    def apply_theme(self):
        theme = self.get_active_theme()

        self.settings_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: rgba({theme['text'].red()}, {theme['text'].green()}, {theme['text'].blue()}, 0.7);
                font-size: 18px;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background: rgba({theme['accent'].red()}, {theme['accent'].green()}, {theme['accent'].blue()}, 0.3);
                color: white;
            }}
        """)

        self.mouse_card.update_theme(theme)
        self.keyboard_card.update_theme(theme)
        self.update()

    def change_lang(self, lang):
        self.current_lang = lang
        self.settings.setValue("lang", lang)
        self.mouse_card.update_name(self.get_device_display_name("mouse"))
        self.keyboard_card.update_name(self.get_device_display_name("keyboard"))

    def change_theme(self, theme_key):
        self.current_theme = theme_key
        self.settings.setValue("theme", self.current_theme)
        self.apply_theme()

    def restart_monitor(self):
        self.monitor.stop()
        self.monitor = BluetoothMonitor(
            mouse_brand=self.mouse_brand,
            keyboard_brand=self.keyboard_brand
        )
        self.monitor.battery_updated.connect(self.update_battery)
        self.mouse_card.update_name(self.get_device_display_name("mouse"))
        self.keyboard_card.update_name(self.get_device_display_name("keyboard"))
