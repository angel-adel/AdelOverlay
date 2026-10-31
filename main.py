import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from pynput import keyboard as pynput_kb

from config import load_config, save_config
from overlay import Overlay
from tray import create_tray
from about import AboutDialog

# Мост для безопасного вызова хоткея из потока pynput в GUI-поток
class HotkeyBridge(QObject):
    triggered = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._listener = None

    def start(self):
        def on_activate():
            self.triggered.emit()  # Отправляем сигнал в GUI-поток

        self._listener = pynput_kb.GlobalHotKeys({'<ctrl>+<alt>+<space>': on_activate})
        self._listener.start()

    def stop(self):
        if self._listener:
            self._listener.stop()

def main():
    cfg = load_config()
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    def save_pos_and_config(x=None, y=None):
        if x is not None and y is not None:
            cfg["window"]["x"] = x
            cfg["window"]["y"] = y
        save_config(cfg)

    hotkey = HotkeyBridge()

    def quit_app():
        hotkey.stop()
        cfg["window"]["x"] = overlay.x()
        cfg["window"]["y"] = overlay.y()
        save_config(cfg)
        app.quit()

    overlay = Overlay(cfg, save_pos_and_config, quit_app)
    overlay.show()

    def toggle():
        if overlay.isVisible():
            overlay.hide()
        else:
            overlay.show()
            overlay.raise_()

    # Подключаем сигнал к функции toggle (Qt.QueuedConnection гарантирует, что вызов будет в GUI-потоке)
    hotkey.triggered.connect(toggle, Qt.ConnectionType.QueuedConnection)
    hotkey.start()

    tray = create_tray(app, overlay, AboutDialog, quit_app)
    
    if tray:
        tray.showMessage(
            "Ádel Overlay",
            "Запущено. Ctrl+Alt+Space — показать/скрыть.",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )

    sys.exit(app.exec())

if __name__ == "__main__":
    main()