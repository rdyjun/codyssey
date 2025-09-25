from crawling_KBS import get_kbs_headlines, display_headlines
from weather_crawler import get_weather_info, display_weather_info
from stock_crawler import get_stock_info, display_stock_info


"""KBS, 날씨, 주가 모두 크롤링하는 메인 함수"""
def main():
    print('=' * 60)
    print('통합 정보 크롤링 프로그램')
    print('=' * 60)
    
    # 1. 뉴스 정보
    print('\n1. KBS 뉴스 헤드라인')
    print('-' * 40)
    headlines = get_kbs_headlines()
    display_headlines(headlines)
    
    # 2. 날씨 정보
    print('\n2. 날씨 정보')
    print('-' * 40)
    weather_data = get_weather_info()
    display_weather_info(weather_data)
    
    # 3. 주식 정보
    print('\n3. 주식 정보')
    print('-' * 40)
    stocks = get_stock_info()
    display_stock_info(stocks)
    
    print('\n' + '=' * 60)
    print('모든 정보 수집이 완료되었습니다!')
    print('=' * 60)


if __name__ == '__main__':
    main()
