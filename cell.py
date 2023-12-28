import cell_properties as cp

class Cell:
    # TODO: set temreture not to be default one 
    def __init__(self, x: int, y: int, cell_type, color):
        self.x = x
        self.y = y
        self.type = cell_type # L = Land, C = City ,....
        self.tempreture= cp.CELL_TYPE_TO_TEMPERATURE_DICT[cell_type]
        self.wind_direction = cp.CELL_TYPE_TO_WIND_DIRECTION_DICT[cell_type]
        self.pollution = 0
        self.color = color
        self.cloud =  self.cloud_in_cell()  #Clouds or None depends on the cell number
        self.rain = self.rain_meter() # 100% chance of rain if clouds are present else 0% - no rain
        self.prev_temperature = self.tempreture

    @property
    def wind_on_y(self):
        return self.wind_direction in ['W', 'E']
    
    @property
    def wind_on_x(self):
        return self.wind_direction in ['S', 'N']
    
    #init cloud on every n-th cell
    def cloud_in_cell(self):
        nth_cell = 5
        if (self.x + self.y) % nth_cell == 0:
            return 'Clouds'
        else:
            return None
        
    def rain_meter(self):
        if self.cloud == 'Clouds':
            # 100% chance of rain if clouds are present
            return 100  
        return 0
    