# 실행하려면 project1 폴더까지 이동한 뒤 python -m procedure1.problem8.mars_mission_computer 입력

from procedure1.problem6.mars_mission_computer import DummySensor
from procedure1.problem7.mars_mission_computer import MissonComputer

if __name__ == '__main__':
    ds = DummySensor()
    runComputer = MissonComputer()

    # 설정 파일 경로
    setting_file_path = 'procedure1/problem8/setting.txt'

    # 설정
    setting = []

    # 설정 파일 읽기
    with open(setting_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                setting += [item.strip() for item in line.split(',')]

    runComputer.get_mission_computer_info(setting, '운영체제 정보를 불러오는데 오류가 발생했습니다.')
    runComputer.get_mission_computer_load(setting, '실시간 사용량 정보를 불러오는데 오류가 발생했습니다.')