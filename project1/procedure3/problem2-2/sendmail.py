import csv
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# --- 1. 사용자 설정 영역 ---

# Gmail SMTP 설정 (STARTTLS)
SMTP_CONFIG_GMAIL = {
    'host': 'smtp.gmail.com',
    'port': 587
}

# (보너스) Naver SMTP 설정 (STARTTLS)
SMTP_CONFIG_NAVER = {
    'host': 'smtp.naver.com',
    'port': 587
}

# 발신자 인증 정보 (반드시 '앱 비밀번호'를 사용해야 합니다)
AUTH_INFO_GMAIL = {
    'email': 'your_gmail_account@gmail.com',  # 본인 Gmail 주소
    'pass': 'your_16_digit_app_password',  # 본인 Gmail 앱 비밀번호
    'name': '관리자'  # 발신자 이름 (한글 가능)
}

# (보너스) 네이버 인증 정보
AUTH_INFO_NAVER = {
    'email': 'your_naver_id@naver.com',  # 본인 Naver 주소
    'pass': 'your_naver_app_password',  # 본인 Naver 앱 비밀번호
    'name': '네이버관리자'
}

# 수신자 목록 CSV 파일 경로
CSV_FILE = 'mail_target_list.csv'

# 이메일 제목
EMAIL_SUBJECT = 'HTML 테스트 이메일 (CSV 발송)'

# 발송할 HTML 본문
HTML_CONTENT = """
<html>
<head>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; }
        h1 { color: #0055b8; }
        p { font-size: 14px; }
        .highlight { color: #d9534f; font-weight: bold; }
    </style>
</head>
<body>
    <h1>안녕하세요!</h1>
    <p>이것은 Python에서 보낸 <span class="highlight">HTML</span> 형식의 테스트 이메일입니다.</p>
    <p>이 메일은 CSV 파일의 목록을 기반으로 발송되었습니다.</p>
    <ul>
        <li>CSV 읽기 테스트</li>
        <li>HTML 메일 발송 테스트</li>
        <li>Bcc (숨은 참조) 권장 방식 테스트</li>
    </ul>
</body>
</html>
"""

# --- 2. 핵심 기능 함수 ---

def read_targets(csv_path):
    """CSV 파일에서 이름과 이메일 목록을 읽어 리스트로 반환합니다."""
    targets = []
    try:
        # 한글 깨짐 방지를 위해 encoding='utf-8' 명시
        with open(csv_path, 'r', encoding='utf-8') as f:
            # csv.DictReader를 사용하면 헤더 이름을 키로 사용 가능
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('이름', '').strip()
                email = row.get('이메일', '').strip()
                if name and email:  # 이름과 이메일이 모두 유효한 경우에만 추가
                    targets.append({'name': name, 'email': email})
        
        if not targets:
            print(f"경고: {csv_path} 파일에 유효한 수신자 정보가 없습니다.")
        return targets

    except FileNotFoundError:
        print(f'오류: {csv_path} 파일을 찾을 수 없습니다.')
        return []
    except Exception as e:
        print(f'CSV 파일 읽기 중 오류 발생: {e}')
        return []


def create_html_message(sender_info, subject, html_body):
    """HTML 본문을 포함하는 MIMEMultipart 객체를 생성합니다."""
    
    msg = MIMEMultipart('alternative')
    
    # UTF-8로 인코딩하여 한글 제목 깨짐 방지
    msg['Subject'] = Header(subject, 'utf-8')
    
    # 발신자 정보 설정 (한글 이름 인코딩)
    msg['From'] = formataddr((
        Header(sender_info['name'], 'utf-8').encode(), 
        sender_info['email']
    ))

    # HTML 본문 추가 ('html'로 지정)
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    return msg


def send_mail_via_bcc(smtp_info, auth_info, targets, subject, html_body):
    print(f"--- 'Bcc'(숨은 참조) 일괄 전송 시작 (총 {len(targets)}명) ---")

    # --- [수행과제 #4] 발송 방식 비교 및 선택 ---
    #
    # 1. 'To'/'Cc'에 여러 명 열거 (시도 1)
    #    - 구현: msg['To'] = ", ".join([t['email'] for t in targets])
    #    - 문제: (치명적) 수신자 간 서로의 이메일이 노출되어 개인정보가 유출됩니다.
    #          과제 요건에 부합하지 않아 기각합니다.
    #
    # 2. 한 명씩 반복 발송 (시도 2)
    #    - 구현: for t in targets: server.sendmail(..., [t['email']], ...)
    #    - 문제: 100명 발송 시 100번의 SMTP 전송이 필요합니다. 매우 비효율적이며,
    #          서버 부하가 크고 단시간 대량 발송으로 스팸 간주 위험이 큽니다.
    #
    # 3. 'Bcc' (숨은 참조) 일괄 발송 (★ 최종 선택)
    #    - 구현: 본 함수(send_mail_via_bcc)의 방식.
    #          sendmail()의 수신자 리스트(recipient_emails)에만 실제 대상을 전달.
    #    - 장점: 단 1번의 전송으로 모든 대상에게 발송 (효율적).
    #          수신자 목록이 노출되지 않아 개인정보가 보호됩니다.
    #    - 결론: 효율성과 개인정보 보호를 모두 만족하는 'Bcc' 방식을 선택합니다.
    # -------------------------------------------------

    if not targets:
        print('수신자가 없어 발송을 건너뜁니다.\n')
        return False
    
    # 실제 메일을 수신할 주소 리스트
    recipient_emails = [target['email'] for target in targets]
    
    # 보안 SSL 컨텍스트 생성
    context = ssl.create_default_context()
    
    try:
        # 'with' 구문을 사용하여 서버 연결 자동 관리
        with smtplib.SMTP(smtp_info['host'], smtp_info['port']) as server:
            server.starttls(context=context)  # TLS 암호화 시작
            server.login(auth_info['email'], auth_info['pass'])
            print(f"SMTP 서버({smtp_info['host']}) 로그인 성공.")

            # 메일 메시지 생성
            msg = create_html_message(auth_info, subject, html_body)
            
            # (핵심) 'To' 헤더는 '미지정 수신자' 등으로 설정합니다.
            # 이는 수신자에게 표시되는 부분이며, 실제 발송과는 무관합니다.
            msg['To'] = formataddr((
                Header('미지정 수신자', 'utf-8').encode(), 
                auth_info['email']  # 혹은 발신자 본인 메일
            ))
            
            # (중요) sendmail 함수의 두 번째 인자가 실제 발송 대상입니다.
            # 'To'나 'Cc' 헤더에 없는 주소는 자동으로 'Bcc' 처리됩니다.
            server.sendmail(
                auth_info['email'],  # From (발신자)
                recipient_emails,    # To (실제 수신자 리스트)
                msg.as_string()      # Message (메시지 본문)
            )
            
            print(f' -> {len(recipient_emails)}명 모두에게 \'Bcc\'로 발송 성공.')
            print('  (효율과 개인정보 보호를 모두 만족하는 권장 방식입니다.)\n')
            return True
    
    except smtplib.SMTPException as e:
        print(f'SMTP 오류 발생: {e}\n')
        return False
    except Exception as e:
        print(f'알 수 없는 오류 발생: {e}\n')
        return False


# --- 3. 메인 실행 영역 ---

def main():
    """메인 실행 함수"""
    
    # 0. 설정 값 확인
    if 'your_gmail_account' in AUTH_INFO_GMAIL['email'] or \
       'your_16_digit_app_password' in AUTH_INFO_GMAIL['pass']:
        print('='*60)
        print("주의: 코드 상단의 AUTH_INFO_GMAIL을")
        print("      본인의 Gmail 계정과 앱 비밀번호로 변경해야 합니다.")
        print('='*60)
        return

    # 1. CSV 읽기
    targets = read_targets(CSV_FILE)
    if not targets:
        print('발송할 대상이 없습니다. 스크립트를 종료합니다.')
        return
    
    print(f"\n총 {len(targets)}명의 발송 대상을 '{CSV_FILE}'에서 읽었습니다.")
    
    # --- Gmail로 발송 테스트 ---
    print('\n=== Gmail 발송 테스트 시작 ===')
    
    # 2. 권장 방식(Bcc)으로 발송 실행
    send_mail_via_bcc(
        SMTP_CONFIG_GMAIL, 
        AUTH_INFO_GMAIL, 
        targets,
        EMAIL_SUBJECT, 
        HTML_CONTENT
    )

    # 3. (보너스) 네이버 과제 실행
    run_bonus_naver_task(targets)


def run_bonus_naver_task(targets):
    """보너스 과제: 네이버 SMTP로 발송 시도"""
    
    print('\n=== [보너스 과제] Naver 발송 테스트 시작 ===')

    # 0. 설정 값 확인
    if 'your_naver_id' in AUTH_INFO_NAVER['email'] or \
       'your_naver_app_password' in AUTH_INFO_NAVER['pass']:
        print('네이버 SMTP 설정(AUTH_INFO_NAVER)이 완료되지 않았습니다.')
        print('보너스 과제를 실행하려면 해당 영역을 수정하세요.')
        return

    print("네이버 메일 발송을 시작합니다. (권장 방식 'Bcc' 사용)")
    
    # 네이버로 발송 시도 (동일한 Bcc 함수 사용)
    send_mail_via_bcc(
        SMTP_CONFIG_NAVER, 
        AUTH_INFO_NAVER, 
        targets,
        EMAIL_SUBJECT, 
        HTML_CONTENT
    )

if __name__ == '__main__':
    main()