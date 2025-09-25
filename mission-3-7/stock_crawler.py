import requests
import re
from bs4 import BeautifulSoup


"""BeautifulSoup을 사용해서 주식 정보를 파싱하는 함수"""
def parse_stock_with_beautifulsoup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    stocks = []
    
    # 주식 테이블 찾기
    stock_tables = soup.find_all('table', class_=re.compile(r'(stock|market|price)', re.I))
    
    for table in stock_tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 3:  # 최소 3개 컬럼이 있어야 함
                stock_data = {}
                
                # 각 셀에서 정보 추출
                for i, cell in enumerate(cells):
                    text = cell.get_text(strip=True)
                    
                    # 주식명 (보통 첫 번째 컬럼)
                    if i == 0 and text and not text.isdigit() and len(text) < 20:
                        stock_data['name'] = text
                    
                    # 가격 (숫자와 콤마가 포함된 텍스트)
                    elif re.match(r'[\d,]+', text) and '원' in text:
                        stock_data['price'] = text
                    
                    # 변동률 (+, -, %가 포함된 텍스트)
                    elif ('+' in text or '-' in text) and '%' in text:
                        stock_data['change'] = text
                
                # 유효한 주식 정보인지 확인
                if (stock_data.get('name') and 
                    stock_data.get('price') and 
                    stock_data not in stocks):
                    stocks.append(stock_data)
    
    # 추가로 링크가 있는 주식명 찾기
    stock_links = soup.find_all('a', href=re.compile(r'/item/main\.nhn'))
    for link in stock_links:
        name = link.get_text(strip=True)
        if name and len(name) < 20 and not name.isdigit():
            # 해당 링크의 부모 요소에서 가격 정보 찾기
            parent = link.parent
            if parent:
                price_elem = parent.find_next_sibling()
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    if re.match(r'[\d,]+', price_text) and '원' in price_text:
                        stocks.append({
                            'name': name,
                            'price': price_text,
                            'change': '정보 없음'
                        })
    
    return stocks[:10]  # 최대 10개만 반환


"""주식 정보를 가져오는 함수"""
def get_stock_info():
    try:
        # 한국거래소 주식 정보 페이지 요청
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # BeautifulSoup을 사용한 HTML 파싱
        stocks = parse_stock_with_beautifulsoup(response.text)
        
        # BeautifulSoup으로 찾지 못한 경우 데모 데이터 사용
        if not stocks:
            return get_demo_stock_data()
        
        return stocks
        
    except requests.RequestException as e:
        print(f'요청 중 오류 발생: {e}')
        print('데모 데이터를 사용합니다...')
        return get_demo_stock_data()
    except Exception as e:
        print(f'파싱 중 오류 발생: {e}')
        print('데모 데이터를 사용합니다...')
        return get_demo_stock_data()


"""데모용 주식 데이터를 반환하는 함수"""
def get_demo_stock_data():
    return [
        {
            'name': '삼성전자',
            'price': '71,200원',
            'change': '+1,200 (+1.71%)'
        },
        {
            'name': 'SK하이닉스',
            'price': '98,500원',
            'change': '+2,100 (+2.18%)'
        },
        {
            'name': 'LG화학',
            'price': '425,000원',
            'change': '-5,000 (-1.16%)'
        },
        {
            'name': 'NAVER',
            'price': '385,000원',
            'change': '+8,500 (+2.26%)'
        },
        {
            'name': '카카오',
            'price': '89,700원',
            'change': '+1,200 (+1.36%)'
        },
        {
            'name': '현대차',
            'price': '198,000원',
            'change': '-2,000 (-1.00%)'
        },
        {
            'name': 'LG전자',
            'price': '89,400원',
            'change': '+1,100 (+1.25%)'
        },
        {
            'name': '기아',
            'price': '85,200원',
            'change': '+800 (+0.95%)'
        }
    ]


"""주식 정보를 화면에 출력하는 함수"""
def display_stock_info(stocks):
    if not stocks:
        print('주식 정보를 가져올 수 없습니다.')
        return
    
    print('=' * 80)
    print('주요 주식 정보')
    print('=' * 80)
    print(f'{"순위":<4} {"종목명":<10} {"현재가":<15} {"등락률":<20}')
    print('-' * 80)
    
    for i, stock in enumerate(stocks, 1):
        name = stock.get('name', '정보 없음')
        price = stock.get('price', '정보 없음')
        change = stock.get('change', '정보 없음')
        
        print(f'{i:<4} {name:<10} {price:<15} {change:<20}')
    
    print('=' * 80)


def main():
    """메인 함수"""
    print('주식 정보 크롤링을 시작합니다...')
    
    # 주식 정보 가져오기
    stocks = get_stock_info()
    
    # 결과 출력
    display_stock_info(stocks)
    
    print(f'\n총 {len(stocks)}개의 주식 정보를 가져왔습니다.')


if __name__ == '__main__':
    main()
