from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, QComboBox)
from PyQt6.QtCore import Qt

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить ярлык")
        self.setFixedSize(400, 240)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("QDialog { background: #1e1e1e; color: #e8e8e8; }")
        
        self.result_data = None
        
        lay = QVBoxLayout(self)
        
        # Название
        lay.addWidget(QLabel("Название (если пусто — возьмётся имя файла):"))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("QLineEdit { background: #2d2d2d; color: white; padding: 4px; border: 1px solid #444; border-radius: 4px; }")
        lay.addWidget(self.name_input)
        
        # Тип
        lay.addWidget(QLabel("Тип:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Программа / Файл", "Папка", "Команда"])
        self.type_combo.setStyleSheet("QComboBox { background: #2d2d2d; color: white; padding: 4px; border: 1px solid #444; border-radius: 4px; }")
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        lay.addWidget(self.type_combo)
        
        # Путь
        lay.addWidget(QLabel("Путь или команда:"))
        path_lay = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setStyleSheet("QLineEdit { background: #2d2d2d; color: white; padding: 4px; border: 1px solid #444; border-radius: 4px; }")
        path_lay.addWidget(self.path_input)
        
        self.browse_btn = QPushButton("Обзор...")
        self.browse_btn.setStyleSheet("QPushButton { background: #444; color: white; padding: 4px 10px; border-radius: 4px; }")
        self.browse_btn.clicked.connect(self._browse)
        path_lay.addWidget(self.browse_btn)
        lay.addLayout(path_lay)
        
        lay.addStretch()
        
        # Кнопки
        btns = QHBoxLayout()
        ok_btn = QPushButton("Добавить")
        ok_btn.setStyleSheet("QPushButton { background: #2d7d46; color: white; padding: 6px 14px; border-radius: 4px; font-weight: bold; }")
        ok_btn.clicked.connect(self._accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet("QPushButton { background: #444; color: white; padding: 6px 14px; border-radius: 4px; }")
        cancel_btn.clicked.connect(self.reject)
        btns.addStretch()
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)
        lay.addLayout(btns)
        
    def _on_type_changed(self, idx):
        # Если "Команда" — прячем кнопку "Обзор"
        self.browse_btn.setVisible(idx != 2)
        
    def _browse(self):
        idx = self.type_combo.currentIndex()
        if idx == 1: # Папка
            path = QFileDialog.getExistingDirectory(self, "Выбрать папку")
        else: # Файл
            path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл")
        if path:
            self.path_input.setText(path)
            if not self.name_input.text():
                import os
                self.name_input.setText(os.path.basename(path))

    def _accept(self):
        target = self.path_input.text().strip()
        if not target:
            return
        name = self.name_input.text().strip()
        if not name:
            import os
            name = os.path.basename(target)
            
        idx = self.type_combo.currentIndex()
        type_map = {0: "file", 1: "folder", 2: "command"}
        
        self.result_data = {
            "name": name,
            "type": type_map[idx],
            "target": target
        }
        self.accept()