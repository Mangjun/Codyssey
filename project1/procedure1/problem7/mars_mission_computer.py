# 실행하려면 project1 폴더까지 이동한 뒤 python -m procedure1.problem7.mars_mission_computer 입력

from procedure1.problem6.mars_mission_computer import DummySensor
import time
import threading

# 문제 8
import platform
import psutil # pip install psutil

# 전역 변수
stop_program = False
standard_time = (300, "5분")
keys = (
    'mars_base_internal_temperature',
    'mars_base_external_temperature',
    'mars_base_internal_humidity',
    'mars_base_external_illuminance',
    'mars_base_internal_co2',
    'mars_base_internal_oxygen'
)
system_exit = ('q', 'Q')

# Json 형식 출력
def print_json(data) :
    data_length = len(data)
    print()
    print('{')
    for index, (key, value) in enumerate(data.items()) :
        if index == data_length - 1 :
            print('    "{0}": {1}'.format(key, value))
        else :
            print('    "{0}": {1},'.format(key, value))
    print('}')
    print()

class MissonComputer :
    def __init__(self):
        self.env_values = {key: 0 for key in keys}
    
    def get_sensor_data(self, sensor) :
        sensor.set_env()
        sensor_data = sensor.get_env()

        for key in keys:
            self.env_values[key] = sensor_data[key]

        return self.env_values

    # 문제 8
    def get_mission_computer_info(self, setting, error) :
        try :
            os_data = {}

            if 'os' in setting :
                os_data['운영체제'] = platform.platform()
            
            if 'os_version' in setting :
                os_data['운영체제 버전'] = platform.version()

            if 'cpu' in setting :
                os_data['CPU의 타입'] = platform.processor()

            if 'cpu_core_count' in setting :
                os_data['CPU의 코어 수'] = psutil.cpu_count(logical=False)

            if 'mem' in setting :
                os_data['메모리의 크기'] = psutil.virtual_memory()

            if len(os_data) != 0 :
                print_json(os_data)
        except :
            print(error)
            
    def get_mission_computer_load(self, setting, error) :
        try :
            using_percent_data = {}

            if 'cpu_using_percent' in setting :
                using_percent_data['CPU 실시간 사용량'] = psutil.cpu_percent()

            if 'mem_using_percent' in setting :
                using_percent_data['메모리 실시간 사용량'] = psutil.virtual_memory().percent

            if len(using_percent_data) != 0 :
                print_json(using_percent_data)
            
        except :
            print(error)
    

# 쓰레드 키보드 입력 처리
def get_user_input():
    global stop_program
    while True:
        user_input = input()
        if user_input in system_exit:
            print("System stopped...")
            stop_program = True

# 평균 구하기
def get_avg(env_values, cnt) :
    if cnt == 0:
        return {key: 0 for key in keys}
    else :
        return {key: env_values[key] / cnt for key in keys}

if __name__ == '__main__':
    ds = DummySensor()
    RunComputer = MissonComputer()

    # 쓰레드 생성
    input_thread = threading.Thread(target=get_user_input)
    input_thread.daemon = True
    input_thread.start()

    # 평균 환경 데이터 초기화
    avg_env = {key: 0 for key in keys}

    # 평균 환경 데이터 측정 카운트 초기화
    cnt = 0

    start_time = time.time()

    while not stop_program:
        current_time = time.time()
        elsapsed_time = current_time - start_time

        # 평균 데이터 출력
        if elsapsed_time >= standard_time[0] :
            print("---{}분 동안의 평균 환경 데이터---".format(standard_time[1]))
            print_json(get_avg(avg_env, cnt))
            
            # 다시 측정하기 위해 초기화
            avg_env = {key: 0 for key in avg_env.keys()}
            cnt = 0
            start_time = current_time

        env_values = RunComputer.get_sensor_data(ds)
        
        # 환경 데이터 누적 계산
        for key in keys:
            avg_env[key] += env_values[key]

        cnt += 1

        print_json(env_values)

        print("멈추려면 q를 입력하세요...")
        print()
        
        time.sleep(5)