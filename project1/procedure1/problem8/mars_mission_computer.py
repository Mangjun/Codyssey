# 실행하려면 project1 폴더까지 이동한 뒤 python -m procedure1.problem8.mars_mission_computer 입력

from procedure1.problem6.mars_mission_computer import DummySensor
from procedure1.problem7.mars_mission_computer import MissonComputer

if __name__ == '__main__':
    ds = DummySensor()
    runComputer = MissonComputer()
    runComputer.get_mission_computer_info()
    print()
    runComputer.get_mission_computer_load()