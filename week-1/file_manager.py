problem_log_file = None
analysis_file = None
logs = None

def getFiles():
    global isDefine, problem_log_file, analysis_file, logs
    
    problem_log_file = open('week-1/problem.log', 'w', encoding = 'utf-8')
    analysis_file = open('week-1/log_analysis.md', 'w', encoding = 'utf-8')
    logs = open('week-1/mission_computer_main.log', 'r', encoding = 'utf-8')

    return (problem_log_file, analysis_file, logs)

def closeAll():
    global isDefine, problem_log_file, analysis_file, logs

    if logs is None:
        return

    problem_log_file.close()
    analysis_file.close()
    logs.close()    
        