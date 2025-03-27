import random

class EnvValues:
    mars_base_internal_temperature: int # 18 ~ 30
    mars_base_external_temperature: int # 0 ~ 21
    mars_base_internal_humidity: int    # 50 ~ 60
    mars_base_external_illuminance: int # 500 ~ 715
    mars_base_internal_co2: float       # 0.02 ~ 0.1
    mars_base_internal_oxygen: int      # 4 ~ 7

    internal_temperature_range: tuple[int, int] = (18, 30)
    external_temperature_range: tuple[int, int] = (0, 21)
    internal_humidity_range: tuple[int, int] = (50, 60)
    external_illuminance_range: tuple[int, int] = (500, 715)
    internal_co2_range: tuple[int, int] = (0.02, 0.1)
    internal_oxygen_range: tuple[int, int] = (4, 7)

    def random(self):
        self.mars_base_internal_temperature = random.randint(self.internal_temperature_range)
        self.mars_base_external_temperature = random.randint(self.external_temperature_range)
        self.mars_base_internal_humidity = random.randint(self.internal_humidity_range)
        self.mars_base_external_illuminance = random.randint(self.external_illuminance_range)
        self.mars_base_internal_co2 = random.uniform(self.internal_co2_range)
        self.mars_base_internal_oxygen = random.randint(self.internal_oxygen_range)

class DummySensor:
    env_values: EnvValues

    def set_env(self):
        self.env_values = EnvValues()
        self.env_values.random()

    def get_env(self):
        return self.env_values

class MarsMissionComputer:
    def __init__(self):
        self.internal_temperature_range = (18, 30)  # (min, max) 튜플로 온도 범위 정의
        self.mars_base_internal_temperature = random.randint(*self.internal_temperature_range)

ds = DummySensor()
ds.set_env()
print(ds.get_env())