import sys

# pip install PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('계산기')  # 윈도우 타이틀 설정
        self.setFixedSize(300, 400)   # 고정된 창 크기 설정
        self.init_ui()                # UI 초기화 함수 호출

    def init_ui(self):
        # 세로 박스 레이아웃 생성 (전체 구조)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # 입력창 설정
        self.input_line = QLineEdit()                        # 한 줄 입력창 생성
        self.input_line.setAlignment(Qt.AlignRight)          # 텍스트 오른쪽 정렬
        self.input_line.setFont(QFont("Arial", 24))          # 폰트 설정
        self.input_line.setReadOnly(True)                    # 사용자가 직접 입력 못하게 설정
        vbox.addWidget(self.input_line)                      # 입력창을 vbox에 추가

        # 계산기 버튼 배열
        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '=']
        ]

        # 그리드 레이아웃 생성 (버튼 배치용)
        grid = QGridLayout()
        for row, row_values in enumerate(buttons):           # 각 행과 버튼 값 반복
            for col, text in enumerate(row_values):          # 각 열의 버튼 텍스트 반복
                if text == '':                               # 빈 문자열이면 스킵
                    continue
                btn = QPushButton(text)                      # 버튼 생성
                btn.setFixedSize(60, 60)                     # 버튼 크기 설정
                btn.setFont(QFont("Arial", 18))              # 버튼 폰트 설정
                btn.clicked.connect(self.on_click)           # 클릭 시 함수 연결
                grid.addWidget(btn, row, col)                # 그리드에 버튼 추가

        vbox.addLayout(grid)                                 # 전체 레이아웃에 그리드 추가

    # 버튼 클릭 시 실행되는 함수
    def on_click(self):
        sender = self.sender()           # 어떤 버튼이 눌렸는지 확인
        text = sender.text()             # 버튼의 텍스트 가져오기

        if text == 'C':
            self.input_line.clear()      # 입력창 초기화
        elif text == '=':
            try:
                # eval로 문자열 수식 계산 후 결과 출력
                result = str(eval(self.input_line.text()))
                self.input_line.setText(result)
            except:
                self.input_line.setText("Error")  # 에러 발생 시 표시
        elif text == '+/-':
            current = self.input_line.text()  # 현재 입력창 내용 가져오기
            if current.startswith('-'):
                self.input_line.setText(current[1:])  # 음수일 경우 양수로 변경
            else :
                self.input_line.setText('-' + current)  # 양수일 경우 음수로 변경
        elif text == '%':
            current = self.input_line.text()
            if current:
                result = str(float(current) / 100)  # 현재 입력값을 100으로 나누기
                self.input_line.setText(result)
        else:
            current = self.input_line.text()  # 현재 입력창 내용 가져오기
            if current == '0' and text.isdigit():  # '0'이 맨 앞에 올 경우 처리
                current = ''
            self.input_line.setText(current + text)  # 버튼 텍스트 입력창에 추가

if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication 객체 생성
    calc = Calculator()           # 계산기 객체 생성
    calc.show()                   # 계산기 창 띄우기
    sys.exit(app.exec_())         # 앱 실행 및 종료 처리
