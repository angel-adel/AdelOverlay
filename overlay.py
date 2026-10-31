from PyQt6.QtCore import Qt, QFileInfo
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QFileIconProvider, QDialog, QMenu, 
    QColorDialog, QWidgetAction, QSlider
)
from PyQt6.QtGui import QIcon, QAction, QColor

from add_dialog import AddDialog
from actions import run_shortcut
from about import AboutDialog
from floating_ball import FloatingBall

class Overlay(QWidget):
    def __init__(self, cfg, on_save_cfg, on_quit):
        super().__init__()
        self.cfg = cfg
        self.on_save_cfg = on_save_cfg
        self.on_quit = on_quit

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        w = cfg.get("window", {})
        self.setFixedSize(int(w.get("w", 320)), int(w.get("h", 420)))
        self.move(int(w.get("x", 200)), int(w.get("y", 200)))
        
        self._drag_pos = None
        self.icon_provider = QFileIconProvider()
        
        # Плавающая кнопка (пока скрыта)
        self.ball = FloatingBall(self.show_overlay_from_ball)
        
        self._build_ui()
        self._apply_theme()
        self._refresh_list()

    def _apply_theme(self):
        theme = self.cfg.get("theme", {})
        r, g, b = theme.get("bg_color", [30, 30, 30])
        a = theme.get("bg_alpha", 200)
        
        self.main_widget.setStyleSheet(f"""
            #mainWidget {{
                background-color: rgba({r}, {g}, {b}, {a});
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,25);
            }}
        """)

    def _build_ui(self):
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("mainWidget")
        
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(self.main_widget)

        lay = QVBoxLayout(self.main_widget)
        lay.setContentsMargins(12, 10, 12, 12)
        lay.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel("Ádel Overlay")
        title.setStyleSheet("color: #e8e8e8; font-weight: 600; font-size: 14px;")
        header.addWidget(title)
        header.addStretch()

        btn_add = QPushButton("+")
        btn_add.setFixedSize(26, 26)
        btn_add.setToolTip("Добавить ярлык")
        btn_add.setStyleSheet(self._btn_style())
        btn_add.clicked.connect(self._add_shortcut)
        
        btn_settings = QPushButton("⚙️")
        btn_settings.setFixedSize(26, 26)
        btn_settings.setToolTip("Настройки")
        btn_settings.setStyleSheet(self._btn_style())
        btn_settings.clicked.connect(self._show_settings_menu)

        btn_about = QPushButton("?")
        btn_about.setFixedSize(26, 26)
        btn_about.setToolTip("О программе")
        btn_about.setStyleSheet(self._btn_style())
        btn_about.clicked.connect(self._show_about)
        
        btn_hide = QPushButton("–")
        btn_hide.setFixedSize(26, 26)
        btn_hide.setToolTip("Свернуть в плавающую кнопку")
        btn_hide.setStyleSheet(self._btn_style())
        btn_hide.clicked.connect(self._minimize_to_ball)
        
        btn_close = QPushButton("×")
        btn_close.setFixedSize(26, 26)
        btn_close.setToolTip("Закрыть приложение")
        btn_close.setStyleSheet(self._btn_style() + "QPushButton:hover { background-color: rgba(255,100,100,200); }")
        btn_close.clicked.connect(self.request_quit)

        header.addWidget(btn_add)
        header.addWidget(btn_settings)
        header.addWidget(btn_about)
        header.addWidget(btn_hide)
        header.addWidget(btn_close)
        lay.addLayout(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        self.list_widget = QWidget()
        self.list_widget.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(4)
        self.list_layout.addStretch()
        self.scroll.setWidget(self.list_widget)
        lay.addWidget(self.scroll, 1)

        hint = QLabel("Ctrl+Alt+Space — показать/скрыть")
        hint.setStyleSheet("color: rgba(255,255,255,90); font-size: 11px;")
        lay.addWidget(hint)

    def _minimize_to_ball(self):
        self.hide()
        # Показываем шарик чуть ниже левого верхнего угла оверлея
        self.ball.move(self.x() + 20, self.y() + 20)
        self.ball.show()

    def show_overlay_from_ball(self):
        self.ball.hide()
        self.show()
        self.raise_()

    def _show_settings_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #2d2d2d; color: white; border: 1px solid #444; border-radius: 6px; padding: 5px; }
            QMenu::item { padding: 5px 20px; }
            QMenu::item:selected { background-color: #444; }
        """)
        
        color_menu = menu.addMenu("🎨 Цвет фона")
        colors = [
            ("Тёмный", QColor(30, 30, 30)),
            ("Светлый", QColor(240, 240, 240)),
            ("Синий", QColor(20, 50, 90)),
            ("Фиолетовый", QColor(60, 20, 80)),
            ("Зелёный", QColor(20, 70, 40))
        ]
        for name, color in colors:
            a = QAction(name)
            a.triggered.connect(lambda checked, c=color: self._set_bg_color(c))
            color_menu.addAction(a)
            
        custom = QAction("Свой цвет...")
        custom.triggered.connect(self._choose_custom_color)
        color_menu.addAction(custom)

        menu.addSeparator()
        
        # Слайдер прозрачности
        opacity_action = QWidgetAction(self)
        opacity_widget = QWidget()
        opacity_layout = QHBoxLayout(opacity_widget)
        opacity_layout.setContentsMargins(10, 5, 10, 5)
        label = QLabel("Прозрачность:")
        label.setStyleSheet("color: white;")
        opacity_layout.addWidget(label)
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(100, 255)
        slider.setValue(self.cfg["theme"].get("bg_alpha", 200))
        slider.setFixedWidth(120)
        slider.valueChanged.connect(self._set_alpha)
        opacity_layout.addWidget(slider)
        
        opacity_action.setDefaultWidget(opacity_widget)
        menu.addAction(opacity_action)

        menu.exec(self.cursor().pos())

    def _set_bg_color(self, color: QColor):
        self.cfg["theme"]["bg_color"] = [color.red(), color.green(), color.blue()]
        self.on_save_cfg()
        self._apply_theme()

    def _choose_custom_color(self):
        c = QColorDialog.getColor(QColor(*self.cfg["theme"]["bg_color"]), self, "Выберите цвет")
        if c.isValid():
            self._set_bg_color(c)

    def _set_alpha(self, val):
        self.cfg["theme"]["bg_alpha"] = val
        self.on_save_cfg()
        self._apply_theme()

    def _show_about(self):
        dlg = AboutDialog(self)
        dlg.exec()

    @staticmethod
    def _btn_style():
        return """
            QPushButton {
                background-color: rgba(255,255,255,18);
                color: #e8e8e8;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: rgba(255,255,255,35); }
        """

    def _refresh_list(self):
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        for i, sc in enumerate(self.cfg.get("shortcuts", [])):
            row = QWidget()
            row.setStyleSheet("QWidget { background: rgba(255,255,255,10); border-radius: 6px; } QWidget:hover { background: rgba(255,255,255,20); }")
            row_lay = QHBoxLayout(row)
            row_lay.setContentsMargins(6, 4, 6, 4)
            row_lay.setSpacing(8)
            
            icon_lbl = QLabel()
            if sc.get("type") == "folder":
                icon = self.icon_provider.icon(QFileIconProvider.IconType.Folder)
            elif sc.get("type") == "file":
                icon = self.icon_provider.icon(QFileInfo(sc.get("target")))
            else:
                icon = self.icon_provider.icon(QFileIconProvider.IconType.Computer)
            icon_lbl.setPixmap(icon.pixmap(16, 16))
            row_lay.addWidget(icon_lbl)
            
            name_btn = QPushButton(sc.get("name", "Без имени"))
            name_btn.setStyleSheet("""
                QPushButton { background: transparent; color: #e8e8e8; text-align: left; padding: 0; border: none; font-size: 13px; }
                QPushButton:hover { color: #ffffff; }
            """)
            name_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            name_btn.clicked.connect(lambda checked, s=sc: run_shortcut(s))
            row_lay.addWidget(name_btn, 1)
            
            del_btn = QPushButton("×")
            del_btn.setFixedSize(20, 20)
            del_btn.setStyleSheet("""
                QPushButton { background: transparent; color: rgba(255,255,255,100); border: none; font-size: 14px; }
                QPushButton:hover { color: #ff6b6b; }
            """)
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.clicked.connect(lambda checked, idx=i: self._remove_shortcut(idx))
            row_lay.addWidget(del_btn)
            
            self.list_layout.insertWidget(self.list_layout.count() - 1, row)

    def _add_shortcut(self):
        dlg = AddDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.result_data:
            self.cfg.setdefault("shortcuts", []).append(dlg.result_data)
            self.on_save_cfg()
            self._refresh_list()

    def _remove_shortcut(self, idx):
        if 0 <= idx < len(self.cfg.get("shortcuts", [])):
            self.cfg["shortcuts"].pop(idx)
            self.on_save_cfg()
            self._refresh_list()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            e.accept()

    def mouseMoveEvent(self, e):
        if self._drag_pos is not None and e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)
            e.accept()

    def mouseReleaseEvent(self, e):
        self._drag_pos = None
        self.on_save_cfg(self.x(), self.y())
        
    def request_quit(self):
        if callable(self.on_quit):
            self.on_quit()