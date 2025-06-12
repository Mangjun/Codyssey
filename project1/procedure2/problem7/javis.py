# 문제 7
import os
import datetime
import sounddevice as sd
import wavio

# 문제 8
import csv
import speech_recognition as sr

class Javis:
    def __init__(self):
        pass
    
    # 문제 7
    def ensure_records_folder(self):
        if not os.path.exists('./records'):
            os.makedirs('./records')

    def get_record_filename(self):
        now = datetime.datetime.now()
        filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        return os.path.join('records', filename)

    def record_voice(self, duration = 5, fs = 44100):
        print('녹음을 시작합니다. {}초 동안 말하세요...'.format(duration))
        recording = sd.rec(int(duration * fs), samplerate = fs, channels = 1, dtype = 'int16')
        sd.wait()
        self.ensure_records_folder()
        filename = self.get_record_filename()
        wavio.write(filename, recording, fs, sampwidth = 2)
        print('녹음이 저장되었습니다: {}'.format(filename))

    def list_records_by_date(self, start_date, end_date):
        files = []
        start_dt = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_dt = datetime.datetime.strptime(end_date, '%Y%m%d')
        for filename in os.listdir('records'):
            if filename.endswith('.wav'):
                date_str = filename[:8]
                try:
                    file_dt = datetime.datetime.strptime(date_str, '%Y%m%d')
                    if start_dt <= file_dt <= end_dt:
                        files.append(filename)
                except ValueError:
                    continue
        return files
    
    # 문제 8
    def get_audio_files(self, directory):
        audio_extensions = ('.wav')
        files = []
        for file_name in os.listdir(directory):
            if file_name.lower().endswith(audio_extensions):
                files.append(file_name)
        return files

    def speech_to_text(self, audio_path):
        recognizer = sr.Recognizer()
        result_list = []
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language='ko-KR')
                result_list.append(('0:00', text))
            except sr.UnknownValueError:
                result_list.append(('0:00', '음성을 인식할 수 없습니다.'))
            except sr.RequestError as e:
                result_list.append(('0:00', f'API 에러: {e}'))
        return result_list

    def save_csv(self, csv_dir, audio_path, stt_data):
        audio_basename = os.path.basename(audio_path)
        csv_filename = os.path.splitext(audio_basename)[0] + '.csv'
        csv_path = os.path.join(csv_dir, csv_filename)

        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        print('CSV 저장 경로:', csv_path)
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['시간', '인식된 텍스트'])
            for row in stt_data:
                writer.writerow(row)


    def search_keyword_in_csv(self, directory, keyword):
        for file_name in os.listdir(directory):
            if file_name.lower().endswith('.csv'):
                with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader, None)  # 헤더 스킵
                    for row in reader:
                        if keyword in row[1]:
                            print(f'{file_name}: {row[0]} - {row[1]}')

def main():
    javis = Javis()
    while True:
        print('\n1. 음성 녹음\n2. 날짜로 파일 목록 보기\n3. 종료')
        choice = input('선택: ')
        if choice == '1':
            javis.record_voice()
        elif choice == '2':
            start_date = input('시작 날짜 입력 (YYYYMMDD): ')
            end_date = input('종료 날짜 입력 (YYYYMMDD): ')
            files = javis.list_records_by_date(start_date, end_date)
            if files:
                print('해당 기간의 녹음 파일 목록:')
                for f in files:
                    print(f)
            else:
                print('해당 기간에 녹음 파일이 없습니다.')
        elif choice == '3':
            print('프로그램을 종료합니다.')
            break
        else:
            print('잘못된 입력입니다.')

if __name__ == '__main__':
    main()
