import os
import datetime
import sounddevice as sd
import wavio

def ensure_records_folder():
    if not os.path.exists('./records'):
        os.makedirs('./records')

def get_record_filename():
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return os.path.join('records', filename)

def record_voice(duration = 5, fs = 44100):
    print('녹음을 시작합니다. {}초 동안 말하세요...'.format(duration))
    recording = sd.rec(int(duration * fs), samplerate = fs, channels = 1, dtype = 'int16')
    sd.wait()
    ensure_records_folder()
    filename = get_record_filename()
    wavio.write(filename, recording, fs, sampwidth = 2)
    print('녹음이 저장되었습니다: {}'.format(filename))

def list_records_by_date(start_date, end_date):
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

def main():
    while True:
        print('\n1. 음성 녹음\n2. 날짜로 파일 목록 보기\n3. 종료')
        choice = input('선택: ')
        if choice == '1':
            record_voice()
        elif choice == '2':
            start_date = input('시작 날짜 입력 (YYYYMMDD): ')
            end_date = input('종료 날짜 입력 (YYYYMMDD): ')
            files = list_records_by_date(start_date, end_date)
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
