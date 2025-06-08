import os
import csv
import speech_recognition as sr

"""
javis.py 파일에서 실행해주세요.
"""

def get_audio_file_list(directory):
    file_list = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.wav'):
            file_list.append(file_name)
    return file_list

def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='ko-KR')
    except sr.UnknownValueError:
        text = ''
    except sr.RequestError:
        text = ''
    return text

def save_text_to_csv(audio_file_path, datetime, text):
    base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    csv_file_name = base_name + '.csv'
    folder = os.path.dirname(audio_file_path)
    csv_file_path = os.path.join(folder, csv_file_name)
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'text'])
        writer.writerow([datetime, text])

def process_audio_files(directory):
    file_list = get_audio_file_list(directory)
    for file_name in file_list:
        audio_file_path = os.path.join(directory, file_name)
        text = speech_to_text(audio_file_path)
        save_text_to_csv(audio_file_path, text)
        print(f'Processed {file_name} -> {file_name[:-4]}.csv')

def search_keyword_in_csv(directory, keyword):
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(directory, file_name)
            with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if keyword in row[1]:
                        print(f'[{file_name}] {row[0]}초: {row[1]}')