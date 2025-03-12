problem_log_file = None
analysis_file = None
logs = None

def getFiles():
    global isDefine, problem_log_file, analysis_file, logs

    try:
        problem_log_file = open('week-1/problem.log', 'w', encoding = 'utf-8')
        analysis_file = open('week-1/log_analysis.md', 'w', encoding = 'utf-8')
        logs = open('week-1/mission_computer_main.log', 'r', encoding = 'utf-8')

        return (problem_log_file, analysis_file, logs)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except UnicodeDecodeError:
        print("파일을 UTF-8로 디코딩할 수 없습니다. 다른 인코딩을 사용해 보세요.")
    except Exception as e:
        print(f"파일을 여는 중 예상치 못한 오류가 발생했습니다: {e}")

def closeAll():
    global isDefine, problem_log_file, analysis_file, logs

    if logs is None:
        return


    try:
        problem_log_file.close()
        analysis_file.close()
        logs.close()  

    except Exception as e:
        print(f"파일 종료 중 예상치 못한 오류가 발생했습니다: {e}")  
        