print('Hello Mars')

try:
    f = open('week-1/mission_computer_main.log', 'r', encoding = 'utf-8');
    # print(f.read()); // 정방향
    log_array = f.read().strip().split('\n')
    print(log_array[0])
    del log_array[0]

    for log in reversed(log_array):
        print(log)
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except UnicodeDecodeError:
    print("파일을 UTF-8로 디코딩할 수 없습니다. 다른 인코딩을 사용해 보세요.")
except Exception as e:
    print(f"예상치 못한 오류가 발생했습니다: {e}")