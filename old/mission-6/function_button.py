from button import Button

class FunctionButton(Button):
    def __init__(self, row, column, row_span, column_span, text):
        super().__init__(row, column, row_span, column_span, text, '#a5a5a5')

class ACButton(FunctionButton):
    def __init__(self):
        super().__init__(0, 0, 1, 1, 'AC')

class ChangeSignButton(FunctionButton):
    def __init__(self):
        super().__init__(0, 1, 1, 1, '±')

class PercentButton(FunctionButton):
    def __init__(self):
        super().__init__(0, 2, 1, 1, '%')
