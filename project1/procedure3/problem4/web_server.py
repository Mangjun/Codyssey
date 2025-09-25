import http.server
import socketserver
import json
import urllib.request
from datetime import datetime

# 서버가 사용할 포트 번호
PORT = 8080

def get_ip_location(ip_address):
    # 로컬호스트나 사설 IP는 위치 조회가 불가능하므로 제외합니다.
    if ip_address == '127.0.0.1' or ip_address.startswith(('192.168.', '10.')):
        return ' (로컬 또는 사설 IP)'

    try:
        # 표준 라이브러리인 urllib를 사용하여 API 요청
        url = f'http://ip-api.com/json/{ip_address}'
        with urllib.request.urlopen(url, timeout=3) as response:
            data = json.loads(response.read().decode())
            
            if data['status'] == 'success':
                country = data.get('country', 'N/A')
                city = data.get('city', 'N/A')
                return f' (위치: {city}, {country})'
            else:
                return ' (위치 정보 조회 실패)'
    except Exception as e:
        # API 요청 중 에러 발생 시 (타임아웃 등)
        print(f'[!] 위치 정보 조회 에러: {e}')
        return ' (위치 정보 조회 불가)'

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 1. 접속 정보 로깅
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        
        # 보너스 과제: IP 위치 정보 가져오기
        location_info = get_ip_location(client_ip)
        
        print(f'접속 시간: {current_time}')
        print(f'클라이언트 IP: {client_ip}{location_info}')
        print('-' * 50)  # 로그 구분을 위한 라인

        # 2. index.html 파일 읽기 및 전송
        try:
            # 루트 경로('/') 요청 시 'index.html' 파일을 서빙하도록 설정
            if self.path == '/':
                file_path = 'index.html'
            else:
                # 보안을 위해 루트 경로 외의 요청은 무시하고 index.html로 연결
                file_path = 'index.html'

            # 파일을 바이너리 읽기 모드('rb')로 열기
            with open(file_path, 'rb') as file:
                content = file.read()
            
            # 200 OK 응답 코드 전송
            self.send_response(200)
            # UTF-8로 인코딩된 HTML 문서임을 헤더에 명시
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 파일 내용을 응답의 본문(body)으로 전송
            self.wfile.write(content)
            
        except FileNotFoundError:
            # index.html 파일이 없는 경우 404 에러 응답
            self.send_error(404, "오류: 'index.html' 파일을 찾을 수 없습니다.")
        except Exception as e:
            # 기타 서버 오류 발생 시 500 에러 응답
            self.send_error(500, f"서버 내부 오류: {e}")

# --- 서버 실행 부분 ---
if __name__ == '__main__':
    # TCPServer 객체를 생성하여 요청을 처리할 핸들러를 지정
    with socketserver.TCPServer(('', PORT), MyHttpRequestHandler) as httpd:
        print(f'[*] 서버가 포트 {PORT}에서 실행 중입니다...')
        print(f'웹 브라우저에서 http://127.0.0.1:{PORT} 으로 접속하세요.')
        print('서버를 중지하려면 Ctrl+C를 누르세요.')
        
        try:
            # 서버를 계속 실행하여 요청을 처리
            httpd.serve_forever()
        except KeyboardInterrupt:
            # Ctrl+C 입력 시 서버를 정상적으로 종료
            print('\n[*] 서버를 종료합니다.')
            httpd.shutdown()