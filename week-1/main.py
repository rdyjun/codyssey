print('Hello Mars')

isProblem = False

try:
    problem_log_file = open('week-1/problem.log', 'w', encoding = 'utf-8');
    logs = open('week-1/mission_computer_main.log', 'r', encoding = 'utf-8').read();
    log_array = logs.strip().split('\n')
    del log_array[0]

    # for log in log_array: # 정방향
    #     print(log)
    for log in reversed(log_array):
        print(log)

    for log in log_array:
        if 'explosion' in log:
            isProblem = True
        if isProblem:
            problem_log_file.write(log + '\n')

except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except UnicodeDecodeError:
    print("파일을 UTF-8로 디코딩할 수 없습니다. 다른 인코딩을 사용해 보세요.")
except Exception as e:
    print(f"예상치 못한 오류가 발생했습니다: {e}")