import socket
import threading
import os

class ChatClient:
    def __init__(self, host='127.0.0.1', port=8080):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.is_running = True

    def start_client(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print('[!] 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.')
            return
        except Exception as e:
            print(f'[!] 연결 중 오류 발생: {e}')
            return

        # 닉네임 설정
        self.setup_nickname()
        
        # 메시지 수신을 위한 쓰레드 시작
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # 메시지 발신
        self.send_messages()
        
        # 클라이언트 종료
        self.client_socket.close()
        print('[*] 클라이언트를 종료합니다.')
    
    def setup_nickname(self):
        while self.is_running:
            try:
                # 서버로부터 '닉네임을 입력하세요: ' 프롬프트를 수신
                prompt = self.client_socket.recv(1024).decode('utf-8')
                nickname = input(prompt)
                self.client_socket.send(nickname.encode('utf-8'))
                
                # 닉네임 설정 결과 메시지 수신
                response = self.client_socket.recv(1024).decode('utf-8')
                print(response)

                # 닉네임이 정상적으로 설정되면 루프 탈출
                if '잘못된 닉네임' not in response:
                    break
            except Exception:
                print('\n[!] 닉네임 설정 중 서버와 연결이 끊어졌습니다.')
                self.is_running = False
                break


    def receive_messages(self):
        while self.is_running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    print('\n[!] 서버와의 연결이 끊어졌습니다.')
                    self.is_running = False
                    break
                # 수신된 메시지를 화면에 출력
                print(message)
            except Exception:
                print('\n[!] 메시지 수신 중 오류가 발생했습니다.')
                self.is_running = False
                break
        os._exit(0) # 연결이 끊어지면 입력 대기 상태를 강제 종료

    def send_messages(self):
        while self.is_running:
            try:
                message = input()
                if not self.is_running:
                    break
                
                self.client_socket.send(message.encode('utf-8'))
                
                if message.lower() == '/종료':
                    self.is_running = False
                    break
            except EOFError: # Ctrl+D 입력 시
                print("\n'/종료'를 입력하여 프로그램을 종료합니다.")
                if self.is_running:
                    self.client_socket.send('/종료'.encode('utf-8'))
                self.is_running = False
                break
            except Exception:
                print('\n[!] 메시지 전송 중 오류가 발생했습니다.')
                self.is_running = False
                break

if __name__ == '__main__':
    client = ChatClient()
    client.start_client()