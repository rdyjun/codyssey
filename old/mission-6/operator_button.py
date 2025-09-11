from button import Button

class OperatorButton(Button):
    def __init__(self, row, column, row_span, column_span, text):
        super().__init__(row, column, row_span, column_span, text, '#ff9500')

class DivisionButton(OperatorButton):
    def __init__(self):
        super().__init__(0, 3, 1, 1, '÷')

class MultiplicationButton(OperatorButton):
    def __init__(self):
        super().__init__(1, 3, 1, 1, '×')

class SubtractionButton(OperatorButton):
    def __init__(self):
        super().__init__(2, 3, 1, 1, '-')

class AdditionButton(OperatorButton):
    def __init__(self):
        super().__init__(3, 3, 1, 1, '+')

class EqualsButton(OperatorButton):
    def __init__(self):
        super().__init__(4, 3, 1, 1, '=')