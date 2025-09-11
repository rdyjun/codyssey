import pymysql

def read_csv():
    with open('mission-12(last)/mars_weather_data.csv', 'r') as f:
        return f.read()
    
def main():
    content = read_csv()
    print(content)

    connection = DBConnector.get_connection()
    cursor = connection.cursor()

    content_by_line = content.split('\n')
    for line in content_by_line[1:]: # 헤더를 제외한 데이터만
        splited: str = line.split(',')
        if len(splited) < 4:
            continue

        sql = 'INSERT INTO mars_weather(weather_id, mars_date, temp, storm) VALUES(%s, %s, %s, %s);'
        cursor.execute(sql, (splited[0], splited[1], splited[2], splited[3]))

    connection.commit()

    cursor.close()
    connection.close()

class DBConnector:

    connect_config = { # DB 연결 설정
        'host': 'localhost',
        'user': 'root',
        'password': 'admin',
        'db': 'codyssey',
        'charset': 'utf8'
    }

    @staticmethod
    def get_connection():
        return pymysql.connect(**DBConnector.connect_config)
    
if (__name__ == '__main__'):
    main()