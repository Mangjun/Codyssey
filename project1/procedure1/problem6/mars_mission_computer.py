import random

class DummySensor :
    def __init__(self) :
        self.env_values = dict()
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    def set_env(self) :
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    def get_env(self) :
        return self.env_values  
        
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