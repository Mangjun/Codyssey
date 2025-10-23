import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

'''
[앱 비밀번호 생성 방법]
1. Google 계정 관리 페이지에 접속합니다. (myaccount.google.com)
2. 왼쪽 메뉴에서 '보안' 탭으로 이동합니다.
3. 'Google에 로그인하는 방법' 섹션에서 '2단계 인증'을 활성화합니다.
   (이미 활성화되어 있다면 다음 단계로 넘어갑니다.)
4. 2단계 인증 설정 후, 같은 섹션에 '앱 비밀번호' 메뉴가 나타납니다.
5. '앱 비밀번호'를 클릭하고, 앱 이름(예: Python Mail)을 지정하여 비밀번호를 생성합니다.
6. 생성된 16자리 앱 비밀번호를 아래 SENDER_PASSWORD 변수에 입력합니다.
'''

# --- 사용자 설정 부분 ---
# 보내는 사람의 Gmail 계정
SENDER_EMAIL = 'your_gmail_account@gmail.com'
# Google 계정에서 발급받은 16자리 앱 비밀번호
SENDER_PASSWORD = 'your_16_digit_app_password'
# 받는 사람의 이메일 주소
RECEIVER_EMAIL = 'receiver_email_address@example.com'


def send_gmail(sender, password, receiver, subject, body, attachment_path=None):
    try:
        # 이메일 메시지 객체 생성 (MIMEMultipart)
        # 한글 등 비-아스키 문자를 포함하기 위해 'utf-8'로 인코딩을 지정합니다.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        # 이메일 본문 추가 (MIMEText)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # (보너스 과제) 첨부 파일이 있는 경우 처리
        if attachment_path:
            # 파일을 바이너리 읽기 모드('rb')로 엽니다.
            with open(attachment_path, 'rb') as attachment:
                # MIMEBase 객체 생성
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            # 파일을 Base64로 인코딩합니다.
            encoders.encode_base64(part)

            # 첨부 파일 헤더 정보 추가
            # 파일 이름을 ASCII로 변환하여 헤더에 추가합니다.
            # os.path.basename을 사용하여 어떤 OS에서도 파일 이름만 정확히 추출합니다.
            file_name = os.path.basename(attachment_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{file_name}"'
            )
            msg.attach(part)
            print(f"첨부 파일 '{file_name}' 추가 완료.")

        # SMTP 서버에 연결
        print('SMTP 서버에 연결 중...')
        
        # 보안 강화를 위한 기본 SSL 컨텍스트 생성
        context = ssl.create_default_context()
        
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            # TLS 암호화 통신 시작 시 context 전달
            smtp.starttls(context=context)
            
            # SMTP 서버에 로그인
            smtp.login(sender, password)
            print('로그인 성공.')

            # 이메일 발송
            smtp.send_message(msg)
            print(f"'{receiver}'에게 메일을 성공적으로 보냈습니다.")
        
        return True

    except FileNotFoundError:
        print(f"오류: 첨부 파일 '{attachment_path}'을(를) 찾을 수 없습니다.")
        return False
    except smtplib.SMTPAuthenticationError:
        print('오류: SMTP 인증에 실패했습니다.')
        print('보내는 사람의 이메일 주소나 앱 비밀번호가 올바른지 확인하세요.')
        return False
    except smtplib.SMTPException as e:
        print(f'오류: 메일 발송 중 문제가 발생했습니다. (SMTP 오류: {e})')
        return False
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')
        return False

if __name__ == '__main__':
    # --- 이메일 내용 설정 ---
    email_subject = '파이썬으로 보내는 테스트 메일입니다.'
    email_body = '파이썬으로 보내는 테스트 메일입니다.'
    
    # --- 첨부 파일 경로 (없으면 None으로 설정) ---
    # 첨부 파일 테스트를 안 할 경우: file_to_attach = None
    file_to_attach = None 

    # SENDER_EMAIL 또는 SENDER_PASSWORD가 기본값인지 확인
    if SENDER_EMAIL == 'your_gmail_account@gmail.com' or \
       SENDER_PASSWORD == 'your_16_digit_app_password':
        print("="*60)
        print("주의: 코드의 SENDER_EMAIL과 SENDER_PASSWORD를")
        print("      본인의 Gmail 계정과 앱 비밀번호로 변경해야 합니다.")
        print("="*60)
    else:
        send_gmail(
            SENDER_EMAIL,
            SENDER_PASSWORD,
            RECEIVER_EMAIL,
            email_subject,
            email_body,
            file_to_attach
        )