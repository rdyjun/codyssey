#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 로그인 크롤링 스크립트
셀레니움을 사용하여 네이버에 로그인하고 로그인 후에만 보이는 콘텐츠를 크롤링합니다.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class NaverCrawler:
    """네이버 크롤링을 위한 클래스"""
    
    def __init__(self):
        """크롤러 초기화"""
        self.driver = None
        self.wait = None
        self.login_content_list = []
        
    def setup_driver(self):
        """셀레니움 드라이버 설정"""
        try:
            # Chrome 옵션 설정
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 드라이버 생성 (수동 설치된 ChromeDriver 사용)
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            chromedriver_path = os.path.join(script_dir, 'chromedriver-mac-arm64', 'chromedriver')
            service = Service(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 대기 객체 생성
            self.wait = WebDriverWait(self.driver, 10)
            
            print('드라이버 설정 완료')
            return True
            
        except Exception as e:
            print(f'드라이버 설정 실패: {e}')
            return False
    
    def login_to_naver(self, user_id, user_pw):
        """네이버 로그인"""
        try:
            # 네이버 로그인 페이지로 이동
            self.driver.get('https://nid.naver.com/nidlogin.login')
            time.sleep(2)
            
            # 아이디 입력
            id_input = self.wait.until(
                EC.presence_of_element_located((By.ID, 'id'))
            )
            id_input.clear()
            id_input.send_keys(user_id)
            
            # 비밀번호 입력
            pw_input = self.driver.find_element(By.ID, 'pw')
            pw_input.clear()
            pw_input.send_keys(user_pw)
            
            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.ID, 'log.login')
            login_button.click()
            
            # 로그인 완료 대기
            time.sleep(3)
            
            # 로그인 성공 확인
            if 'naver.com' in self.driver.current_url:
                print('네이버 로그인 성공')
                return True
            else:
                print('네이버 로그인 실패')
                return False
                
        except Exception as e:
            print(f'로그인 중 오류 발생: {e}')
            return False
    
    def get_login_content(self):
        """로그인 후에만 보이는 콘텐츠 크롤링"""
        try:
            # 네이버 메인 페이지로 이동
            self.driver.get('https://www.naver.com')
            time.sleep(3)
            
            # 페이지 소스 가져오기
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 로그인 후에만 보이는 콘텐츠들 수집
            content_list = []
            
            # 1. 로그인 상태 확인 (로그인 버튼이 없으면 로그인된 상태)
            login_button = soup.find('a', string=lambda x: x and '로그인' in x)
            if not login_button:
                content_list.append('로그인 상태: 로그인됨')
            else:
                content_list.append('로그인 상태: 비로그인')
            
            # 2. 검색 영역 정보 (로그인 후 개인화됨)
            search_area = soup.find('div', class_='search_area')
            if search_area:
                search_text = search_area.get_text().strip()
                if search_text:
                    content_list.append(f'검색 영역: {search_text[:100]}')
            
            # 3. 메뉴 영역 정보
            menu_area = soup.find('div', class_='menu_area')
            if menu_area:
                menu_text = menu_area.get_text().strip()
                if menu_text:
                    content_list.append(f'메뉴 영역: {menu_text[:100]}')
            
            # 4. 알림 영역 (로그인 후에만 보임)
            notify_area = soup.find('div', class_='notify_area')
            if notify_area:
                notify_text = notify_area.get_text().strip()
                if notify_text:
                    content_list.append(f'알림 영역: {notify_text[:100]}')
            
            # 5. 결제 영역 (로그인 후에만 보임)
            pay_area = soup.find('div', class_='pay_area')
            if pay_area:
                pay_text = pay_area.get_text().strip()
                if pay_text:
                    content_list.append(f'결제 영역: {pay_text[:100]}')
            
            # 6. 광고 영역 (로그인 후 개인화됨)
            ad_area = soup.find('div', class_='ad_area')
            if ad_area:
                ad_text = ad_area.get_text().strip()
                if ad_text:
                    content_list.append(f'광고 영역: {ad_text[:100]}')
            
            # 7. 프리미엄 광고 영역 (로그인 후 개인화됨)
            ad_premium_area = soup.find('div', class_='ad_premium_area')
            if ad_premium_area:
                premium_text = ad_premium_area.get_text().strip()
                if premium_text:
                    content_list.append(f'프리미엄 광고: {premium_text[:100]}')
            
            # 8. 페이지의 모든 텍스트에서 로그인 관련 키워드 찾기
            page_text = soup.get_text()
            login_keywords = ['마이페이지', '로그아웃', '내정보', '설정', '알림']
            for keyword in login_keywords:
                if keyword in page_text:
                    content_list.append(f'로그인 후 키워드 발견: {keyword}')
            
            # 9. 개인화된 콘텐츠가 있을 수 있는 영역들
            personalized_areas = soup.find_all(['div', 'section'], class_=lambda x: x and any(
                word in x.lower() for word in ['personal', 'my', 'user', 'custom', 'recommend']
            ))
            for i, area in enumerate(personalized_areas[:3]):
                if area:  # None 체크 추가
                    area_text = area.get_text().strip()
                    if area_text and len(area_text) > 10:
                        content_list.append(f'개인화 영역 {i+1}: {area_text[:100]}')
            
            self.login_content_list = content_list
            print(f'로그인 후 콘텐츠 {len(content_list)}개 수집 완료')
            return content_list
            
        except Exception as e:
            print(f'콘텐츠 크롤링 중 오류 발생: {e}')
            return []
    
    def get_non_login_content(self):
        """로그인 전 콘텐츠 크롤링 (비교용)"""
        try:
            # 로그아웃 상태로 네이버 메인 페이지 접속
            self.driver.get('https://www.naver.com')
            time.sleep(2)
            
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 로그인 전에 보이는 기본 콘텐츠들
            non_login_content = []
            
            # 1. 로그인 상태 확인
            login_button = soup.find('a', string=lambda x: x and '로그인' in x)
            if login_button:
                non_login_content.append('로그인 상태: 비로그인 (로그인 버튼 존재)')
            else:
                non_login_content.append('로그인 상태: 로그인됨 (로그인 버튼 없음)')
            
            # 2. 기본 검색 영역
            search_area = soup.find('div', class_='search_area')
            if search_area:
                search_text = search_area.get_text().strip()
                if search_text:
                    non_login_content.append(f'기본 검색 영역: {search_text[:100]}')
            
            # 3. 기본 메뉴 영역
            menu_area = soup.find('div', class_='menu_area')
            if menu_area:
                menu_text = menu_area.get_text().strip()
                if menu_text:
                    non_login_content.append(f'기본 메뉴 영역: {menu_text[:100]}')
            
            # 4. 기본 광고 영역
            ad_area = soup.find('div', class_='ad_area')
            if ad_area:
                ad_text = ad_area.get_text().strip()
                if ad_text:
                    non_login_content.append(f'기본 광고 영역: {ad_text[:100]}')
            
            # 5. 페이지의 기본 구조 정보
            page_text = soup.get_text()
            basic_keywords = ['검색', '뉴스', '웹툰', '쇼핑', '지도']
            for keyword in basic_keywords:
                if keyword in page_text:
                    non_login_content.append(f'기본 키워드 발견: {keyword}')
            
            print(f'로그인 전 콘텐츠 {len(non_login_content)}개 수집 완료')
            return non_login_content
            
        except Exception as e:
            print(f'비로그인 콘텐츠 크롤링 중 오류 발생: {e}')
            return []
    
    def display_content_difference(self, login_content, non_login_content):
        """로그인 전후 콘텐츠 차이점 출력"""
        print('\n=== 로그인 전후 콘텐츠 차이점 ===')
        print('\n[로그인 전 콘텐츠]')
        for i, content in enumerate(non_login_content, 1):
            print(f'{i}. {content}')
        
        print('\n[로그인 후 콘텐츠]')
        for i, content in enumerate(login_content, 1):
            print(f'{i}. {content}')
        
        print(f'\n로그인 전: {len(non_login_content)}개 항목')
        print(f'로그인 후: {len(login_content)}개 항목')
        print(f'차이점: {len(login_content) - len(non_login_content)}개 추가 콘텐츠')
    
    def close_driver(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            print('드라이버 종료 완료')


def main():
    """메인 함수"""
    print('=== 네이버 로그인 크롤링 시작 ===')
    
    # 크롤러 인스턴스 생성
    crawler = NaverCrawler()
    
    try:
        # 드라이버 설정
        if not crawler.setup_driver():
            return
        
        # 사용자 입력 받기 (실제 사용시에는 입력받아야 함)
        print('\n주의: 실제 사용시에는 아래 정보를 입력받아야 합니다.')
        print('테스트용으로 더미 데이터를 사용합니다.')
        
        # 테스트용 더미 데이터 (실제 사용시에는 input()으로 받아야 함)
        test_user_id = input('네이버 아이디를 입력하세요: ')  # 실제 사용시: input('네이버 아이디를 입력하세요: ')
        test_user_pw = input('네이버 비밀번호를 입력하세요: ')  # 실제 사용시: input('네이버 비밀번호를 입력하세요: ')
        
        # 로그인 전 콘텐츠 수집
        print('\n1. 로그인 전 콘텐츠 수집 중...')
        non_login_content = crawler.get_non_login_content()
        
        # 네이버 로그인
        print('\n2. 네이버 로그인 시도 중...')
        if crawler.login_to_naver(test_user_id, test_user_pw):
            # 로그인 후 콘텐츠 수집
            print('\n3. 로그인 후 콘텐츠 수집 중...')
            login_content = crawler.get_login_content()
            
            # 콘텐츠 차이점 출력
            crawler.display_content_difference(login_content, non_login_content)
            
            # 최종 결과를 리스트로 출력
            print('\n=== 최종 크롤링 결과 ===')
            print('로그인 후 수집된 콘텐츠 리스트:')
            for i, content in enumerate(crawler.login_content_list, 1):
                print(f'{i}. {content}')
        else:
            print('로그인에 실패하여 로그인 후 콘텐츠를 수집할 수 없습니다.')
            print('실제 네이버 계정 정보를 입력하여 다시 시도해주세요.')
    
    except Exception as e:
        print(f'프로그램 실행 중 오류 발생: {e}')
    
    finally:
        # 드라이버 종료
        crawler.close_driver()
        print('\n=== 네이버 로그인 크롤링 종료 ===')


if __name__ == '__main__':
    main()
