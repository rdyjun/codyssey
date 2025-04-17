from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from function_button import FunctionButton, ACButton, ChangeSignButton, PercentButton
from operator_button import (
    OperatorButton, DivisionButton, MultiplicationButton,
    SubtractionButton, AdditionButton, EqualsButton
)
from number_button import (
    NumberButton, ZeroButton, OneButton, TwoButton, 
    ThreeButton, FourButton, FiveButton, SixButton,
    SevenButton, EightButton, NineButton, DotButton
)

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")   # 윈도우 창 이름 설정
        self.setFixedSize(350, 500)         # 윈도우 크기 설정
        self.init_ui()                      # 실제 UI 구성

    def init_ui(self):
        self.setStyleSheet("background-color: #18191a;")    # 배경 색

        central_widget = QWidget(self)                      # 위젯 생성, 이 위젯이 있어야 레이아웃 배치가 가능
        self.setCentralWidget(central_widget)               # 위젯을 중앙에 배치

        main_layout = QVBoxLayout()                         # 메인 레이아웃 생성 - 수직 레이아웃
        central_widget.setLayout(main_layout)               # 중앙 위젯에 레이아웃 설정

        # Display
        self.display = QLineEdit("0")               # 초기 값 설정
        self.display.setAlignment(Qt.AlignRight)            # 값 오른쪽 정렬
        self.display.setReadOnly(True)                      # 읽기 전용으로 설정 (계산기기 때문)
        self.display.setFont(QFont("Arial", 36, QFont.Bold))# 폰트 설정
        self.display.setStyleSheet("background: transparent; color: white; border: none; padding: 10px;")
        main_layout.addWidget(self.display)                 # 레이아웃에 배치

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
            button.clicked.connect(lambda _, b=button: self.button_click_event(b))
            btn_layout.addWidget(button, button.row, button.column, button.row_span, button.column_span)

    def button_click_event(self, button):
        if isinstance(button, NumberButton):
            self.number_click_event(button);
        
        if isinstance(button, FunctionButton):
            self.function_click_event(button)

        if isinstance(button, OperatorButton):
            self.operator_click_event(button)

    def number_click_event(self, button):
        display_text = self.display.text()

        if (display_text == '0'):
            self.display.setText(button.value)
            return

        if (len(display_text) > 2 and display_text[-2] is not [0-9] and display_text[-1] is 0):
            self.display.setText(display_text[:-2] + button.value)
            return
        
        self.display.setText(display_text + button.value)
    
    def operator_click_event(self, button):
        display_text = self.display.text()

        if isinstance(button, EqualsButton):
            try:
                result = eval(display_text.replace('÷', '/').replace('×', '*'))
                if result % 1 == 0: # 소수점 제거
                    result = str(int(result))

                self.display.setText(result)
            except Exception as e:
                self.display.setText("연산식 오류: " + str(e))
            return

        if display_text[-1] in ['+', '-', '*', '/']:
            self.display.setText(display_text[:-1] + button.value)
            return

        self.display.setText(display_text + button.value)

if __name__ == "__main__":
    app = QApplication([])      # PyQT로 GUI를 생성하기 위한 QApplication 객체 생성
    window = CalculatorWindow() # 구현한 GUI 생성
    window.show()               # 생성한 GUI를 화면에 표시
    app.exec_()       # 프로그램 종료 전까지 계속 실행
