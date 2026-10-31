from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor

class FloatingBall(QWidget):
    def __init__(self, on_click):
        super().__init__()
        self.on_click = on_click
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(50, 50)
        self._drag_pos = None
        self._is_dragging = False

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor(30, 30, 30, 220))
        p.setPen(QColor(255, 255, 255, 100))
        p.drawEllipse(2, 2, 46, 46)
        
        # Рисуем букву "A" (или Á)
        p.setPen(QColor(232, 232, 232))
        font = p.font()
        font.setPointSize(18)
        font.setBold(True)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Á")

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self._is_dragging = False
            e.accept()

    def mouseMoveEvent(self, e):
        if self._drag_pos is not None and e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)
            self._is_dragging = True
            e.accept()

    def mouseReleaseEvent(self, e):
        self._drag_pos = None
        if not self._is_dragging:
            self.on_click() # Если не таскали, а просто кликнули — открываем оверлей
        self._is_dragging = False