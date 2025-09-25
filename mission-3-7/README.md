# Mission 3-7: 웹 크롤링 프로그램

## 프로젝트 개요

Python의 내장 모듈과 requests 라이브러리를 사용하여 웹 크롤링을 구현한 프로그램입니다. KBS 뉴스, 날씨 정보, 주식 정보를 수집하여 출력합니다.

## 파일 구조

```
mission-3-7/
├── crawling_KBS.py          # KBS 뉴스 크롤링 프로그램
├── weather_crawler.py       # 날씨 정보 크롤링 프로그램
├── stock_crawler.py         # 주식 정보 크롤링 프로그램
├── integrated_crawler.py    # 통합 크롤링 프로그램(KBS, 날씨, 주식)
└── README.md               # 프로젝트 설명서
```

## 주요 기능

### 1. KBS 뉴스 크롤링 (crawling_KBS.py)

- KBS 뉴스 사이트에서 헤드라인 뉴스 수집
- HTML 파서와 정규식을 사용한 데이터 추출
- 뉴스 제목과 링크 정보 제공

### 2. 날씨 정보 크롤링 (weather_crawler.py)

- 기상청 날씨 정보 수집
- 현재 온도, 날씨 상태, 습도 등 정보 제공
- 지역별 날씨 정보 표시

### 3. 주식 정보 크롤링 (stock_crawler.py)

- 주요 주식 정보 수집
- 주식명, 현재가, 등락률 정보 제공
- 상위 주식 정보 표시

### 4. 통합 크롤링 (integrated_crawler.py)

- 모든 크롤링 프로그램을 통합하여 실행
- 뉴스, 날씨, 주식 정보를 한 번에 수집

## 사용법

### 개별 실행

```bash
# KBS 뉴스 크롤링
python3 crawling_KBS.py

# 날씨 정보 크롤링
python3 weather_crawler.py

# 주식 정보 크롤링
python3 stock_crawler.py
```

### 통합 실행

```bash
# 모든 정보 수집
python3 integrated_crawler.py
```

## 주요 클래스 및 함수

### parse_kbs_news_with_beautifulsoup()

KBS 뉴스 HTML 파싱을 위한 함수

- BeautifulSoup을 사용한 CSS 선택자 기반 파싱
- 다양한 선택자로 뉴스 링크와 제목 추출

### parse_weather_with_beautifulsoup()

날씨 정보 HTML 파싱을 위한 함수

- 온도, 날씨 설명, 지역 정보 추출
- CSS 선택자를 통한 정확한 데이터 추출

### parse_stock_with_beautifulsoup()

주식 정보 HTML 파싱을 위한 함수

- 주식명, 가격, 변동률 정보 추출
- 테이블 구조 분석을 통한 데이터 추출

## 보너스 과제

- 날씨 정보 크롤링 (weather_crawler.py)
- 주식 정보 크롤링 (stock_crawler.py)
- 통합 크롤링 프로그램 (integrated_crawler.py)
