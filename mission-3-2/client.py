'''
채팅 서버 테스트용 클라이언트
'''

import socket
import threading
import configparser
import sys

config = configparser.ConfigParser()
config.read('./mission-3-2/config.ini', encoding='utf-8')

host = config['server']['host']
port = int(config['server']['port'])

class ChatClient:
    
    def __init__(self, host=host, port=port):
        self.host = host
        self.port = port
        self.socket = None
        self.nickname = None
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            # 닉네임 입력
            self.nickname = input('닉네임을 입력하세요: ')
            self.socket.send(self.nickname.encode('utf-8'))
            
            # 메시지 수신 쓰레드 시작
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # 메시지 전송
            self.send_messages()
            
        except Exception as e:
            print(f'연결 오류: {e}')
            sys.exit(1)
    
    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                print(message)
            except Exception as e:
                print(f'메시지 수신 오류: {e}')
                break
    
    def send_messages(self):
        while True:
            try:
                message = input()
                if message == '/종료':
                    self.socket.send(message.encode('utf-8'))
                    break
                else:
                    self.socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f'메시지 전송 오류: {e}')
                break
        
        self.socket.close()
        print('연결이 종료되었습니다.')


def main():
    try:
        client = ChatClient()
        client.connect()
    except KeyboardInterrupt:
        print('\n클라이언트를 종료합니다...')
        sys.exit(0)
    except Exception as e:
        print(f'프로그램 실행 오류: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
