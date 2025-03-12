import analysis_writer # analysis_writer.py 직접 구현

print('Hello Mars')

isProblem = False

try:
    problem_log_file = open('week-1/problem.log', 'w', encoding = 'utf-8')
    analysis_file = open('week-1/log_analysis.md', 'w', encoding = 'utf-8')
    logs = open('week-1/mission_computer_main.log', 'r', encoding = 'utf-8')
    log_content = logs.read()
    log_array = log_content.strip().split('\n')
    del log_array[0]

    # for log in log_array: # 정방향
    #     print(log)
    for log in reversed(log_array):
        print(log)

    problem = []    # problem log를 저장하기 위한 배열
    reason = ''

    for index in range(len(log_array)):
        if 'explosion' in log_array[index]:
            if not isProblem and index > 0:
                problem.append(log_array[index - 1])        # 폭발 로그 직전 로그 수집
                reason = log_array[index - 1].split(',')[2]

            isProblem = True                                # 문제 로그 발견 처리

        if isProblem:
            problem_log_file.write(log_array[index] + '\n')
            problem.append(log_array[index])
        
    analysis_writer.write(analysis_file, problem, reason)
    
    problem_log_file.close()
    analysis_file.close()
    logs.close()

except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except UnicodeDecodeError:
    print("파일을 UTF-8로 디코딩할 수 없습니다. 다른 인코딩을 사용해 보세요.")
except Exception as e:
    print(f"예상치 못한 오류가 발생했습니다: {e}")