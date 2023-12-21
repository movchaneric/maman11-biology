import tkinter as tk
from cell import Cell

GRID_SIZE = 40
CUBE_SIZE = 24
COLOR_MAP = {
    'S': "#3399FF",   # Sea
    'I': 'white',  # Ice
    'G': '#D2B48C',  # Ground (Light brown)
    'C': 'yellow', # City
    'L': "#009900"   # Land
}

class World:   
    def __init__(self):
        self.world_map = []
        self.refresh_rate = 30 # half a second delay
        self.curr_gen = 1
        self.total_num_gen = 365
        self.canvas = None # Initialize canvas
        self.window = None

        self.create_world_map()


    #Get neighbors of a specific cell
    # return an array of Cell neighbors
    def get_neighbors(self,x, y, world):
        cell_neighbors = []
        rows = len(world)
        cols = len(world[0]) if rows > 0 else 0

        for delta_x in [-1, 0, 1]:
            for delta_y in [-1, 0, 1]:
                new_x, new_y = x + delta_x, y + delta_y
                if(delta_x == 0 and delta_y == 0) or new_x < 0 or new_y < 0 or new_x >= cols or new_y >= rows:
                    continue
                
                cell_neighbors.append(world[new_x][new_y])
        
        # print(cell_neighbors)
        return cell_neighbors
    
    def update_wind_direction(self, x, y, world_map):
        # get the cell
        print('world_map:' , world_map)
        cell = world_map[x][y]
        text_tag = f"text_{x}_{y}"
        rect_tag = f"rect_{x}_{y}"
        new_temp = self.calc_next_temp(x, y)

        self.canvas.delete(text_tag)

        print('Cell OLD direction: ', cell.get_wind_direction())
        cell.set_reverse_direction()
        print('Cell NEW direction: ', cell.get_wind_direction())
        
        # Update the canvas with the new arrow direction
        x1 = x * CUBE_SIZE
        y1 = y * CUBE_SIZE
        x2 = x1 + CUBE_SIZE
        y2 = y1 + CUBE_SIZE

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        wind_direction_icon = cell.get_wind_direction_icon()

        updated_cell_text = f"{new_temp}° {wind_direction_icon}"

        # Update the canvas with the new text
        self.canvas.create_text(center_x, center_y, text=updated_cell_text, fill='black',
                                font=('Helvetica', 10, 'bold', 'bold'), tags=f"text_{x}_{y}")
    
    # Set next gen to get the result of the next step
    def calc_next_gen(self):
        self.curr_gen += 1
        self.update_next_temp()
        self.window.after(self.refresh_rate, self.calc_next_gen)

    def calc_next_temp(self, x, y):
        if self.curr_gen <= self.total_num_gen:
            curr_cell_neighbors = self.get_neighbors(x, y, self.world_map) #array of neighbors of current cell
            new_cell_temp = 0

            for cell in curr_cell_neighbors:
                new_cell_temp += cell.get_cell_tempreture()
            
            new_cell_temp /= len(curr_cell_neighbors)

            #return new cell temp after getting its neighbors
            return new_cell_temp   

    def create_world_map(self):
        self.window = tk.Tk()
        self.window.title("Cellular Automaton World Simulation")
        self.window.resizable(False, False)

        # Create a Canvas widget
        self.canvas = tk.Canvas(self.window, width=GRID_SIZE * CUBE_SIZE, height=GRID_SIZE * CUBE_SIZE, bg="white")
        self.canvas.pack()

        #Get the content of the file 'earth.dat'
        with open('earth.dat', 'r') as file:
            file_content = file.read().replace('\n', '')

        for i in range(GRID_SIZE):
            row_cells = []
            for j in range(GRID_SIZE):
                file_cell_type = file_content[j * GRID_SIZE + i] # letter 'C', 'G', ..
                color = COLOR_MAP.get(file_cell_type, 'white') #'#D2B48C' / 'White'/ ....

                x1 = i * CUBE_SIZE
                y1 = j * CUBE_SIZE
                x2 = x1 + CUBE_SIZE
                y2 = y1 + CUBE_SIZE

                 # Create a Cell object for each grid cell
                cell = Cell(i, j,file_cell_type) #file_cell_type = 'S' ,...
                row_cells.append(cell)

                # Create a rectangle for the cell with a unique tag
                rect_tag = f"rect_{i}_{j}"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black" , tags=rect_tag)

                # Calculate the center of the cube
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                temperature_text = f"{cell.get_init_temp(file_cell_type)}°"
                wind_direction_icon = cell.get_wind_direction_icon() #get the arrow icon depend on the direction
                
                text_to_display = f"{temperature_text}{wind_direction_icon}"

                text_tag = f"text_{i}_{j}"
                self.canvas.create_text(center_x, center_y, text=text_to_display, fill='black', font=('Helvetica', 10, 'bold', 'bold'), tags=text_tag)
    
            self.world_map.append(row_cells)

        print('world map has been created...')



