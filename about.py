from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

from version import VERSION  # <--- Добавляем импорт

ABOUT_HTML = f"""
<div style="color:#e8e8e8; font-size:13px; line-height:1.5;">
  <div style="font-size:20px; font-weight:700; margin-bottom:2px;">Ádel Overlay</div>
  <div style="color:rgba(255,255,255,140); margin-bottom:14px;">Версия {VERSION}</div>

  <div style="margin-bottom:10px;">Автор: <b>Ádel</b></div>
  <div style="margin-bottom:6px;">
    Портфолио:
    <a style="color:#8ab4ff;" href="https://angel-adel.github.io/portfolio/">angel-adel.github.io/portfolio</a>
  </div>
  <div style="margin-bottom:14px;">
    Обратная связь:
    <a style="color:#8ab4ff;" href="mailto:adel.angel2026@gmail.com">adel.angel2026@gmail.com</a>
  </div>

  <div style="color:rgba(255,255,255,90); font-size:11px;">
    © 2026 Ádel. Бесплатно для личного использования.
  </div>
</div>
"""

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setFixedSize(420, 300)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setStyleSheet("QDialog { background: #1e1e1e; }")

        lay = QVBoxLayout(self)
        lab = QLabel(ABOUT_HTML)
        lab.setWordWrap(True)
        lab.setOpenExternalLinks(True)
        lab.setTextFormat(Qt.TextFormat.RichText)
        lay.addWidget(lab)

        btn = QPushButton("Закрыть")
        btn.setStyleSheet("""
            QPushButton { background: rgba(255,255,255,20); color:#e8e8e8;
                          border:none; border-radius:6px; padding:6px 12px; }
            QPushButton:hover { background: rgba(255,255,255,40); }
        """)
        btn.clicked.connect(self.accept)
        lay.addWidget(btn)

    def showEvent(self, e):
        super().showEvent(e)
        self.raise_()
        self.activateWindow()