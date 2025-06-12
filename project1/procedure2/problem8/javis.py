# project1 에서 python -m procedure2.problem8.javis 실행

import os
from procedure2.problem7.javis import Javis

def main():
    javis = Javis()
    audio_dir = './procedure2/problem7/records'
    csv_dir = './procedure2/problem8/csvs'
    audio_files = javis.get_audio_files(audio_dir)
    print(f'오디오 파일 목록: {audio_files}')
    for audio_file in audio_files:
        print(f'파일 처리중: {audio_file}')
        audio_path = os.path.join(audio_dir, audio_file)
        stt_data = javis.speech_to_text(audio_path)
        javis.save_csv(csv_dir, audio_path, stt_data)
        print(f'CSV 저장 완료: {audio_file}')

    keyword = input('검색할 키워드를 입력하세요 (엔터시 종료): ')
    if keyword:
        javis.search_keyword_in_csv(audio_dir, keyword)

if __name__ == '__main__':
    main()