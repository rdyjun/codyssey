def analysis(analysis_file, problem, reason):
    analysis_file.write('## 문제\n\n')
    analysis_file.write('화성 기지 폭발\n\n')
    analysis_file.write('## 문제 원인\n\n')
    analysis_file.write(reason + '\n\n')
    analysis_file.write('## 문제 로그\n\n')
    for problem_log in problem:
        analysis_file.write(problem_log + '\n')
    