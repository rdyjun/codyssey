import os
import datetime

try:
    import sounddevice as sd
    from scipy.io.wavfile import write
except ImportError:
    print('음성 녹음을 위해 sounddevice와 scipy 패키지가 필요합니다.')
    print('pip install sounddevice scipy 명령어로 설치하세요.')
    exit(1)

# 레코드 파일 검사
def get_records_folder():
    folder = 'records'
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

# 파일 이름 생성
def get_filename():
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return filename

# 녹음, 5초
def record_voice(duration = 5, fs = 44100): # 녹음 시간 5초, Sampling Rate 44100
    print('녹음을 시작합니다. {}초 동안 말을 해주세요.'.format(duration))
    recording = sd.rec(int(duration * fs), samplerate = fs, channels = 1)
    sd.wait()
    print('녹음이 완료되었습니다.')
    return recording, fs

# 녹음 파일 저장
def save_recording(recording, fs, folder, filename):
    filepath = os.path.join(folder, filename)
    write(filepath, fs, recording)
    print('녹음 파일이 저장되었습니다: {}'.format(filepath))


def main():
    folder = get_records_folder()
    filename = get_filename()
    duration = 5  # 녹음 시간(초)
    recording, fs = record_voice(duration=duration)
    save_recording(recording, fs, folder, filename)


if __name__ == '__main__':
    main()
