#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 페이지 구조 디버깅 스크립트
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def debug_naver_structure():
    """네이버 페이지 구조 디버깅"""
    try:
        # Chrome 옵션 설정
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 드라이버 생성
        service = Service('./chromedriver-mac-arm64/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print('네이버 메인 페이지 접속 중...')
        driver.get('https://www.naver.com')
        time.sleep(3)
        
        # 페이지 소스 가져오기
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        print('\n=== 네이버 페이지 구조 분석 ===')
        
        # 1. 사용자 정보 관련 요소들 찾기
        print('\n1. 사용자 정보 관련 요소들:')
        user_elements = soup.find_all(['div', 'span', 'a'], class_=lambda x: x and ('user' in x.lower() or 'login' in x.lower() or 'my' in x.lower()))
        for elem in user_elements[:5]:
            print(f'  - {elem.name}.{elem.get("class", [])}: {elem.get_text().strip()[:50]}')
        
        # 2. 뉴스 관련 요소들 찾기
        print('\n2. 뉴스 관련 요소들:')
        news_elements = soup.find_all(['div', 'li', 'a'], class_=lambda x: x and ('news' in x.lower() or 'article' in x.lower()))
        for elem in news_elements[:5]:
            print(f'  - {elem.name}.{elem.get("class", [])}: {elem.get_text().strip()[:50]}')
        
        # 3. 서비스 메뉴 관련 요소들 찾기
        print('\n3. 서비스 메뉴 관련 요소들:')
        service_elements = soup.find_all(['div', 'a'], class_=lambda x: x and ('service' in x.lower() or 'menu' in x.lower()))
        for elem in service_elements[:5]:
            print(f'  - {elem.name}.{elem.get("class", [])}: {elem.get_text().strip()[:50]}')
        
        # 4. 검색 관련 요소들 찾기
        print('\n4. 검색 관련 요소들:')
        search_elements = soup.find_all(['div', 'li', 'a'], class_=lambda x: x and ('search' in x.lower() or 'suggest' in x.lower()))
        for elem in search_elements[:5]:
            print(f'  - {elem.name}.{elem.get("class", [])}: {elem.get_text().strip()[:50]}')
        
        # 5. 모든 클래스명 출력 (일부)
        print('\n5. 페이지의 주요 클래스명들:')
        all_classes = set()
        for elem in soup.find_all(class_=True):
            if isinstance(elem.get('class'), list):
                all_classes.update(elem.get('class'))
        
        for class_name in sorted(list(all_classes))[:20]:  # 상위 20개만
            print(f'  - {class_name}')
        
        # 6. 로그인 상태 확인
        print('\n6. 로그인 상태 확인:')
        if '로그인' in page_source:
            print('  - 로그인 버튼이 보입니다 (비로그인 상태)')
        else:
            print('  - 로그인 버튼이 보이지 않습니다 (로그인 상태일 수 있음)')
        
        driver.quit()
        print('\n디버깅 완료!')
        
    except Exception as e:
        print(f'디버깅 중 오류 발생: {e}')

if __name__ == '__main__':
    debug_naver_structure()
