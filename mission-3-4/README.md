# 우주 해적 웹서버 (Space Pirates Web Server)

## 프로젝트 개요

우주 해적단에 대한 소개 페이지이며, 접속 로그가 터미널에 노출됩니다.

## 주요 기능

- HTTP 통신을 통한 웹 페이지 서빙
- 8888 포트에서 서버 실행
- 접속 시간과 클라이언트 IP 주소 로깅
- 우주 해적단 소개 페이지 제공
- 404, 500 에러 페이지 처리

## 파일 구조

```
mission-3-4/
├── server.py          # 메인 웹서버 코드
├── index.html         # 우주 해적단 소개 페이지
└── README.md          # 프로젝트 설명서
```

## 사용법

### 1. 서버 실행

```bash
python3 mission-3-4/server.py

# or

python3 server.py
```

### 2. 브라우저에서 접속

```
http://localhost:8888
```

## 주요 클래스 및 함수

### SpacePirateHandler

웹 요청을 처리하는 핸들러 클래스

- `do_GET()`: GET 요청 처리
- `_log_access()`: 접속 정보 로깅
- `_serve_file()`: 파일 서빙
- `_send_404_response()`: 404 에러 응답
- `_send_500_response()`: 500 에러 응답

## 로그 출력 예시

```
[2025-09-18 00:37:04] 접속 - IP: 127.0.0.1
[2025-09-18 00:37:05] 접속 - IP: 127.0.0.1
```

## 요구사항 충족 사항

- [x] HTTP 통신 서버 구현 (http.server 사용)
- [x] 8080 포트 사용
- [x] 200번 응답 코드 전달
- [x] index.html 파일 작성 및 서빙
- [x] 접속 시간 및 IP 주소 로깅
