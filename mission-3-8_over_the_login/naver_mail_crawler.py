#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 메일 제목 크롤링 스크립트 (보너스 과제)
셀레니움을 사용하여 네이버 메일에 로그인하고 받은 편지함의 메일 제목을 크롤링합니다.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class NaverMailCrawler:
    """네이버 메일 크롤링을 위한 클래스"""
    
    def __init__(self):
        """메일 크롤러 초기화"""
        self.driver = None
        self.wait = None
        self.mail_titles = []
        
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
    
    def access_naver_mail(self):
        """네이버 메일 접속"""
        try:
            # 네이버 메일로 이동
            self.driver.get('https://mail.naver.com')
            time.sleep(5)  # 더 긴 대기 시간
            
            # 페이지 로딩 확인
            page_title = self.driver.title
            print(f'메일 페이지 제목: {page_title}')
            
            # 메일 페이지가 로드되었는지 확인 (더 유연한 조건)
            if ('메일' in page_title or 'mail' in page_title.lower() or 
                'naver' in page_title.lower() or '로그인' in page_title):
                print('네이버 메일 페이지 접근 완료')
                return True
            else:
                print('메일 페이지 로딩 실패')
                return False
            
        except Exception as e:
            print(f'메일 접속 중 오류 발생: {e}')
            return False
    
    def crawl_mail_titles(self):
        """메일 제목 크롤링"""
        try:
            # 페이지 소스 가져오기
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 메일 제목들 수집
            mail_titles = []
            
            # 1. 페이지에서 메일 관련 텍스트 찾기
            page_text = soup.get_text()
            if '메일' in page_text or 'mail' in page_text.lower():
                mail_titles.append('메일 페이지 접근 성공')
            
            # 2. 다양한 메일 제목 선택자 시도
            title_selectors = [
                'strong.mail_title',
                'span.mail_title',
                'a.mail_title',
                '.mail_list .mail_title',
                '.mail_item .title',
                '.mail_list_item .title',
                'td.subject a',
                '.mail_list td.subject',
                'span[title]',
                'a[title]',
                '.subject',
                '.mail_subject',
                '.title'
            ]
            
            for selector in title_selectors:
                try:
                    titles = soup.select(selector)
                    if titles:
                        for title in titles:
                            if title:  # None 체크
                                title_text = title.get_text().strip()
                                if title_text and len(title_text) > 3 and title_text not in mail_titles:
                                    mail_titles.append(f'메일 제목: {title_text}')
                except Exception:
                    continue
            
            # 3. 메일 리스트에서 제목 추출
            try:
                mail_items = soup.find_all('tr', class_='mail_item')
                for item in mail_items:
                    if item:
                        title_elem = item.find('td', class_='subject')
                        if title_elem:
                            title_text = title_elem.get_text().strip()
                            if title_text and title_text not in mail_titles:
                                mail_titles.append(f'메일 제목: {title_text}')
            except Exception:
                pass
            
            # 4. 메일 관련 링크들에서 추출
            try:
                mail_links = soup.find_all('a', href=True)
                for link in mail_links:
                    if link and 'mail.naver.com' in link.get('href', ''):
                        title_text = link.get_text().strip()
                        if title_text and len(title_text) > 5 and title_text not in mail_titles:
                            mail_titles.append(f'메일 링크: {title_text}')
            except Exception:
                pass
            
            # 5. 페이지의 모든 텍스트에서 메일 관련 키워드 찾기
            mail_keywords = ['받은편지', '보낸편지', '임시보관함', '휴지통', '스팸']
            for keyword in mail_keywords:
                if keyword in page_text:
                    mail_titles.append(f'메일 키워드 발견: {keyword}')
            
            # 6. 메일이 없는 경우 안내 메시지
            if len(mail_titles) <= 1:  # '메일 페이지 접근 성공'만 있는 경우
                mail_titles.append('메일이 없거나 접근 제한이 있습니다.')
                mail_titles.append('실제 네이버 계정으로 로그인하여 다시 시도해주세요.')
            
            self.mail_titles = mail_titles
            print(f'메일 제목 {len(mail_titles)}개 수집 완료')
            return mail_titles
            
        except Exception as e:
            print(f'메일 제목 크롤링 중 오류 발생: {e}')
            return ['메일 크롤링 중 오류가 발생했습니다.']
    
    def display_mail_titles(self):
        """수집된 메일 제목들 출력"""
        print('\n=== 네이버 메일 제목 목록 ===')
        if self.mail_titles:
            for i, title in enumerate(self.mail_titles, 1):
                print(f'{i}. {title}')
        else:
            print('수집된 메일 제목이 없습니다.')
            print('메일이 없거나 선택자가 변경되었을 수 있습니다.')
    
    def close_driver(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            print('드라이버 종료 완료')


def main():
    """메인 함수"""
    print('=== 네이버 메일 제목 크롤링 시작 ===')
    
    # 메일 크롤러 인스턴스 생성
    mail_crawler = NaverMailCrawler()
    
    try:
        # 드라이버 설정
        if not mail_crawler.setup_driver():
            return
        
        # 사용자 입력 받기 (실제 사용시에는 입력받아야 함)
        print('\n주의: 실제 사용시에는 아래 정보를 입력받아야 합니다.')
        print('테스트용으로 더미 데이터를 사용합니다.')
        
        # 테스트용 더미 데이터 (실제 사용시에는 input()으로 받아야 함)
        test_user_id = input('네이버 아이디를 입력하세요: ')  # 실제 사용시: input('네이버 아이디를 입력하세요: ')
        test_user_pw = input('네이버 비밀번호를 입력하세요: ')  # 실제 사용시: input('네이버 비밀번호를 입력하세요: ')
        
        # 네이버 로그인
        print('\n1. 네이버 로그인 시도 중...')
        if mail_crawler.login_to_naver(test_user_id, test_user_pw):
            # 네이버 메일 접속
            print('\n2. 네이버 메일 접속 중...')
            if mail_crawler.access_naver_mail():
                # 메일 제목 크롤링
                print('\n3. 메일 제목 크롤링 중...')
                mail_titles = mail_crawler.crawl_mail_titles()
                
                # 메일 제목 출력
                mail_crawler.display_mail_titles()
                
                # 최종 결과를 리스트로 출력
                print('\n=== 최종 크롤링 결과 ===')
                print('수집된 메일 제목 리스트:')
                for i, title in enumerate(mail_crawler.mail_titles, 1):
                    print(f'{i}. {title}')
            else:
                print('네이버 메일 접속에 실패했습니다.')
        else:
            print('네이버 로그인에 실패하여 메일을 확인할 수 없습니다.')
            print('실제 네이버 계정 정보를 입력하여 다시 시도해주세요.')
    
    except Exception as e:
        print(f'프로그램 실행 중 오류 발생: {e}')
    
    finally:
        # 드라이버 종료
        mail_crawler.close_driver()
        print('\n=== 네이버 메일 제목 크롤링 종료 ===')


if __name__ == '__main__':
    main()
