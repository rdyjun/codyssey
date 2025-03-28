import random
from datetime import datetime

class EnvValues:
    mars_base_internal_temperature: int # 18 ~ 30
    mars_base_external_temperature: int # 0 ~ 21
    mars_base_internal_humidity: int    # 50 ~ 60
    mars_base_external_illuminance: int # 500 ~ 715
    mars_base_internal_co2: float       # 0.02 ~ 0.1
    mars_base_internal_oxygen: int      # 4 ~ 7

    _internal_temperature_range: tuple[int, int] = (18, 30)
    _external_temperature_range: tuple[int, int] = (0, 21)
    _internal_humidity_range: tuple[int, int] = (50, 60)
    _external_illuminance_range: tuple[int, int] = (500, 715)
    _internal_co2_range: tuple[int, int] = (0.02, 0.1)
    _internal_oxygen_range: tuple[int, int] = (4, 7)

    def random(self):
        self.mars_base_internal_temperature = random.randint(*self._internal_temperature_range)
        self.mars_base_external_temperature = random.randint(*self._external_temperature_range)
        self.mars_base_internal_humidity = random.randint(*self._internal_humidity_range)
        self.mars_base_external_illuminance = random.randint(*self._external_illuminance_range)
        self.mars_base_internal_co2 = random.uniform(*self._internal_co2_range)
        self.mars_base_internal_oxygen = random.randint(*self._internal_oxygen_range)
    def get_items(self):
        return self.__dict__.items()

class DummySensor:
    env_values: EnvValues

    def set_env(self):
        self.env_values = EnvValues()
        self.env_values.random()

    def get_env(self):
        with open('./mission-3/env.log', 'w') as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Date: {current_time}\n\n")
            for field_name, value in self.env_values.get_items():
                if field_name.startswith('_'):  # private 속성 제외
                    continue

                f.write(f"{field_name}: {value}\n")
        return self.env_values

class MarsMissionComputer:
    def __init__(self):
        self.internal_temperature_range = (18, 30)  # (min, max) 튜플로 온도 범위 정의
        self.mars_base_internal_temperature = random.randint(*self.internal_temperature_range)

ds = DummySensor()
ds.set_env()
print(ds.get_env())