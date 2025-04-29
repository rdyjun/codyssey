from PyQt5.QtWidgets import QApplication
from calculator_window import CalculatorWindow

if __name__ == "__main__":
    app = QApplication([])      # PyQT로 GUI를 생성하기 위한 QApplication 객체 생성
    window = CalculatorWindow() # 구현한 GUI 생성
    window.show()               # 생성한 GUI를 화면에 표시하도록 설정
    app.exec_()                 # 프로그램 실행
