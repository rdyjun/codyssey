from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtGui import QFont

font = QFont("Arial", 22)

class Button(QPushButton):
    def __init__(self, row, column, row_span, column_span, text, color):
        super().__init__(text)
        self.row = row
        self.column = column
        self.row_span = row_span
        self.column_span = column_span
        self.color = color

        # 버튼 스타일 설정
        self.setFont(font)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: {"black" if self.color == "#a5a5a5" else "white"};
                border: none;
                border-radius: 35px;
                min-width: 70px;
                min-height: 70px;
            }}

            QPushButton:pressed {{
                background-color: #666666;
            }}
        """)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)