# 실행하려면 project1 폴더까지 이동한 뒤 python -m procedure1.problem7.mars_mission_computer 입력

from procedure1.problem6.mars_mission_computer import DummySensor
from time import sleep

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
        while 1 :
            sensor.set_env()
            sensor_data = sensor.get_env()
            self.env_values['mars_base_internal_temperature'] = sensor_data['mars_base_internal_temperature']
            self.env_values['mars_base_external_temperature'] = sensor_data['mars_base_external_temperature']
            self.env_values['mars_base_internal_humidity'] = sensor_data['mars_base_internal_humidity']
            self.env_values['mars_base_external_illuminance'] = sensor_data['mars_base_external_illuminance']
            self.env_values['mars_base_internal_co2'] = sensor_data['mars_base_internal_co2']
            self.env_values['mars_base_internal_oxygen'] = sensor_data['mars_base_internal_oxygen']

            print('{')
            for key, value in self.env_values.items() :
                print('    "{0}": "{1}",'.format(key, value))
            print('}')

            sleep(5)

if __name__ == '__main__':
    ds = DummySensor()
    RunComputer = MissonComputer()
    RunComputer.get_sensor_data(ds)