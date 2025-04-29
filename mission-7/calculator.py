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
        self.calculator = Calculator()  # 계산기 객체 생성

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
        result = self.calculator.input(button.value)
        self.display.setText(result)
    
    def operator_click_event(self, button):
        display_text = self.display.text()

        if isinstance(button, EqualsButton):
            try:
                self.calculator.equal()
                self.display.setText(self.calculator.display())
            except Exception as e:
                self.display.setText("연산식 오류: " + str(e))
            return

        if display_text[-1] in ['+', '-', '*', '/']:
            self.display.setText(display_text[:-1] + button.value)
            return

        self.calculator.add_operator(button.value)
        self.display.setText(self.calculator.display())

class Calculator:
    current = '0'
    operand = None
    operator = None
    pointer = 0

    def input(self, value):
        if self.pointer == 0:
            self.current = self.add_number(self.current, value)
            return self.current
        
        self.operand = self.add_number(self.operand, value)

        display = self.current
        if self.operator is None:   # 연산자가 없으면 current 숫자만 반환
            return display
        
        display += self.operator
        
        if self.operand is None:
            return display
        
        return display + self.operand
    
    def add_operator(self, operator):
        self.operator = operator

        # 이미 연산자와 피연산자에 값이 할당된 경우 equal 실행 
        if self.pointer == 1 and self.operator is not None:
            self.equal()
            
        self.operator = operator
        self.pointer = 1

    def add_number(self, current, number):
        if current == '0' or current == 0 or current is None:
            return number

        if (len(current) > 2 and current[-2] is not [0-9] and current[-1] is 0):
            return current[:-2] + number
        
        return current + number

    def change_pointer(self):
        self.pointer += 1
        self.pointer %= 2
    
    def add(self):
        return int(self.current) + int(self.operand)

    def subtract(self):
        return int(self.current) - int(self.operand)

    def multiply(self):
        return int(self.current) * int(self.operand)

    def divide(self):
        result = int(self.current) / int(self.operand)
        if result % 1 == 0:
            return int(result)
        
        return result
    
    def equal(self):
        print(self.operator)
        if self.operator == '+':
            self.current = str(self.add())
        if self.operator == '-':
            self.current = str(self.subtract())
        if self.operator == '×':
            self.current = str(self.multiply())
        if self.operator == '÷':
            self.current = str(self.divide())

        self.operand = None
        self.operator = None
        self.pointer = 0
    
    def display(self):
        if self.pointer == 0:
            return self.current
        
        if self.operand is None:
            return self.current + self.operator
        
        return self.current + self.operator + self.operand


if __name__ == "__main__":
    app = QApplication([])      # PyQT로 GUI를 생성하기 위한 QApplication 객체 생성
    window = CalculatorWindow() # 구현한 GUI 생성
    window.show()               # 생성한 GUI를 화면에 표시하도록 설정
    app.exec_()                 # 프로그램 실행
