import socket
import threading

class ChatServer:
    def __init__(self, host='0.0.0.0', port=8080):
        # 클라이언트 소켓을 키로, 닉네임을 값으로 저장하는 딕셔너리
        self.clients = {}  
        # 공유 자원(clients 딕셔너리)의 동시 접근을 제어하기 위한 Lock
        self.lock = threading.Lock()
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 서버 종료 후 빠른 재시작을 위해 주소 재사용 옵션 설정
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))

    def start_server(self):
        self.server_socket.listen()
        host, port = self.server_socket.getsockname()
        print(f'[*] 채팅 서버가 시작되었습니다. (listening on {host}:{port})')
        
        try:
            while True:
                # 클라이언트 연결 수락 (blocking)
                client_socket, addr = self.server_socket.accept()
                
                # 각 클라이언트를 처리할 쓰레드 생성 및 시작
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.daemon = True  # 메인 프로그램 종료 시 쓰레드도 함께 종료
                thread.start()
        except KeyboardInterrupt:
            print('\n[*] 서버를 종료합니다.')
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, addr):
        print(f'[+] 새로운 클라이언트가 연결되었습니다: {addr}')
        
        nickname = self.get_unique_nickname(client_socket)
        
        # Lock을 사용하여 self.clients 딕셔너리에 안전하게 클라이언트 추가
        with self.lock:
            self.clients[client_socket] = nickname

        self.broadcast(f'[{nickname}]님이 입장하셨습니다.', client_socket)
        
        while True:
            try:
                # 클라이언트로부터 메시지 수신 (최대 1024바이트)
                message = client_socket.recv(1024).decode('utf-8')
                
                # 클라이언트 연결이 끊겼을 경우
                if not message:
                    break
                
                # '/종료' 명령 처리
                if message.lower() == '/종료':
                    break
                    
                # 귓속말('/w') 명령 처리
                if message.startswith('/w '):
                    self.send_whisper(message, nickname)
                else:
                    # 전체 메시지 브로드캐스팅
                    full_message = f'{nickname}> {message}'
                    self.broadcast(full_message, client_socket)

            except ConnectionResetError:
                # 클라이언트가 비정상적으로 연결을 종료한 경우
                break
            except Exception as e:
                print(f'[!] 에러 발생: {e}')
                break
        
        # 클라이언트 연결 종료 처리
        self.remove_client(client_socket, nickname)

    def get_unique_nickname(self, client_socket):
        while True:
            client_socket.send('닉네임을 입력하세요: '.encode('utf-8'))
            nickname = client_socket.recv(1024).decode('utf-8').strip()
            
            with self.lock:
                # 닉네임이 비어있지 않고, 현재 사용 중인 닉네임이 아닐 경우
                if nickname and nickname not in self.clients.values():
                    client_socket.send(f'"{nickname}" 닉네임으로 입장합니다.\n'.encode('utf-8'))
                    return nickname
                else:
                    client_socket.send('이미 사용 중이거나 잘못된 닉네임입니다. 다른 닉네임을 입력하세요.\n'.encode('utf-8'))

    def remove_client(self, client_socket, nickname):
        with self.lock:
            if client_socket in self.clients:
                del self.clients[client_socket]
                client_socket.close()
                print(f'[-] 클라이언트 연결이 종료되었습니다: {nickname}')
                # 클라이언트의 퇴장을 모든 클라이언트에게 알림
                self.broadcast(f'[{nickname}]님이 퇴장하셨습니다.', None)

    def broadcast(self, message, sender_socket=None):
        with self.lock:
            # 딕셔너리를 순회하는 동안 변경이 발생할 수 있으므로, 키 리스트의 복사본을 사용
            for client in list(self.clients.keys()):
                if client is not sender_socket:
                    try:
                        client.send(message.encode('utf-8'))
                    except Exception as e:
                        # 메시지 전송 중 오류 발생 시 (예: 클라이언트 비정상 종료)
                        print(f'[!] 브로드캐스트 에러: {e}')
                        nickname_to_remove = self.clients.get(client, '알 수 없는 사용자')
                        self.remove_client(client, nickname_to_remove)
                        
    def send_whisper(self, message, sender_nickname):
        try:
            # '/w 받는사람 메시지' 형식으로 메시지를 분리
            _, recipient_nickname, whisper_message = message.split(' ', 2)
            
            # 메시지를 보낸 사람과 받는 사람의 소켓을 찾음
            with self.lock:
                sender_socket = next((sock for sock, nick in self.clients.items() if nick == sender_nickname), None)
                recipient_socket = next((sock for sock, nick in self.clients.items() if nick == recipient_nickname), None)
            
            if recipient_socket:
                # 귓속말 메시지 포맷팅 및 전송
                formatted_message = f'(귓속말) {sender_nickname}> {whisper_message}'
                recipient_socket.send(formatted_message.encode('utf-8'))
                if sender_socket:
                    sender_socket.send(f'[{recipient_nickname}]님에게 귓속말을 보냈습니다.'.encode('utf-8'))
            else:
                if sender_socket:
                    sender_socket.send(f'[{recipient_nickname}]님을 찾을 수 없습니다.'.encode('utf-8'))

        except ValueError:
            # 메시지 형식이 잘못되었을 경우
            with self.lock:
                sender_socket = next((sock for sock, nick in self.clients.items() if nick == sender_nickname), None)
            if sender_socket:
                sender_socket.send('귓속말 형식이 올바르지 않습니다. (사용법: /w 상대닉네임 메시지)'.encode('utf-8'))
        except Exception as e:
            print(f'[!] 귓속말 처리 에러: {e}')


if __name__ == '__main__':
    chat_server = ChatServer()
    chat_server.start_server()