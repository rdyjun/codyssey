import os

script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, 'Codyssey 프로젝트 현황 로그.log')

f = open(log_path, 'r', encoding='utf-8');
print(f.read());