import os
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import main

def get_records_folder():
    folder = 'records'
    os.makedirs(folder, exist_ok=True)
    return folder

def get_filename():
    return datetime.now().strftime('%Y%m%d-%H%M%S') + '.wav'

def record_voice(duration=5, fs=44100):
    print(f'녹음을 시작합니다. {duration}초 동안 말해주세요.')
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print('녹음이 완료되었습니다.')
    return recording, fs

def save_recording(recording, fs, folder, filename):
    filepath = os.path.join(folder, filename)
    sf.write(filepath, recording, fs, subtype='PCM_16')
    print(f'녹음 파일 저장: {filepath}')
    return filepath

def main_javis():
    folder = get_records_folder()
    filename = get_filename()
    recording, fs = record_voice()
    filepath = save_recording(recording, fs, folder, filename)

    # main.py의 STT 및 CSV 저장 함수 호출
    print('STT 및 CSV 저장을 시작합니다...')
    text = main.speech_to_text(filepath)
    main.save_text_to_csv(filepath, datetime.now(), text)
    print('STT 및 CSV 저장이 완료되었습니다.')

    # 키워드 검색
    keyword = input('검색할 키워드를 입력하세요(엔터시 종료): ')
    if keyword:
        print(f'키워드 "{keyword}" 검색 결과:')
        main.search_keyword_in_csv(folder, keyword)

if __name__ == '__main__':
    main_javis()
