import cell_properties as cp

class Cell:
    # TODO: Add windDirection, humidityLevel, pullutionMeter later on...

    def __init__(self, x: int, y: int, cell_type, color):
        self.x = x
        self.y = y
        self.type = cell_type # L = Land, C = City ,....
        self.tempreture= cp.CELL_TYPE_TO_TEMPERATURE_DICT[cell_type]
        self.wind_direction = cp.CELL_TYPE_TO_WIND_DIRECTION_DICT[cell_type]
        self.pollution = 0
        self.color = color

    
    @property
    def wind_on_y(self):
        return self.wind_direction in ['W', 'E']
    
    @property
    def wind_on_x(self):
        return self.wind_direction in ['S', 'N']
