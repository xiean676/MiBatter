from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QPainterPath
import math

class LiquidBar(QWidget):
    def __init__(self, theme=None, parent=None):
        super().__init__(parent)
        self.level = 0.5
        self.wave_offset = 0.0
        self.theme = theme

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)

    def update_theme(self, theme):
        self.theme = theme
        self.update()

    def set_level(self, level):
        self.level = max(0.0, min(1.0, level))
        self.update()

    def animate(self):
        self.wave_offset += 0.1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()

        # Calculate water level
        water_y = h * (1.0 - self.level)

        # Create wave path
        path = QPainterPath()
        path.moveTo(0, h)

        # Draw wave
        for x in range(0, w + 1):
            wave_height = 4 * math.sin((x / 20) + self.wave_offset)
            y = water_y + wave_height
            path.lineTo(x, y)

        path.lineTo(w, h)
        path.closeSubpath()

        # Gradient for liquid
        gradient = QLinearGradient(0, water_y, 0, h)

        if self.theme:
            accent = self.theme['accent']
            base_color = QColor(accent)
        else:
            base_color = QColor(100, 200, 255)

        # Color based on level
        if self.level > 0.5:
            gradient.setColorAt(0, QColor(base_color.red(), base_color.green(), base_color.blue(), 200))
            gradient.setColorAt(1, QColor(base_color.red() // 2, base_color.green() // 2, base_color.blue(), 200))
        elif self.level > 0.2:
            gradient.setColorAt(0, QColor(255, 200, 100, 200))
            gradient.setColorAt(1, QColor(255, 150, 50, 200))
        else:
            gradient.setColorAt(0, QColor(255, 100, 100, 200))
            gradient.setColorAt(1, QColor(255, 50, 50, 200))

        painter.fillPath(path, gradient)
        painter.end()
