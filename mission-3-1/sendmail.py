import smtplib
import os

# MIMEMultipart: 여러 부분(텍스트, 첨부 파일 등)으로 구성된 이메일을 만들 때 사용
from email.mime.multipart import MIMEMultipart
# MIMEText: 이메일의 본문(텍스트) 부분을 만들 때 사용
from email.mime.text import MIMEText
# MIMEBase: 이메일에 첨부될 파일(이미지, 문서 등)을 표현할 때 사용
from email.mime.base import MIMEBase
# encoders: 첨부 파일을 이메일에 포함할 수 있는 형식(Base64)으로 인코딩하는 데 사용
from email import encoders

def send_gmail(sender_email, app_password, receiver_email, subject, body, attachment_path=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    # 이메일 메시지 객체 생성 (MIMEMultipart)
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # 이메일 본문 추가 (MIMEText)
    # 'plain'은 일반 텍스트 형식의 본문
    msg.attach(MIMEText(body, 'plain'))

    # 보너스 과제: 첨부 파일 처리
    if attachment_path and os.path.exists(attachment_path):
        try:
            with open(attachment_path, 'rb') as attachment:
                # 'application/octet-stream'은 특정 유형을 알 수 없는 바이너리 파일을 의미
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            # 파일을 Base64로 인코딩
            encoders.encode_base64(part)

            # 첨부 파일의 헤더 정보를 설정
            file_name = os.path.basename(attachment_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={file_name}',
            )

            # 메시지 객체에 첨부 파일 부분을 추가합니다.
            msg.attach(part)
        except Exception as e:
            print(f'파일 첨부 중 오류가 발생했습니다: {e}')
            return False

    # SMTP 서버 연결 및 이메일 전송
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
        # SMTP 서버에 로그인
        server.login(sender_email, app_password)
        
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        server.quit()
        
        print('이메일을 성공적으로 보냈습니다!')
        return True
    
    # 로그인 실패 시 (예: 앱 비밀번호 오류)
    except smtplib.SMTPAuthenticationError:
        print('로그인에 실패했습니다. 이메일 주소와 앱 비밀번호를 확인해주세요.')
        print('Gmail 2단계 인증을 사용하고, 앱 비밀번호를 생성해야 합니다.')
    # 서버 연결 실패 시
    except smtplib.SMTPConnectError:
        print('SMTP 서버에 연결할 수 없습니다. 네트워크 상태나 서버 주소를 확인해주세요.')
    # 기타 예외
    except Exception as e:
        print(f'이메일 전송 중 알 수 없는 오류가 발생했습니다: {e}')
    
    return False

# 이 스크립트가 직접 실행될 때만 아래 코드가 동작합니다.
if __name__ == '__main__':
    SENDER_EMAIL = input('보내는 사람의 Gmail 주소를 입력하세요: ')
    
    APP_PASSWORD = input('Gmail 앱 비밀번호를 입력하세요: ') 
    
    RECEIVER_EMAIL = input('받는 사람의 이메일 주소를 입력하세요: ')
    
    # 4. 이메일 제목과 본문
    email_subject = '파이썬으로 보내는 테스트 메일'
    email_body = (
        '안녕하세요.\n'
        '이 메일은 Python의 smtplib 라이브러리를 사용하여 자동으로 발송되었습니다.\n\n'
        '감사합니다.'
    )
    
    attachment_file_path = os.path.join(os.path.dirname(__file__), 'mission-3-1/attachment_file_path.txt')

    send_gmail(
        SENDER_EMAIL,
        APP_PASSWORD,
        RECEIVER_EMAIL,
        email_subject,
        email_body,
        attachment_file_path
    )
