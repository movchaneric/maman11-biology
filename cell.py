class Cell:
    # TODO: Add windDirection, humidityLevel, pullutionMeter later on...
    def __init__(self, x, y, cell_type):
        self.x = x
        self.y = y
        self.cell_type = cell_type
        self.cell_tempreture= self.get_init_temp(cell_type)
        self.wind_direction = self.set_init_wind_direction(cell_type)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def get_wind_direction(self):
        return self.wind_direction
    
    def set_tempreture(self, new_temp):
        self.cell_tempreture = new_temp

    def cell_type_init(cell_type):
        if cell_type == 'C':
            return 'city'
        elif cell_type == 'S':
            return 'sea'
        elif cell_type == 'L':
            return "land"
        elif cell_type == 'I':
            return 'ice'
        elif cell_type == 'G':
            return 'ground'
        else:
            return 'land'  # Default color if cell_type is not recognized

    def get_init_temp(self, cell_type):
        if cell_type == 'C':
            return 25
        elif cell_type == 'S':
            return 15
        elif cell_type == 'L':
            return 35
        elif cell_type == 'I':
            return -15
        elif cell_type == 'G':
            return 45
    
    # set default values for cell wind direction
    def set_init_wind_direction(self, cell_type):
        if cell_type == "S":
            return "S"
        elif cell_type == "L" or cell_type =="G":
            return "N"
        elif cell_type == "I":
            return "E"
        elif cell_type == "C":
            return "W"
    
    def set_reverse_direction(self):
        if self.get_wind_direction() == 'S':
            self.wind_direction = 'N'
        elif self.get_wind_direction() == 'N':
            self.wind_direction = 'S'
        elif self.get_wind_direction() == 'W':
            self.wind_direction = 'E'
        elif self.get_wind_direction() == 'E':
            self.wind_direction = 'W'

    def set_wind_direction(self, direction):
        self.wind_direction = direction

    def get_wind_direction_icon(self):
        if self.get_wind_direction() == 'S':
            return '↓'
        elif self.get_wind_direction() == 'N':
            return '↑'
        elif self.get_wind_direction() == 'E':
            return '→'
        elif self.get_wind_direction() == 'W':
            return '←'
