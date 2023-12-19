import tkinter as tk
import statistics


def create_matrix(rows,cols):
    return [([0]*rows) for i in range(cols)]

def reverse_direction(direction):
    if direction == "N":
        return "S"
    if direction == "E":
        return "W"
    if direction == "W":
        return "E"
    if direction == "S":
        return "N"
   


class Cell:
    def __init__(self, x, y, element, wind_speed=0.5, wind_direction='N', cloud=None, air_pollution=0.08, city_pollution=0.001):
        self.x = x
        self.y = y
        self.element = element  # element types: land, sea, iceburg, forest, city

        self.temperature = self._temperature_init(element)  # temperature in celsius 
        self.wind_speed = wind_speed    # number between 0 (0%) to 1 (100%)
        self.wind_direction = wind_direction    # can be "N", "E", "W", "S"
        self.cloud = cloud  # can be "cloud", "rain_cloud", None
        self.air_pollution = air_pollution  # number between 0 (0%) to 1 (100%)
        self.city_pollution = city_pollution    # how much pollution city generates in a day, number between 0 (0%) to 1 (100%)
        
        # variables to be used for next generation calculation
        self.next_temperature = self.temperature
        self.next_wind_speed = self.wind_speed
        self.next_wind_direction = self.wind_direction
        self.next_cloud = self.cloud
        self.next_air_pollution = self.air_pollution
        self.next_element = self.element

    def _temperature_init(self, element):
        if element == "land":
            return 25
        if element == "sea":
            return 15
        if element == "iceburg":
            return -15
        if element == "forest":
            return 20
        if element == "city":
            return 27

    def calculate_next_gen_data(self, map):
        # calculate wind
        if self.wind_direction == "N":
            self.next_wind_direction = "W"
        if self.wind_direction == "W":
            self.next_wind_direction = "N"

        # generate pollution in cities
        if self.element == "city":
            self.next_air_pollution += self.city_pollution

        # look at neighbors that blows winds toward me
        for direction in ["N", "E", "W", "S"]:  # checking neighbors from all 4 directions
            neighbor = map.get_neighbor_cell(self.x, self.y, direction)
            if neighbor.get_wind_direction() == reverse_direction(direction): # if neighbor's wind is blowing toward me
                self.next_air_pollution += neighbor.get_air_pollution() * neighbor.get_wind_speed() # add pollution from neighbor
                # if I don't have cloud in next gen, try getting cloud from neighbor
                if self.next_cloud == None:
                    cloud_from_neighbor = neighbor.take_cloud()
                    if cloud_from_neighbor != None:
                        self.next_cloud = cloud_from_neighbor
        
        self.next_air_pollution -= self.air_pollution * self.wind_speed  # decrease pollution I'm blowing to neighbor

        # raise temperature becuase of pollution
        self.next_temperature = self.next_temperature + (map.get_pollution_heat_factor() * self.air_pollution)

        # make it rain (or not)
        if map.is_raining_today():
            if self.next_cloud != None:
                self.next_cloud = "rain_cloud"
        else:
            if self.next_cloud != None:
                self.next_cloud = "cloud"

        # decrease temperature if raining
        if self.next_cloud == "rain_cloud" and self.next_temperature > 15:   # rain doesn't decrease temperature of areas below 15 degrees
            self.next_temperature -= map.get_rain_cold_factor()


        # effect from temperature change
        if self.element == "iceburg" and self.next_temperature > 0:
            self.next_element = "sea"
        if self.element == "sea" and self.next_temperature < 0:
            self.next_element = "iceburg"
        if (self.element == "forest" or self.element == "fire2") and self.next_temperature > 40:
            self.next_element = "fire1"
        if self.element == "fire1" and self.next_temperature > 40:
            self.next_element = "fire2"
        if self.element == "city" and self.next_temperature > 50:
            self.next_element = "fire1"

    def apply_next_gen_data(self):
        self.temperature = self.next_temperature
        self.wind_speed = self.next_wind_speed
        self.wind_direction = self.next_wind_direction
        self.cloud = self.next_cloud
        self.air_pollution = self.next_air_pollution
        if self.air_pollution > 1:
            self.air_pollution = 1
        if self.air_pollution < 0:
            self.air_pollution = 0
        self.element = self.next_element

    def take_cloud(self):
        cloud_to_take = self.next_cloud
        if cloud_to_take != None:
            self.next_cloud = None
        return cloud_to_take
    
    def get_cell_text(self):
        compass_symbol_dict = {
            "N" : "\u2191",     # unicode arrow up
            "E" : "\u2192",     # unicode arrow right
            "W" : "\u2190",     # unicode arrow left
            "S" : "\u2193",     # unicode arrow down
        }

        wind_direction = compass_symbol_dict[self.wind_direction]
        temp = int(self.temperature)  # adding unicode celcius degeress symbol
        pollution = round(self.air_pollution*100, 1)
        # cloud = int(self.cloud*100)

        # text = "{} {}\u2103\n P:{}%\n C:{}%".format(wind_direction,temp, pollution, cloud)
        text = "{} {}\u2103\n P:{}%".format(wind_direction,temp, pollution)
        return text

    def get_color(self):
        if self.element == "land":
            return "#994C00"
        if self.element == "sea":
            return "#3399FF"
        if self.element == "iceburg":
            return "#CCFFFF"
        if self.element == "forest":
            return "#009900"
        if self.element == "city":
            return "#A0A0A0"
        if self.element == "fire1":
            return "#FF8000"
        if self.element == "fire2":
            return "#FF0000"

    def get_cloud(self):
        return self.cloud

    def get_cloud_color(self):
        cloud_color_dict = {
            "cloud" : "#FFFFFF",
            "rain_cloud" : "#808080",
        }
        if self.cloud != None:
            return cloud_color_dict[self.cloud]
        else:
            return None

    def get_temperature(self):
        return self.temperature

    def get_air_pollution(self):
        return self.air_pollution

    def get_wind_direction(self):
        return self.wind_direction

    def get_wind_speed(self):
        return self.wind_speed


class Map:
    def __init__(self):
        print ("creating world")
        self.rows = 15
        self.cols = 15
        self.cell_size = 50
        self.map_file = "world.dat"
        self.pollution_heat_factor = 0.7  # how much 100% pollution will raise the temperture in a day (in celsius degrees)
        slf.rain_cold_factor = 0.4       # how much will the temperature decrease when raining
        self.is_raining = Falsee

        element_map = self._read_element_map()  # reads element map file
        (self.cells, self.temperature_list, self.air_pollution_list) = self._create_cells(element_map)

        self.temperature_average = statistics.mean(self.temperature_list)
        self.air_pollution_average = statistics.mean(self.air_pollution_list)
        self.temperature_std_dev = statistics.pstdev(self.temperature_list)
        self.air_pollution_std_dev = statistics.pstdev(self.air_pollution_list)
        print("world created")

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_cell_size(self):
        return self.cell_size

    def get_temperature_average(self):
        return self.temperature_average

    def get_temperature_std_dev(self):
        return self.temperature_std_dev

    def get_air_pollution_average(self):
        return self.air_pollution_average

    def get_air_pollution_std_dev(self):
        return self.air_pollution_std_dev

    def get_pollution_heat_factor(self):
        return self.pollution_heat_factor

    def get_rain_cold_factor(self):
        return self.rain_cold_factor

    def is_raining_today(self):
        return self.is_raining

    def get_neighbor_cell(self, base_x, base_y, neighbor_direction):
        delta_x = 0
        delta_y = 0

        if neighbor_direction == "N":
            delta_y = -1

        if neighbor_direction == "E":
            delta_x = 1

        if neighbor_direction == "W":
            delta_x = -1

        if neighbor_direction == "S":
            delta_y = 1

        neighbor_x = (base_x + delta_x)%self.cols
        neighbor_y = (base_y + delta_y)%self.rows

        # print("get_neighbor_cell recieved cell ({},{}), direction={}. returned cell({},{})".format(base_x,base_y,neighbor_direction,neighbor_x,neighbor_y)) # ~~ debug print
        return self.cells[neighbor_x][neighbor_y]

    def _create_cells(self, element_map):
        print("creating cells")
        cells = create_matrix(self.rows, self.cols)
        temperature_list =  []
        air_pollution_list = []

        for y in range(self.rows):
            for x in range(self.cols):
                wind_direction = self._wind_direction_init(x,y)
                cloud = self._cloud_init(x,y)

                cell = Cell(x, y, element=element_map[x][y], wind_direction=wind_direction, cloud=cloud) 
                cells[x][y] = cell

                temperature_list += [cell.get_temperature()]
                air_pollution_list += [cell.get_air_pollution()]
        
        print("cells created")
        return (cells, temperature_list, air_pollution_list)

    def _wind_direction_init(self, x, y):
        if (x+y)%2 == 0: #מקומות זוגיים במטריצה
            wind_direction = "N"
        else:
            wind_direction = "W"#מקומות אי-זוגיים במטריצה
        return wind_direction

    def _cloud_init(self, x, y):
        nth_cell = 7   # create cloud for each n-th cell
        if (x+y)%nth_cell == 0:
            return "cloud"
        else:
            return None

    def _read_element_map(self):
        print("reading element map")
        element_map = create_matrix(self.rows, self.cols)
        
        with open(self.map_file, 'r') as f:
            for y in range(self.rows):
                for x in range(self.cols):
                    element = f.read(1)

                    while element not in ['L', 'S', 'I', 'F', 'C']:
                        element = f.read(1)
                    
                    if element == "L":
                        element_map[x][y] = "land"
                    if element == "S":
                        element_map[x][y] = "sea"
                    if element == "I":
                        element_map[x][y] = "iceburg"
                    if element == "F":
                        element_map[x][y] = "forest"
                    if element == "C":
                        element_map[x][y] = "city"
        
        print("finished reading element map")
        return element_map
 
    def update_map_to_next_gen(self, is_raining):
        self.is_raining = is_raining
        self.temperature_list = []
        self.air_pollution_list = []

        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.cells[x][y]
                cell.calculate_next_gen_data(self)

        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.cells[x][y]
                cell.apply_next_gen_data()
                self.temperature_list += [cell.get_temperature()]
                self.air_pollution_list += [cell.get_air_pollution()]
        
        self.temperature_average = statistics.mean(self.temperature_list)
        self.air_pollution_average = statistics.mean(self.air_pollution_list)
        self.temperature_std_dev = statistics.pstdev(self.temperature_list)
        self.air_pollution_std_dev = statistics.pstdev(self.air_pollution_list)


class Simulation:
    def __init__(self):
        self.refresh_rate = 30
        self.gen_num = 365  #number of cycles
        self.current_gen = 1 #begining with
        self.daily_temperature_list = []
        self.daily_air_pollution_list = []

        self.map = Map()
        self.rows = self.map.get_rows()
        self.cols = self.map.get_cols()
        self.canvas_cells = create_matrix(self.rows, self.cols)

        self.cell_size = self.map.get_cell_size()
        self.window_height = self.rows * self.cell_size
        self.window_width = self.cols * self.cell_size

        print("Creating simulation")
        self.root = tk.Tk()
        self.root.title("Maman 11 - Cellular Automaton World Simulation")
        self.lable = tk.Label(self.root, text="Generation {}".format(self.current_gen), font="bold")
        self.sub_lable = tk.Label(self.root, text=self._get_sub_label_text())
        self.lable.pack()
        self.sub_lable.pack()

        self.canvas = tk.Canvas(self.root, height=self.window_height, width=self.window_width, bg="white")
        self.canvas.pack()
        
        self._create_canvas()
        self._update_canvas()

        self.root.after(self.refresh_rate, self.move_to_next_gen) # root === window
        self.root.mainloop()

    def _create_canvas(self):
        print("creating canvas")
        cg = 0.13  # cloud_margin_gap, unit: cell size percentage
        for y in range(self.rows):
            for x in range(self.cols):
                canvas_square_id = self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, (x+1)*self.cell_size, (y+1)*self.cell_size)
                canvas_text_id = self.canvas.create_text((x+0.5)*self.cell_size, (y+0.25)*self.cell_size, font=("Ariel 8 bold"))
                canvas_cloud_id = self.canvas.create_oval((x+cg)*self.cell_size, (y+0.5+cg)*self.cell_size, (x+1-cg)*self.cell_size, (y+1-cg)*self.cell_size, width=0)
                self.canvas_cells[x][y] = (canvas_square_id, canvas_text_id, canvas_cloud_id)
        print("canvas created")

    def _update_canvas(self):
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.map.cells[x][y]
                canvas_cell_text = cell.get_cell_text()
                canvas_cell_color = cell.get_color()
                canvas_cell_cloud = cell.get_cloud_color()
                
                (canvas_square_id, canvas_text_id, canvas_cloud_id) = self.canvas_cells[x][y]
                self.canvas.itemconfig(canvas_square_id, fill=canvas_cell_color)
                self.canvas.itemconfig(canvas_text_id, text=canvas_cell_text)
                if (canvas_cell_cloud != None):
                    self.canvas.itemconfig(canvas_cloud_id, fill=canvas_cell_cloud)
                else:
                    self.canvas.itemconfig(canvas_cloud_id, fill="")   # ~~ stopped here

    def move_to_next_gen(self):
        self.daily_temperature_list += [self.map.get_temperature_average()]
        self.daily_air_pollution_list += [self.map.get_air_pollution_average()]
        if self.current_gen < self.gen_num: # didn't get to last generation
            self.current_gen += 1
            is_raining = self._decide_if_reaining_today()
            # print("simuation: calculating gen{}, is it raining today? {}".format(self.current_gen, is_raining)) # debug print ~~
            self.map.update_map_to_next_gen(is_raining)
            self._update_canvas()
            self.lable.config(text="Generation {}".format(self.current_gen))
            self.sub_lable.config(text=self._get_sub_label_text())
            self.root.after(self.refresh_rate, self.move_to_next_gen)
        else:
            self.lable.config(text="Generation {}, simulation finished!".format(self.current_gen))
        
    def _decide_if_reaining_today(self):
        is_raining = False
        rain_delta = 14          # start raining every X days, first X days won't be raining
        raining_duration = 5    # rain duration in days, needs to be <= rain_delta

        day = self.current_gen-1   # start counting days from 0

        if self.current_gen >= rain_delta and day%(rain_delta-1) in range(0, raining_duration):
            is_raining = True

        return is_raining
        
    def _get_sub_label_text(self):
        temperature_average = round(self.map.get_temperature_average(), 1)
        air_pollution_average = round(self.map.get_air_pollution_average()*100, 2) # calculate in percentage
        temperature_std_dev = round(self.map.get_temperature_std_dev(), 1)
        air_pollution_std_dev = round(self.map.get_air_pollution_std_dev()*100, 2)

        line1 = "Average temperature: {}\u2103   \t Average air Pollution: {}%\n".format(temperature_average, air_pollution_average)
        line2 = "Standart deviation: {}\u2103 \t\t Standart deviation: {}%".format(temperature_std_dev,  air_pollution_std_dev)

        return line1 + line2


if __name__ == '__main__':
    print("main is running!")

    simultaion = Simulation()

    yearly_temperature_average = statistics.mean(simultaion.daily_temperature_list)
    yearly_temperature_standart_deviation = statistics.pstdev(simultaion.daily_temperature_list)
    
    temp = open("daily_temperature.txt", "w")
    temp_n = open("daily_temperature_normalized.txt", "w")
    for item in simultaion.daily_temperature_list:
        temp.write("{}\n".format(item))
        item_normalaized = (item - yearly_temperature_average) / yearly_temperature_standart_deviation
        temp_n.write("{}\n".format(item_normalaized))
    temp.close()
    temp_n.close()

    yearly_air_pollution_average = statistics.mean(simultaion.daily_air_pollution_list)
    yearly_air_pollution_standart_deviation = statistics.pstdev(simultaion.daily_air_pollution_list)
    air_poll = open("daily_air_pollution.txt", "w")
    air_poll_n = open("daily_air_pollution_normalized.txt", "w")
    for item in simultaion.daily_air_pollution_list:
        air_poll.write("{}\n".format(item))
        item_normalaized = (item - yearly_air_pollution_average) / yearly_air_pollution_standart_deviation
        air_poll_n.write("{}\n".format(item_normalaized))
    air_poll.close()
    air_poll_n.close()

    print("main has come to an end :(")

