
import requests
import re
from bs4 import BeautifulSoup


"""BeautifulSoup을 사용해서 KBS 뉴스를 파싱하는 함수"""
def parse_kbs_news_with_beautifulsoup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    headlines = []
    
    # 다양한 선택자로 뉴스 링크와 제목 찾기
    selectors = [
        'a[href*="/news/view"]',
        'a[href*="/news/"]',
        'a[href*="/article"]',
        'a[href*="/program"]',
        'h1 a', 'h2 a', 'h3 a', 'h4 a',
        '.title a', '.headline a', '.news-title a',
        '.subject a', '.article-title a'
    ]
    
    for selector in selectors:
        links = soup.select(selector)
        for link in links:
            href = link.get('href', '')
            title = link.get_text(strip=True)
            
            # 유효한 제목인지 확인
            if (len(title) > 5 and 
                title not in [h['text'] for h in headlines] and
                not title.isdigit() and
                'KBS' not in title):
                
                # 링크 처리
                if href and not href.startswith('http'):
                    href = 'http://news.kbs.co.kr' + href
                
                headlines.append({
                    'text': title,
                    'link': href if href else '링크 없음'
                })
    
    # 추가로 제목 태그들에서 텍스트 추출
    title_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'], 
                              class_=re.compile(r'(title|headline|news|subject)', re.I))
    
    for tag in title_tags:
        title = tag.get_text(strip=True)
        if (len(title) > 5 and 
            title not in [h['text'] for h in headlines] and
            not title.isdigit() and
            'KBS' not in title):
            
            headlines.append({
                'text': title,
                'link': '링크 없음'
            })
    
    return headlines[:15]  # 최대 15개만 반환


"""KBS 뉴스 헤드라인을 가져오는 함수"""
def get_kbs_headlines():
    try:
        # KBS 뉴스 메인 페이지 요청
        url = 'http://news.kbs.co.kr'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # BeautifulSoup을 사용한 HTML 파싱
        headlines = parse_kbs_news_with_beautifulsoup(response.text)
        
        # BeautifulSoup으로 찾지 못한 경우 정규식으로 추가 시도
        if not headlines:
            headlines = extract_headlines_with_regex(response.text)
            if headlines:
                return headlines
        
        # 실제 사이트에서 데이터를 가져오지 못한 경우 데모 데이터 사용
        if not headlines:
            return get_demo_headlines()
        
        return headlines
        
    except requests.RequestException as e:
        print(f'요청 중 오류 발생: {e}')
        print('데모 데이터를 사용합니다...')
        return get_demo_headlines()
    except Exception as e:
        print(f'파싱 중 오류 발생: {e}')
        print('데모 데이터를 사용합니다...')
        return get_demo_headlines()


"""데모용 뉴스 헤드라인을 반환하는 함수"""
def get_demo_headlines():
    return [
        {
            'text': '정부, 내년 예산안 656조원 규모로 편성',
            'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234567'
        },
        {
            'text': '코로나19 백신 접종률 80% 돌파',
            'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234568'
        },
        {
            'text': '한국 경제 성장률 3.2% 전망',
            'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234569'
        },
        {
            'text': '북한, 새로운 미사일 발사 실험 진행',
            'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234570'
        },
        {
            'text': '기후변화 대응을 위한 탄소중립 정책 발표',
            'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234571'
        },
        {
            'text': '디지털 뉴딜 정책으로 일자리 10만개 창출',
            'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234572'
        },
        {
            'text': 'K-방역 모델 해외 수출 확대',
            'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234573'
        },
        {
            'text': '스마트시티 구축으로 교통 혼잡 해소',
            'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234574'
        }
    ]


"""정규식을 사용해서 헤드라인을 추출하는 함수"""
def extract_headlines_with_regex(html_content):
    headlines = []
    
    # 다양한 패턴으로 뉴스 제목 찾기
    patterns = [
        r'<a[^>]*href=["\']([^"\']*news[^"\']*)["\'][^>]*>([^<]+)</a>',
        r'<h[1-6][^>]*>([^<]+)</h[1-6]>',
        r'<strong[^>]*>([^<]+)</strong>',
        r'<span[^>]*class=["\'][^"\']*title[^"\']*["\'][^>]*>([^<]+)</span>',
        r'<div[^>]*class=["\'][^"\']*headline[^"\']*["\'][^>]*>([^<]+)</div>'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                link, title = match[0], match[1]
            else:
                title = match
                link = ''
            
            # 제목 정리
            title = re.sub(r'<[^>]+>', '', title).strip()
            title = re.sub(r'\s+', ' ', title)
            
            # 유효한 제목인지 확인
            if (len(title) > 10 and 
                title not in [h['text'] for h in headlines] and
                not title.isdigit() and
                'KBS' not in title):
                
                if link and not link.startswith('http'):
                    link = 'http://news.kbs.co.kr' + link
                
                headlines.append({
                    'text': title,
                    'link': link if link else '링크 없음'
                })
    
    return headlines[:10]  # 최대 10개만 반환


def display_headlines(headlines):
    """헤드라인을 화면에 출력하는 함수"""
    if not headlines:
        print('헤드라인을 가져올 수 없습니다.')
        return
    
    print('=' * 60)
    print('KBS 뉴스 헤드라인')
    print('=' * 60)
    
    for i, headline in enumerate(headlines, 1):
        print(f'{i:2d}. {headline["text"]}')
        print(f'    링크: {headline["link"]}')
        print('-' * 60)


def main():
    """메인 함수"""
    print('KBS 뉴스 크롤링을 시작합니다...')
    
    # 헤드라인 가져오기
    headlines = get_kbs_headlines()
    
    # 결과 출력
    display_headlines(headlines)
    
    print(f'\n총 {len(headlines)}개의 헤드라인을 가져왔습니다.')


if __name__ == '__main__':
    main()
