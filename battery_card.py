from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from liquid_bar import LiquidBar

class BatteryCard(QWidget):
    def __init__(self, device_name, theme=None, parent=None):
        super().__init__(parent)
        self.device_name = device_name
        self.theme = theme

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        # Device icon and name
        info_layout = QVBoxLayout()

        self.name_label = QLabel(device_name)
        self.name_label.setFont(QFont("SF Pro Display", 11))

        self.percent_label = QLabel("--")
        self.percent_label.setFont(QFont("SF Pro Display", 24, QFont.Weight.Bold))

        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.percent_label)
        info_layout.addStretch()

        # Liquid bar
        self.liquid_bar = LiquidBar(theme)
        self.liquid_bar.setFixedSize(50, 100)

        layout.addLayout(info_layout)
        layout.addWidget(self.liquid_bar)

        self.apply_theme()

    def apply_theme(self):
        if self.theme:
            color = self.theme['text']
            style = f"color: rgb({color.red()}, {color.green()}, {color.blue()});"
            self.name_label.setStyleSheet(style)
            self.percent_label.setStyleSheet(style)

    def update_name(self, name):
        self.device_name = name
        self.name_label.setText(name)

    def set_battery(self, level, connected=True):
        self.liquid_bar.set_level(level)
        self.percent_label.setText(f"{int(level * 100)}%")

        if not connected:
            self.percent_label.setStyleSheet("color: gray;")

    def update_theme(self, theme):
        self.theme = theme
        self.liquid_bar.update_theme(theme)
        self.apply_theme()
