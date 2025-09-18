import http.server
import socketserver
import datetime
import os


class SpacePirateHandler(http.server.SimpleHTTPRequestHandler):    
    def do_GET(self):
        # 접속 정보 로깅
        self._log_access()
        
        # URL 경로 처리 (쿼리 파라미터 제거)
        path = self.path.split('?')[0]
        
        # 루트 경로인 경우 index.html로 리다이렉트
        if path == '/':
            path = 'index.html'

        # 파일 경로 생성 (실행 경로 기준)
        file_path = os.path.join(os.getcwd(), path)
        if 'mission-3-4' not in file_path:
            # mission-3-4 폴더가 경로에 없으면 추가
            file_path = os.path.join(os.getcwd(), 'mission-3-4', path)
        
        print(file_path)
        # index.html 파일이 존재하는지 확인
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self._serve_file(file_path)
        else:
            self._send_404_response()
    
    def _log_access(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        
        print(f'[{current_time}] 접속 - IP: {client_ip}')
    
    def _serve_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # HTTP 응답 헤더 설정
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.end_headers()
            
            # 응답 본문 전송
            self.wfile.write(content.encode('utf-8'))
            
        except Exception as e:
            print(f'파일 서빙 중 오류 발생: {e}')
            self._send_500_response()
    
    def _send_404_response(self):
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        error_html = '''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>404 - 페이지를 찾을 수 없습니다</title>
        </head>
        <body>
            <h1>404 - 페이지를 찾을 수 없습니다</h1>
            <p>요청하신 페이지가 존재하지 않습니다.</p>
            <a href="/">홈으로 돌아가기</a>
        </body>
        </html>
        '''
        
        self.wfile.write(error_html.encode('utf-8'))
    
    def _send_500_response(self):
        self.send_response(500)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        error_html = '''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>500 - 서버 오류</title>
        </head>
        <body>
            <h1>500 - 서버 내부 오류</h1>
            <p>서버에서 오류가 발생했습니다.</p>
            <a href="/">홈으로 돌아가기</a>
        </body>
        </html>
        '''
        
        self.wfile.write(error_html.encode('utf-8'))


def start_server(port=8888):
    try:
        with socketserver.TCPServer(("", port), SpacePirateHandler) as httpd:
            print(f'우주 해적 웹서버가 포트 {port}에서 시작되었습니다.')
            print(f'브라우저에서 http://localhost:{port} 로 접속하세요.')
            print('서버를 종료하려면 Ctrl+C를 누르세요.')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n서버가 종료되었습니다.')
    except Exception as e:
        print(f'서버 시작 중 오류 발생: {e}')


if __name__ == '__main__':
    start_server()
