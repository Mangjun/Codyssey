import random
import time

class DummySensor :
    def __init__(self) :
        self.env_values = dict()
        self.env_values['mars_base_internal_temperature'] = 0
        self.env_values['mars_base_external_temperature'] = 0
        self.env_values['mars_base_internal_humidity'] = 0
        self.env_values['mars_base_external_illuminance'] = 0
        self.env_values['mars_base_internal_co2'] = 0
        self.env_values['mars_base_internal_oxygen'] = 0

    def set_env(self) :
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    def get_env(self) :
        if __name__ == '__main__' :
            self.write_log()
        return self.env_values
    
    def write_log(self) :
        t = time.localtime()

        try :
            with open('mars_mission_computer.log', 'a', encoding='utf-8') as f :
                f.write('[{year}-{month}-{day} {hour}:{minute}:{second}] '.format(year = t.tm_year, month = t.tm_mon, day = t.tm_mday, hour = t.tm_hour, minute = t.tm_min, second = t.tm_sec))
                f.write('mars_base_internal_temperature : {temperature}도, '.format(temperature = self.env_values['mars_base_internal_temperature']))
                f.write('mars_base_external_temperature : {temperature}도, '.format(temperature = self.env_values['mars_base_external_temperature']))
                f.write('mars_base_internal_humidity : {humidity}%, '.format(humidity = self.env_values['mars_base_internal_humidity']))
                f.write('mars_base_external_illuminance : {illuminance}W/m2, '.format(illuminance = self.env_values['mars_base_external_illuminance']))
                f.write('mars_base_internal_co2 : {co2}%, '.format(co2 = self.env_values['mars_base_internal_co2']))
                f.write('mars_base_internal_oxygen : {oxygen}%\n'.format(oxygen = self.env_values['mars_base_internal_oxygen']))
        except Exception as e :
            print('File Open Error : {error}'.format(error = e))
        
if __name__ == '__main__' :
    ds = DummySensor()
    ds.set_env()
    data = ds.get_env()

    for key, value in data.items() :
        if key == 'mars_base_internal_temperature' or key == 'mars_base_external_temperature' :
            print('{key} : {value}도'.format(key = key, value = value))

        elif key == 'mars_base_internal_humidity' or key == 'mars_base_internal_co2' or key == 'mars_base_internal_oxygen' :
            print('{key} : {value}%'.format(key = key, value = value))

        elif key == 'mars_base_external_illuminance' :
            print('{key} : {value}W/m2'.format(key = key, value = value))