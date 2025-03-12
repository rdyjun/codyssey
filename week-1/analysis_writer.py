import explosion_analysis
import unknown_analysis

problem_types = {
    'UNKNOWN': unknown_analysis,
    'OXYGEN_TANK_EXPLOSION': explosion_analysis
}

def write(analysis_file, problem, reason_log):
    joined_problem = ''.join(problem)

    # 문제 타입 확인
    problem_type = problem_types['UNKNOWN']
    print(problem)
    if 'Oxygen tank explosion' in joined_problem:
        problem_type = problem_types['OXYGEN_TANK_EXPLOSION']

    # 문제 제목 작성
    analysis_file.write('## 문제\n\n')
    analysis_file.write(problem_type.problem() + '\n\n')

    # 문제 원인 작성
    analysis_file.write('## 문제 원인\n\n')
    analysis_file.write(problem_type.reason(reason_log) + '\n\n')
    
    analysis_file.write('## 문제 로그\n\n')
    for problem_log in problem:
        analysis_file.write(problem_log + '\n')