from button import Button

class NumberButton(Button):
    def __init__(self, row, column, row_span, column_span, text):
        super().__init__(row, column, row_span, column_span, text, '#323232')

class ZeroButton(NumberButton):
    def __init__(self):
        super().__init__(4, 0, 1, 2, '0')

class OneButton(NumberButton):
    def __init__(self):
        super().__init__(3, 0, 1, 1, '1')

class TwoButton(NumberButton):
    def __init__(self):
        super().__init__(3, 1, 1, 1, '2')

class ThreeButton(NumberButton):
    def __init__(self):
        super().__init__(3, 2, 1, 1, '3')

class FourButton(NumberButton):
    def __init__(self):
        super().__init__(2, 0, 1, 1, '4')

class FiveButton(NumberButton):
    def __init__(self):
        super().__init__(2, 1, 1, 1, '5')

class SixButton(NumberButton):
    def __init__(self):
        super().__init__(2, 2, 1, 1, '6')

class SevenButton(NumberButton):
    def __init__(self):
        super().__init__(1, 0, 1, 1, '7')

class EightButton(NumberButton):
    def __init__(self):
        super().__init__(1, 1, 1, 1, '8')

class NineButton(NumberButton):
    def __init__(self):
        super().__init__(1, 2, 1, 1, '9')

class DotButton(NumberButton):
    def __init__(self):
        super().__init__(4, 2, 1, 1, '.')