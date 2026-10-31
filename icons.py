import os
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QPen
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtWidgets import QApplication

def get_adel_icon() -> QIcon:
    """Круглая иконка с буквой Á для трея и приложения"""
    pm = QPixmap(64, 64)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Тёмный круг с лёгкой обводкой
    p.setBrush(QColor(30, 30, 30))
    p.setPen(QPen(QColor(255, 255, 255, 80), 2))
    p.drawEllipse(4, 4, 56, 56)
    
    # Буква Á
    p.setPen(QColor(232, 232, 232))
    p.setFont(QFont("Arial", 28, QFont.Weight.Bold))
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, "Á")
    p.end()
    return QIcon(pm)

def generate_ico_file(path="icon.ico"):
    """Генерирует файл .ico для сборки PyInstaller"""
    if not QApplication.instance():
        app = QApplication([])
        
    # Создаем несколько размеров для Windows
    pixmaps = []
    for size in [16, 32, 48, 64, 128, 256]:
        pm = QPixmap(size, size)
        pm.fill(Qt.GlobalColor.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        scale = size / 64.0
        p.scale(scale, scale)
        
        p.setBrush(QColor(30, 30, 30))
        p.setPen(QPen(QColor(255, 255, 255, 80), 2))
        p.drawEllipse(4, 4, 56, 56)
        
        p.setPen(QColor(232, 232, 232))
        p.setFont(QFont("Arial", int(28), QFont.Weight.Bold))
        p.drawText(QRectF(0, 0, 64, 64), Qt.AlignmentFlag.AlignCenter, "Á")
        p.end()
        pixmaps.append(pm)
        
    # В PyQt6 сохранение многокадрового .ico может быть ограничено,
    # поэтому используем самый большой размер как базовый
    pixmaps[-1].save(path, "ICO")
    print(f"Иконка сгенерирована: {os.path.abspath(path)}")

if __name__ == "__main__":
    generate_ico_file()