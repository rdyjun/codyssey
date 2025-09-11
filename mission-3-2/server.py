'''
멀티쓰레드 TCP/IP 소켓 서버
여러 클라이언트와 동시에 통신할 수 있는 채팅 서버
'''

import socket
import threading
import configparser
import sys

config = configparser.ConfigParser()
config.read('./mission-3-2/config.ini', encoding='utf-8')

host = config['server']['host']
port = int(config['server']['port'])

'''멀티쓰레드 채팅 서버 클래스'''
class ChatServer:
    
    def __init__(self, host=host, port=port):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.server_socket = None
        
    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 재실행 시 주소 및 포트가 재사용중이라고 뜨는 오류 예방(1이 활성화)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            
            print(f'서버가 {self.host}:{self.port}에서 시작되었습니다.')
            print('클라이언트 연결을 기다리는 중...')
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f'{address}에서 연결되었습니다.')
                
                # 클라이언트를 위한 쓰레드 생성
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            print('\n서버를 종료합니다...')
            self.shutdown_server()
        except Exception as e:
            print(f'서버 오류: {e}')
            self.shutdown_server()
    
    def handle_client(self, client_socket, address):
        try:
            # 닉네임 요청 및 수신
            nickname = client_socket.recv(1024).decode('utf-8').strip()
            
            # 닉네임 중복 확인
            while nickname in self.nicknames:
                client_socket.send('이미 사용 중인 닉네임입니다. 다른 닉네임을 입력하세요: '.encode('utf-8'))
                nickname = client_socket.recv(  ).decode('utf-8').strip()
            
            # 클라이언트 정보 저장
            self.clients.append(client_socket)
            self.nicknames.append(nickname)
            
            # 입장 메시지 전송
            self.broadcast_message(f'{nickname}님이 입장하셨습니다.', client_socket)
            print(f'{nickname}님이 입장했습니다. (총 {len(self.clients)}명)')
            
            # 클라이언트로부터 메시지 수신 및 처리
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    
                    if message == '/종료':
                        self.remove_client(client_socket, nickname)
                        break
                    
                    # 메시지 브로드캐스트
                    formatted_message = f'{nickname}> {message}'
                    self.broadcast_message(formatted_message, client_socket)
                        
                except ConnectionResetError:
                    self.remove_client(client_socket, nickname)
                    break
                except Exception as e:
                    print(f'메시지 처리 오류: {e}')
                    self.remove_client(client_socket, nickname)
                    break
                    
        except Exception as e:
            print(f'클라이언트 처리 오류: {e}')
            self.remove_client(client_socket, 'Unknown')
    
    def broadcast_message(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    print(f'메시지 전송 오류: {e}')
                    self.remove_client(client, 'Unknown')
    
    def remove_client(self, client_socket, nickname):
        try:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
                self.nicknames.remove(nickname)
                
                # 퇴장 메시지 전송
                self.broadcast_message(f'{nickname}님이 퇴장하셨습니다.', None)
                print(f'{nickname}님이 퇴장했습니다. (총 {len(self.clients)}명)')
                
                client_socket.close()
        except Exception as e:
            print(f'클라이언트 제거 오류: {e}')
    
    def shutdown_server(self):
        try:
            if self.server_socket:
                self.server_socket.close()
            
            # 모든 클라이언트 연결 종료
            for client in self.clients:
                try:
                    client.close()
                except Exception:
                    pass
            
            print('서버가 종료되었습니다.')
        except Exception as e:
            print(f'서버 종료 오류: {e}')


def main():
    try:
        # 서버 생성 및 시작
        server = ChatServer()
        server.start()
    except Exception as e:
        print(f'프로그램 실행 오류: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
