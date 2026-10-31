from PyQt6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtCore import Qt

def make_icon() -> QIcon:
    pm = QPixmap(64, 64)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(30, 30, 30))
    p.setPen(QColor(255, 255, 255, 80))
    p.drawEllipse(2, 2, 60, 60)
    p.setPen(QColor(232, 232, 232))
    p.setFont(QFont("Arial", 28, QFont.Weight.Bold))
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, "Á")
    p.end()
    return QIcon(pm)

def create_tray(app, overlay, about_factory, on_quit):
    if not QSystemTrayIcon.isSystemTrayAvailable():
        return None

    tray = QSystemTrayIcon(make_icon(), app)
    tray.setToolTip("Ádel Overlay (клик — свернуть/развернуть)")

    # Меню делаем, но оно может не открываться на Windows 10 из-за фокуса.
    # Поэтому основной упор делаем на клик по иконке.
    menu = QMenu()
    
    act_toggle = QAction("Показать / Скрыть")
    act_toggle.triggered.connect(lambda: overlay.hide() if overlay.isVisible() else (overlay.show(), overlay.raise_()))
    menu.addAction(act_toggle)

    act_quit = QAction("Выход")
    act_quit.triggered.connect(on_quit)
    menu.addAction(act_quit)

    tray.setContextMenu(menu)
    
    def on_activated(reason):
        # Срабатывает при ЛКМ по иконке
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if overlay.isVisible():
                overlay.hide()
            else:
                overlay.show()
                overlay.raise_()
                
    tray.activated.connect(on_activated)
    tray.show()
    return tray