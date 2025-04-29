
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
        # 이미 연산자와 피연산자에 값이 할당된 경우 equal 실행 
        if self.pointer == 1 and self.operator is not None:
            self.equal()
            
        self.operator = operator
        self.operand = None
        self.pointer = 1

    def add_number(self, current, number):
        if current == '0' or current == 0 or current is None:
            return number
        
        if number == '.' and '.' in current:
            return current

        if (len(current) > 2 and current[-2] is not [0-9] and current[-1] is 0):
            return current[:-2] + number
        
        return current + number

    def change_pointer(self):
        self.pointer += 1
        self.pointer %= 2
    
    def add(self):
        result = float(self.current) + float(self.operand)
        if result % 1 == 0:
            return int(result)
        
        return float(result)

    def subtract(self):
        result = float(self.current) - float(self.operand)
        if result % 1 == 0:
            return int(result)
        
        return float(result)

    def multiply(self):
        result = float(self.current) * float(self.operand)
        if result % 1 == 0:
            return int(result)
        
        return float(result)

    def divide(self):
        result = float(self.current) / float(self.operand)
        if result % 1 == 0:
            return int(result)
        
        return float(result)
    
    def equal(self):
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
    
    def reset(self):
        self.current = '0'
        self.operand = None
        self.operator = None
        self.pointer = 0

    def negative_positive(self):
        if self.pointer == 0:
            if self.current == '0' or self.current is None:
                return
            self.current = str(-int(self.current))
            return
        
        if self.operand == '0' or self.operand is None:
            return
        
        self.operand = str(-int(self.operand))

    def percent(self):
        if self.pointer == 0:
            if self.current == '0' or self.current is None:
                return
            
            self.current = str(int(self.current) / 100)
            return
        
        if self.operand == '0' or self.operand is None:
            return
        
        self.operand = str(int(self.operand) / 100)