import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from widget import BatteryWidget

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    widget = BatteryWidget()
    widget.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
