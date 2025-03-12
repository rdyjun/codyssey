import analysis_writer # analysis_writer.py 직접 구현
import file_manager # file_manager.py 직접 구현

print('Hello Mars')

isProblem = False

def run():
    problem_log_file, analysis_file, logs = file_manager.getFiles()
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
    
    file_manager.closeAll()

run()