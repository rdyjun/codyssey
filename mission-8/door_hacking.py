import zipfile

# ZIP 파일 경로
zip_file_path = 'mission-8/emergency_storage_key.zip'

# 브루트포스 공격 설정
characters = 'abcdefghijklmnopqrstuvwxyz0123456789' # 소문자, 숫자
min_length = 1
max_length = 10

def generate_passwords(length, current=''):
    if len(current) == length:
        yield current
    else:
        for char in characters:
            yield from generate_passwords(length, current + char)

def extract_zip(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode('utf-8'))
        print(f"비밀번호를 찾았습니다: {password}")
        return True
    except:
        return False

def save_password(found_password):
    if found_password:
        with open('mission-8/password.txt', 'w') as f:
            f.write(found_password)
        print("비밀번호가 password.txt 파일에 저장되었습니다.")
    else:
        print("저장할 비밀번호가 없습니다.")

def unlock_zip():
    with zipfile.ZipFile(zip_file_path) as zf:
        found = False
        for length in range(min_length, max_length + 1):
            for password in generate_passwords(length):
                print(f"시도 중인 비밀번호: {password}")
                if extract_zip(zf, password):
                    found = True
                    save_password(password)  # 비밀번호를 찾으면 저장
                    break
            if found:
                break
        else:
            print("비밀번호를 찾지 못했습니다.")

if __name__ == "__main__":
    unlock_zip()