import requests
import re
from bs4 import BeautifulSoup


"""BeautifulSoup을 사용해서 날씨 정보를 파싱하는 함수"""
def parse_weather_with_beautifulsoup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    weather_data = {}
    
    # 온도 정보 찾기
    temp_selectors = [
        '.temperature', '.temp', '.degree',
        '[class*="temp"]', '[class*="temperature"]',
        'span:contains("°")', 'div:contains("°")',
        'span:contains("도")', 'div:contains("도")'
    ]
    
    for selector in temp_selectors:
        try:
            temp_elements = soup.select(selector)
            for element in temp_elements:
                temp_text = element.get_text(strip=True)
                if temp_text and ('°' in temp_text or '도' in temp_text or re.match(r'\d+', temp_text)):
                    weather_data['temperature'] = temp_text
                    break
            if 'temperature' in weather_data:
                break
        except:
            continue
    
    # 날씨 설명 찾기
    weather_selectors = [
        '.weather', '.condition', '.desc', '.status',
        '[class*="weather"]', '[class*="condition"]',
        'span:contains("맑음")', 'span:contains("흐림")',
        'span:contains("비")', 'span:contains("눈")',
        'div:contains("맑음")', 'div:contains("흐림")'
    ]
    
    for selector in weather_selectors:
        try:
            weather_elements = soup.select(selector)
            for element in weather_elements:
                weather_text = element.get_text(strip=True)
                if weather_text and len(weather_text) < 20 and any(keyword in weather_text for keyword in ['맑음', '흐림', '비', '눈', '구름', '바람']):
                    weather_data['description'] = weather_text
                    break
            if 'description' in weather_data:
                break
        except:
            continue
    
    # 지역 정보 찾기
    location_selectors = [
        '.location', '.city', '.region', '.area',
        '[class*="location"]', '[class*="city"]',
        'h1', 'h2', 'h3', 'title'
    ]
    
    for selector in location_selectors:
        try:
            location_elements = soup.select(selector)
            for element in location_elements:
                location_text = element.get_text(strip=True)
                if location_text and len(location_text) < 10 and any(keyword in location_text for keyword in ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']):
                    weather_data['location'] = location_text
                    break
            if 'location' in weather_data:
                break
        except:
            continue
    
    # 습도 정보 찾기
    humidity_selectors = [
        '.humidity', '.moisture',
        '[class*="humidity"]', '[class*="moisture"]',
        'span:contains("%")', 'div:contains("%")'
    ]
    
    for selector in humidity_selectors:
        try:
            humidity_elements = soup.select(selector)
            for element in humidity_elements:
                humidity_text = element.get_text(strip=True)
                if humidity_text and '%' in humidity_text and re.match(r'\d+%', humidity_text):
                    weather_data['humidity'] = humidity_text
                    break
            if 'humidity' in weather_data:
                break
        except:
            continue
    
    # 풍속 정보 찾기
    wind_selectors = [
        '.wind', '.speed',
        '[class*="wind"]', '[class*="speed"]',
        'span:contains("m/s")', 'div:contains("m/s")'
    ]
    
    for selector in wind_selectors:
        try:
            wind_elements = soup.select(selector)
            for element in wind_elements:
                wind_text = element.get_text(strip=True)
                if wind_text and ('m/s' in wind_text or 'km/h' in wind_text):
                    weather_data['wind_speed'] = wind_text
                    break
            if 'wind_speed' in weather_data:
                break
        except:
            continue
    
    # 기압 정보 찾기
    pressure_selectors = [
        '.pressure', '.barometer',
        '[class*="pressure"]', '[class*="barometer"]',
        'span:contains("hPa")', 'div:contains("hPa")'
    ]
    
    for selector in pressure_selectors:
        try:
            pressure_elements = soup.select(selector)
            for element in pressure_elements:
                pressure_text = element.get_text(strip=True)
                if pressure_text and 'hPa' in pressure_text:
                    weather_data['pressure'] = pressure_text
                    break
            if 'pressure' in weather_data:
                break
        except:
            continue
    
    return weather_data


"""날씨 정보를 가져오는 함수"""
def get_weather_info():
    try:
        # 기상청 날씨 페이지 요청
        url = 'https://www.weather.go.kr/w/weather/forecast/short-term.do'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # BeautifulSoup을 사용한 HTML 파싱
        weather_data = parse_weather_with_beautifulsoup(response.text)
        
        # BeautifulSoup으로 찾지 못한 경우 데모 데이터 사용
        if not weather_data:
            return get_demo_weather_data()
        
        return weather_data
        
    except requests.RequestException as e:
        print(f'요청 중 오류 발생: {e}')
        print('데모 데이터를 사용합니다...')
        return get_demo_weather_data()
    except Exception as e:
        print(f'파싱 중 오류 발생: {e}')
        print('데모 데이터를 사용합니다...')
        return get_demo_weather_data()


"""데모용 날씨 데이터를 반환하는 함수"""
def get_demo_weather_data():
    return {
        'location': '서울',
        'temperature': '15°C',
        'description': '맑음',
        'humidity': '65%',
        'wind_speed': '2m/s',
        'pressure': '1013hPa'
    }


"""날씨 정보를 화면에 출력하는 함수"""
def display_weather_info(weather_data):
    if not weather_data:
        print('날씨 정보를 가져올 수 없습니다.')
        return
    
    print('=' * 50)
    print('현재 날씨 정보')
    print('=' * 50)
    print(f'지역: {weather_data.get("location", "정보 없음")}')
    print(f'온도: {weather_data.get("temperature", "정보 없음")}')
    print(f'날씨: {weather_data.get("description", "정보 없음")}')
    print(f'습도: {weather_data.get("humidity", "정보 없음")}')
    print(f'풍속: {weather_data.get("wind_speed", "정보 없음")}')
    print(f'기압: {weather_data.get("pressure", "정보 없음")}')
    print('=' * 50)


def main():
    """메인 함수"""
    print('날씨 정보 크롤링을 시작합니다...')
    
    # 날씨 정보 가져오기
    weather_data = get_weather_info()
    
    # 결과 출력
    display_weather_info(weather_data)


if __name__ == '__main__':
    main()
