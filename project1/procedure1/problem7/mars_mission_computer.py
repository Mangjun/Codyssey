# 실행하려면 project1 폴더까지 이동한 뒤 python -m procedure1.problem7.mars_mission_computer 입력

from procedure1.problem6.mars_mission_computer import DummySensor
import time
import threading
import platform
import psutil # pip install psutil

class MissonComputer :
    def __init__(self):
        self.env_values = dict()
        self.env_values['mars_base_internal_temperature'] = 0
        self.env_values['mars_base_external_temperature'] = 0
        self.env_values['mars_base_internal_humidity'] = 0
        self.env_values['mars_base_external_illuminance'] = 0
        self.env_values['mars_base_internal_co2'] = 0
        self.env_values['mars_base_internal_oxygen'] = 0
    
    def get_sensor_data(self, sensor) :
        sensor.set_env()
        sensor_data = sensor.get_env()
        self.env_values['mars_base_internal_temperature'] = sensor_data['mars_base_internal_temperature']
        self.env_values['mars_base_external_temperature'] = sensor_data['mars_base_external_temperature']
        self.env_values['mars_base_internal_humidity'] = sensor_data['mars_base_internal_humidity']
        self.env_values['mars_base_external_illuminance'] = sensor_data['mars_base_external_illuminance']
        self.env_values['mars_base_internal_co2'] = sensor_data['mars_base_internal_co2']
        self.env_values['mars_base_internal_oxygen'] = sensor_data['mars_base_internal_oxygen']

        return self.env_values

    def get_mission_computer_info(self) :
        try :
            os = platform.platform()
            os_version = platform.version()
            cpu = platform.processor()
            cpu_core_count = psutil.cpu_count(logical=False)
            mem = psutil.virtual_memory()
            print('{')
            print('    "운영체제": "{0}",'.format(os))
            print('    "운영체제 버전": "{0}",'.format(os_version))
            print('    "CPU의 타입": "{0}",'.format(cpu))
            print('    "CPU의 코어 수": "{0}",'.format(cpu_core_count))
            print('    "메모리의 크기": "{0:.2f}GB"'.format(mem.total / (1024**3)))
            print('}')
        except :
            print('운영체제 정보를 가져오는데 실패하였습니다.')
            
    def get_mission_computer_load(self) :
        try :
            cpu_current_using_percent = psutil.cpu_percent()
            mem_current_using_precent = psutil.virtual_memory().percent
            print('{')
            print('    "CPU 실시간 사용량": "{0}%",'.format(cpu_current_using_percent))
            print('    "메모리 실시간 사용량": "{0}%"'.format(mem_current_using_precent))
            print('}')
        except :
            print('CPU 및 메모리 사용량을 가져오는데 실패하였습니다.')
    
def get_user_input():
    global stop_program
    while True:
        user_input = input()
        if user_input == 'q' or user_input == 'Q':
            print("System stopped...")
            stop_program = True
            break

stop_program = False

input_thread = threading.Thread(target=get_user_input)
input_thread.daemon = True
input_thread.start()

if __name__ == '__main__':
    ds = DummySensor()
    RunComputer = MissonComputer()

    avg_env = dict()
    cnt = 0

    avg_env['mars_base_internal_temperature'] = 0
    avg_env['mars_base_external_temperature'] = 0
    avg_env['mars_base_internal_humidity'] = 0
    avg_env['mars_base_external_illuminance'] = 0
    avg_env['mars_base_internal_co2'] = 0
    avg_env['mars_base_internal_oxygen'] = 0

    start_time = time.time()

    while not stop_program:
        current_time = time.time()
        elsapsed_time = current_time - start_time

        if elsapsed_time >= 300 :
            print("---5분 동안의 평균 환경 데이터---")
            print('{')
            for key, value in avg_env.items() :
                if key == 'mars_base_internal_oxygen' :
                    print('    "{0}": {1}'.format(key, value/cnt))
                else :
                    print('    "{0}": {1},'.format(key, value/cnt))
            print('}')
            print()
            avg_env['mars_base_internal_temperature'] = 0
            avg_env['mars_base_external_temperature'] = 0
            avg_env['mars_base_internal_humidity'] = 0
            avg_env['mars_base_external_illuminance'] = 0
            avg_env['mars_base_internal_co2'] = 0
            avg_env['mars_base_internal_oxygen'] = 0
            start_time = current_time

        env_values = RunComputer.get_sensor_data(ds)
        
        cnt += 1
        avg_env['mars_base_internal_temperature'] += env_values['mars_base_internal_temperature']
        avg_env['mars_base_external_temperature'] += env_values['mars_base_external_temperature']
        avg_env['mars_base_internal_humidity'] += env_values['mars_base_internal_humidity']
        avg_env['mars_base_external_illuminance'] += env_values['mars_base_external_illuminance']
        avg_env['mars_base_internal_co2'] += env_values['mars_base_internal_co2']
        avg_env['mars_base_internal_oxygen'] += env_values['mars_base_internal_oxygen']

        print('{')
        for key, value in env_values.items() :
            if key == 'mars_base_internal_oxygen' :
                print('    "{0}": {1}'.format(key, value))
            else :
                print('    "{0}": {1},'.format(key, value))
        print('}')

        print()

        print("멈추려면 q를 입력하세요...")

        print()
        
        time.sleep(5)