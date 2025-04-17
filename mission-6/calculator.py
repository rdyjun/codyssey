import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from function_button import ACButton, ChangeSignButton, PercentButton
from operator_button import (
    DivisionButton, MultiplicationButton, SubtractionButton,
    AdditionButton, EqualsButton
)
from number_button import (
    ZeroButton, OneButton, TwoButton, ThreeButton,
    FourButton, FiveButton, SixButton, SevenButton,
    EightButton, NineButton, DotButton
)

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(350, 500)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #18191a;")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Display
        self.display = QLineEdit("4,256,545")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Arial", 36, QFont.Bold))
        self.display.setStyleSheet("background: transparent; color: white; border: none; padding: 10px;")
        main_layout.addWidget(self.display)

        # 버튼 레이아웃
        btn_layout = QGridLayout()
        main_layout.addLayout(btn_layout)

        buttons = [
            ACButton(),
            ChangeSignButton(),
            PercentButton(),
            DivisionButton(),
            MultiplicationButton(),
            SubtractionButton(),
            AdditionButton(),
            EqualsButton(),
            ZeroButton(),
            OneButton(),
            TwoButton(),
            ThreeButton(),
            FourButton(),
            FiveButton(),
            SixButton(),
            SevenButton(),
            EightButton(),
            NineButton(),
            DotButton()
        ]

        for button in buttons:
            btn_layout.addWidget(button, button.row, button.column, button.row_span, button.column_span)

if __name__ == "__main__":
    app = QApplication([])
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec_())
