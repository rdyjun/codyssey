import random
import time

INTERNAL_TEMPERATURE_RANGE: tuple[int, int] = (18, 30)
EXTERNAL_TEMPERATURE_RANGE: tuple[int, int] = (0, 21)
INTERNAL_HUMIDITY_RANGE: tuple[int, int] = (50, 60)
EXTERNAL_ILLUMINANCE_RANGE: tuple[int, int] = (500, 715)
INTERNAL_CO2_RANGE: tuple[int, int] = (0.02, 0.1)
INTERNAL_OXYGEN_RANGE: tuple[int, int] = (4, 7)

class DummySensor:
    env_values = {
        'mars_base_internal_temperature': None,  # 18 ~ 30
        'mars_base_external_temperature': None,  # 0 ~ 21
        'mars_base_internal_humidity': None,     # 50 ~ 60
        'mars_base_external_illuminance': None,  # 500 ~ 715
        'mars_base_internal_co2': None,          # 0.02 ~ 0.1
        'mars_base_internal_oxygen': None        # 4 ~ 7
    }

    isInitialized = False

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(*INTERNAL_TEMPERATURE_RANGE)
        self.env_values['mars_base_external_temperature'] = random.randint(*EXTERNAL_TEMPERATURE_RANGE)
        self.env_values['mars_base_internal_humidity'] = random.randint(*INTERNAL_HUMIDITY_RANGE)
        self.env_values['mars_base_external_illuminance'] = random.randint(*EXTERNAL_ILLUMINANCE_RANGE)
        self.env_values['mars_base_internal_co2'] = random.uniform(*INTERNAL_CO2_RANGE)
        self.env_values['mars_base_internal_oxygen'] = random.randint(*INTERNAL_OXYGEN_RANGE)
        self.isInitialized = True;

    def get_env(self):
        if not self.isInitialized:
            self.set_env()

        with open('./mission-3-4/env.log', 'w') as f:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'Date: {current_time}\n\n')
            for field_name, value in self.env_values.items():
                if field_name.startswith('_'):  # private 속성 제외
                    continue

                f.write(f'{field_name}: {value}\n')
        return self.env_values

class MarsMissionComputer:
    def __init__(self):
        self.internal_temperature_range = (18, 30)  # (min, max) 튜플로 온도 범위 정의
        self.mars_base_internal_temperature = random.randint(*self.internal_temperature_range)

def mission_3():
    ds = DummySensor()
    ds.set_env()
    print(ds.get_env())

class MissionComputer:
    env_values_mean = {
        'mars_base_internal_temperature': 0,
        'mars_base_external_temperature': 0,
        'mars_base_internal_humidity': 0,
        'mars_base_external_illuminance': 0,
        'mars_base_internal_co2': 0.0,
        'mars_base_internal_oxygen': 0
    }

    def print_json(self, env_values, divider):
        print('{\n')
        for i, (field_name, value) in enumerate(env_values.items()):
            print(f"    '{field_name}': {value / divider}", end='')
            if i < len(env_values) - 1:
                print(',')
        print('\n}')

    def get_sensor_data(self):
        start_time = time.time()
        count = 0
        ds = DummySensor()

        while (True):
            ds.set_env()
            env_values = ds.get_env()
            self.print_json(env_values, 1)

            if time.time() - start_time >= 300:
                self.env_values_mean['mars_base_external_temperature'] += env_values['mars_base_external_temperature']
                self.env_values_mean['mars_base_internal_temperature'] += env_values['mars_base_internal_temperature']
                self.env_values_mean['mars_base_internal_humidity'] += env_values['mars_base_internal_humidity']
                self.env_values_mean['mars_base_external_illuminance'] += env_values['mars_base_external_illuminance']
                self.env_values_mean['mars_base_internal_co2'] += env_values['mars_base_internal_co2']
                self.env_values_mean['mars_base_internal_oxygen'] += env_values['mars_base_internal_oxygen']
                count += 1

                print(f'평균 값 출력: ')
                self.print_json(self.env_values_mean, count)
                start_time = time.time()

            time.sleep(5)

def mission_4():
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()


try:
    mission_4()
except KeyboardInterrupt:       # Ctrl + C 로 종료
    print()
    print('System stoped….')