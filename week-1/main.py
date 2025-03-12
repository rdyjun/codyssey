import os

script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, 'Codyssey 프로젝트 현황 로그.log')

try:
    f = open(log_path, 'r', encoding = 'utf-8');
    print(f.read());
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except UnicodeDecodeError:
    print("파일을 UTF-8로 디코딩할 수 없습니다. 다른 인코딩을 사용해 보세요.")
except Exception as e:
    print(f"예상치 못한 오류가 발생했습니다: {e}")