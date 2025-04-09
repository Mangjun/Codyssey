import sys

# pip install PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('계산기')         # 윈도우 타이틀 설정
        self.setFixedSize(300, 400)           # 고정된 창 크기 설정
        self.init_ui()                        # UI 초기화 함수 호출
        self.operator = ('+', '-', 'x', '÷')  # 연산자 목록

    def init_ui(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self.setStyleSheet("background-color: black;")  # 전체 배경

        self.input_line = QLineEdit()
        self.input_line.setAlignment(Qt.AlignRight)
        self.input_line.setFont(QFont("Arial", 30))
        self.input_line.setReadOnly(True)
        self.input_line.setStyleSheet("background-color: black; color: white; border: none;")
        self.input_line.setFixedHeight(80)
        vbox.addWidget(self.input_line)

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid = QGridLayout()
        grid.setSpacing(10)

        for row, row_values in enumerate(buttons):
            col = 0
            for text in row_values:
                btn = QPushButton(text)
                btn.setFont(QFont("Arial", 20))
                btn.clicked.connect(self.on_click)

                # 색상 및 스타일
                if text in ['AC', '+/-', '%']:
                    btn.setStyleSheet("background-color: lightgray; color: black; border: none; border-radius: 30px;")
                elif text in ['÷', 'x', '-', '+', '=']:
                    btn.setStyleSheet("background-color: orange; color: white; border: none; border-radius: 30px;")
                else:
                    btn.setStyleSheet("background-color: #333333; color: white; border: none; border-radius: 30px;")

                # 버튼 높이 지정 (크기 통일)
                btn.setMinimumSize(60, 60)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                if text == '0':
                    grid.addWidget(btn, row, col, 1, 2)  # colspan = 2
                    col += 2
                else:
                    grid.addWidget(btn, row, col)
                    col += 1

        vbox.addLayout(grid)

    # 계산기 데이터 유효성 검사
    def valid_scope(self, data):
        min_val = -99999999999.0
        max_val = 99999999999.0

        if not isinstance(data, (int, float)):
            return False
        if data < min_val or data > max_val:
            return False
        return True

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y
    
    def divide(self, x, y):
        return x / y if y != 0 else 'Error'  # 0으로 나누기 방지

    def reset(self):
        self.input_line.setText('')      # 입력창 초기화

    def negative_positive(self):
        current = self.input_line.text()
        if current.startswith('-'):
            self.input_line.setText(current[1:])  # 음수일 경우 양수로 변경
        else :
            self.input_line.setText('-' + current)  # 양수일 경우 음수로 변경

    def percent(self):
        current = self.input_line.text()
        if current:
            result = str(float(current) / 100)  # 현재 입력값을 100으로 나누기
            self.input_line.setText(result)

    '''
    다른 방법으로는 replace()로 연산자 변환 -> eval() 함수를 사용하여 문자열 수식을 계산 가능
    하지만 eval()은 보안상 위험할 수 있으므로 주의가 필요
    '''
    def equal(self):
        expression = self.input_line.text()

        if expression == '':
            return

        # 연산자 우선 순위 설정
        precedence = {'+': 1, '-': 1, 'x': 2, '÷': 2}

        # 토큰화
        tokens = []
        buffer = ''

        for ch in expression:
            if ch.isdigit() or ch == '.':
                buffer += ch
            else:
                if buffer:
                    tokens.append(buffer)
                    buffer = ''
                if ch in precedence:
                    tokens.append(ch)
        if buffer:  # 버퍼 비우기
            tokens.append(buffer)

        
        # 후위 표기법 변환
        output = []  # 후위 표기법 결과
        calc_stack = []  # 연산자 스택

        for token in tokens:
            if token.isdigit() or '.' in token:
                output.append(float(token))  # 숫자일 경우 바로 추가
            elif token in precedence:
                while calc_stack and precedence[calc_stack[-1]] >= precedence[token]:  # 연산자 우선 순위 비교
                    output.append(calc_stack.pop())
                calc_stack.append(token)
        
        while calc_stack:  # 스택에 남은 연산자 처리
            output.append(calc_stack.pop())

        # 후위 표기법 계산
        try:
            stack = []  # 계산 스택
            for token in output:
                if isinstance(token, float):  # 숫자일 경우 스택에 추가
                    stack.append(token)
                else:  # 연산자일 경우 계산
                    b = stack.pop()
                    a = stack.pop()
                    if token == '+':
                        stack.append(self.add(a, b))
                    elif token == '-':
                        stack.append(self.subtract(a, b))
                    elif token == 'x':
                        stack.append(self.multiply(a, b))
                    elif token == '÷':
                        result = self.divide(a, b)
                        if result == 'Error':
                            self.input_line.setText('Error')
                            return
                        stack.append(result)

            # 최종 결과 출력
            if len(stack) == 1 and self.valid_scope(stack[0]):
                result = round(stack[0], 6)  # 소수점 6자리 반올림
                result_str = str(result).rstrip('0').rstrip('.') if '.' in str(result) else str(result)  # 불필요한 0 제거

                # 폰트 크기 조정
                length = len(result_str)
                if length <= 9:
                    self.input_line.setFont(QFont("Arial", 24))
                elif length <= 12:
                    self.input_line.setFont(QFont("Arial", 18))
                elif length <= 16:
                    self.input_line.setFont(QFont("Arial", 14))
                else:
                    self.input_line.setFont(QFont("Arial", 10))

                self.input_line.setText(result_str)
            else:
                self.input_line.setText('Error')
        except:
            self.input_line.setText('Error')
            return

    # 버튼 클릭 시 실행되는 함수
    def on_click(self):
        sender = self.sender()           # 어떤 버튼이 눌렸는지 확인
        text = sender.text()             # 버튼의 텍스트 가져오기

        if text == 'AC':                 # AC 버튼 클릭 시 초기화
            self.reset()
        elif text == '+/-':             # +/- 버튼 클릭 시 부호 변경
            self.negative_positive()
        elif text == '%':               # % 버튼 클릭 시 백분율 계산
            self.percent()
        elif text == '=':               # = 버튼 클릭 시 계산 수행
            self.equal()
        elif text == '.':               # . 버튼 클릭 시 소수점 추가
            current = self.input_line.text()
            if current == '' or current == 'Error':
                self.input_line.setText('0.')
            elif '.' not in current:
                self.input_line.setText(current + '.') 
        else:                           # 숫자 및 연산자 버튼 클릭 시
            current = self.input_line.text()  # 현재 입력창 내용 가져오기

            # 에러 상태면 초기화
            if current == 'Error':
                current = ''

            # '0'이 맨 앞에 올 경우 숫자만 덮어쓰기
            if current == '0' and text.isdigit():
                current = ''

            # 연산자가 처음에 오는 것을 막기
            if current == '' and text in self.operator:
                return
            
            # 연산자가 바로 앞에 또 입력되지 않도록 방지
            if current and current[-1] in self.operator and text in self.operator:
                return

            self.input_line.setText(current + text) # 입력창에 버튼 텍스트 추가
           
if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication 객체 생성
    calc = Calculator()           # 계산기 객체 생성
    calc.show()                   # 계산기 창 띄우기
    sys.exit(app.exec_())         # 앱 실행 및 종료 처리
