import csv
import smtplib
import ssl
import getpass  # 비밀번호를 안전하게 입력받기 위함
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys  # sys.exit() 사용

# --- SMTP 서버 설정 ---
# 주석을 변경하여 사용할 서버를 선택하세요.

# [기본] Google Mail (Gmail) 설정
# 참고: 2단계 인증 사용 시 '앱 비밀번호'가 필요합니다.
SMTP_CONFIG = {
    'server': 'smtp.gmail.com',
    'port': 465  # SSL 용 포트
}

# [보너스 과제] Naver Mail 설정
# 참고: 네이버 메일 설정 > POP3/IMAP 설정 > 'SMTP 사용'을 '사용함'으로 변경해야 합니다.
# 2단계 인증 사용 시 '앱 비밀번호'가 필요합니다.
# SMTP_CONFIG = {
#     'server': 'smtp.naver.com',
#     'port': 465  # SSL 용 포트
# }

CSV_FILENAME = 'mail_target_list.csv'


def load_recipients(csv_filename):
    """
    CSV 파일에서 수신자 목록 (이름, 이메일)을 읽어 리스트로 반환합니다.
    """
    recipients = []
    try:
        # utf-8 인코딩으로 한글 이름 처리
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 행 (이름, 이메일) 건너뛰기

            for row in reader:
                if row and len(row) >= 2:  # 빈 행이나 데이터가 부족한 행 방지
                    name = row[0].strip()
                    email = row[1].strip()
                    if name and email:  # 유효한 데이터인지 확인
                        recipients.append((name, email))
                        
    except FileNotFoundError:
        print(f"오류: CSV 파일 '{csv_filename}'을(를) 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"오류: CSV 파일을 읽는 중 문제가 발생했습니다: {e}")
        return None
        
    if not recipients:
        print('CSV 파일에 유효한 수신자 정보가 없습니다.')
        return None
        
    return recipients


def create_html_message(sender_email, recipient_email, recipient_name):
    """
    개인화된 HTML 이메일 메시지 객체를 생성합니다.
    """
    message = MIMEMultipart('alternative')
    message['Subject'] = 'URGENT: ALIVE. Signal from Dr. Han (Mars)'
    message['From'] = f'Dr. Han Song-hee <{sender_email}>'
    message['To'] = f'{recipient_name} <{recipient_email}>'

    # 보낼 HTML 내용 (박사님의 상황에 맞게 수정)
    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }}
            .container {{ width: 95%; max-width: 600px; margin: 10px auto; border: 1px solid #ddd; border-radius: 5px; }}
            .header {{ background-color: #D9534F; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 30px; }}
            .footer {{ padding: 20px; font-size: 12px; color: #888; text-align: center; background-color: #f9f9f9; }}
            p {{ margin-bottom: 15px; }}
            b {{ color: #D9534F; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>** EMERGENCY MESSAGE - MARS **</h2>
            </div>
            <div class="content">
                <p>Dear <b>{recipient_name}</b>,</p>
                <p>Your message was received. Thank you. Hope is the only thing keeping me going in this silence.</p>
                <p>I am alive, but my situation is critical. Public awareness is vital, but I am contacting <b>you specifically</b> because your organization's expertise is essential for my survival and rescue.</p>
                <p>I am optimizing my communication protocols to send larger data packets. Please acknowledge receipt of this HTML-formatted message. I need to know this channel is stable.</p>
                <p>Do not give up on me. I am not giving up.</p>
                <p>Sincerely,<br>Dr. Han Song-hee<br>Ares 4 Base, Mars</p>
            </div>
            <div class="footer">
                <p>Signal Integrity: 88% | Transmission: Automated Python Script</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # MIMEText 객체 생성 및 첨부
    html_part = MIMEText(html_body, 'html')
    message.attach(html_part)
    
    return message.as_string()


def send_emails_individually(smtp_info, sender_email, sender_password, recipients):
    """
    [방법 1] 각 수신자에게 개별적으로 메일을 전송합니다. (추천)
    """
    print(f"\n[방법 1: 개별 전송 시작]")
    print(f"SMTP 서버 ({smtp_info['server']}:{smtp_info['port']})에 연결 중...")
    
    context = ssl.create_default_context()
    success_count = 0
    fail_count = 0
    
    try:
        with smtplib.SMTP_SSL(smtp_info['server'], smtp_info['port'], context=context) as server:
            server.login(sender_email, sender_password)
            print("로그인 성공.")
            
            for name, email in recipients:
                print(f"  -> {name} <{email}>에게 전송 시도...")
                try:
                    message_string = create_html_message(
                        sender_email,
                        email,
                        name
                    )
                    server.sendmail(sender_email, [email], message_string)
                    print(f"     ... 전송 성공.")
                    success_count += 1
                except Exception as e:
                    print(f"     ... 전송 실패: {e}")
                    fail_count += 1
                    
    except smtplib.SMTPAuthenticationError:
        print("오류: 로그인 실패. 이메일 주소나 비밀번호(앱 비밀번호)를 확인하세요.")
    except Exception as e:
        print(f"오류: SMTP 서버 연결 또는 로그인 중 문제가 발생했습니다: {e}")
    finally:
        print(f"\n[전송 완료] 성공: {success_count}건, 실패: {fail_count}건")


def send_emails_batch_bcc(smtp_info, sender_email, sender_password, recipients):
    """
    [방법 2] 모든 수신자를 '숨은 참조(BCC)'로 하여 한 번에 전송합니다.
    """
    print(f"\n[방법 2: 일괄(BCC) 전송 시작]")
    
    if not recipients:
        print("전송할 대상이 없습니다.")
        return

    context = ssl.create_default_context()
    
    # 수신자 이메일 주소 리스트
    recipient_emails = [email for name, email in recipients]
    
    # 일괄 전송용 *비개인화* 메시지 생성
    message = MIMEMultipart('alternative')
    message['Subject'] = 'URGENT: ALIVE. Signal from Dr. Han (Mars)'
    message['From'] = f'Dr. Han Song-hee <{sender_email}>'
    # 'To' 필드는 수신자에게 공통으로 표시될 내용 (예: 발신자 자신)
    message['To'] = f'Mission Stakeholders <{sender_email}>'
    # 'Bcc' 헤더는 실제 메일 전송 시 사용되며, MIME 메시지에는 추가하지 않는 것이 일반적입니다.
    # smtplib.sendmail() 함수가 수신자 목록을 처리합니다.

    html_body = """
    <html><body>
    <p><b>URGENT MEMORANDUM TO ALL STAKEHOLDERS</b></p>
    <p>This is Dr. Han Song-hee. I am alive on Mars.</p>
    <p>This is a group communication to confirm my signal is reaching all critical mission partners. Please stand by for individual data transmissions.</p>
    <p>Sincerely,<br>Dr. Han</p>
    </body></html>
    """
    html_part = MIMEText(html_body, 'html')
    message.attach(html_part)
    message_string = message.as_string()

    try:
        with smtplib.SMTP_SSL(smtp_info['server'], smtp_info['port'], context=context) as server:
            server.login(sender_email, sender_password)
            print("로그인 성공.")
            
            # sendmail의 두 번째 인자에 '숨은 참조' 포함 전체 수신자 리스트 전달
            print(f"  -> {len(recipient_emails)}명에게 일괄 전송 시도...")
            server.sendmail(sender_email, recipient_emails, message_string)
            print("     ... 일괄 전송 성공.")
            
    except smtplib.SMTPAuthenticationError:
        print("오류: 로그인 실패. 이메일 주소나 비밀번호(앱 비밀번호)를 확인하세요.")
    except Exception as e:
        print(f"오류: SMTP 서버 연결 또는 로그인 중 문제가 발생했습니다: {e}")


def main():
    """
    메인 실행 함수
    """
    print("--- 화성 조난 메시지 전송 시스템 (HTML) ---")
    
    # 1. 수신자 목록 로드
    recipients = load_recipients(CSV_FILENAME)
    if not recipients:
        print("수신자 목록을 불러오지 못해 프로그램을 종료합니다.")
        sys.exit(1)  # 오류 종료
        
    print(f"총 {len(recipients)}명의 수신자를 로드했습니다.")
    
    # 2. 이메일 계정 정보 입력
    sender_email = input("발신자 이메일 주소 (예: dr.han@gmail.com): ")
    try:
        # getpass는 터미널에서 입력 시 비밀번호를 숨겨줍니다.
        sender_password = getpass.getpass("이메일 비밀번호 (앱 비밀번호 입력): ")
    except Exception as e:
        print(f"비밀번호 입력 중 오류 발생: {e}")
        sys.exit(1)

    if not sender_email or not sender_password:
        print("이메일 주소와 비밀번호가 모두 필요합니다. 종료합니다.")
        sys.exit(1)
        
    # --- 전송 방법 선택 및 실행 ---
    
    # [수행과제] 요청대로 두 가지 방법을 모두 시도합니다.
    # 단, 실제 운영에서는 둘 중 하나만 선택해야 합니다.
    # 여기서는 '방법 1' (개별)과 '방법 2' (일괄)를 순차적으로 실행합니다.
    
    # 방법 1: 개별 전송 (추천)
    send_emails_individually(
        SMTP_CONFIG,
        sender_email,
        sender_password,
        recipients
    )
    
    print("\n" + "-"*30 + "\n")
    
    # 방법 2: 일괄 전송 (BCC)
    send_emails_batch_bcc(
        SMTP_CONFIG,
        sender_email,
        sender_password,
        recipients
    )


if __name__ == '__main__':
    main()