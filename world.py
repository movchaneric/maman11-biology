import tkinter as tk
from copy import deepcopy
from cell import Cell

import constants as consts
import cell_properties as cp

from typing import List, Optional

GRID_SIZE = 40
CUBE_SIZE = 24

# TODO: canvas to __canvas + set init vals in main func
class World:
    # def __init__(self, world_map, refresh_rate, start_gen, last_gen, world_size):

    def __init__(self):
        self.world_map: List[List[Cell]] = list()
        self.refresh_rate = 1000 # in ms
        self.curr_gen = 1
        self.total_num_gen = 365
        self.canvas = None # Initialize canvas
        self.window = None
        self.world_size = consts.GRID_SIZE
        self.create_world_map()

    
    def get_cell_by_coordinate(self, x: int, y: int) -> Cell:
        return self.world_map[y][x]
    

    def draw_next_gen_canvas(self):
        #Get the content of the file 'earth.dat'
        with open('earth.dat', 'r') as file:
            file_content = file.read().replace('\n', '')
        
        # world_map doesnt exists
        if len(self.world_map) == 0:
            for i in range(GRID_SIZE):
                row_cells = []
                for j in range(GRID_SIZE):
                    file_cell_type = file_content[j * GRID_SIZE + i]
                    
                    cell = Cell(j, i,file_cell_type)
                    row_cells.append(cell)    
                self.world_map.append(row_cells)    
        #exists => remove canvas to redraw                     
        if self.canvas:
            self.canvas.delete('all')
            
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                file_cell_type = file_content[col * GRID_SIZE + row]
                color = cp.COLOR_MAP[file_cell_type]

                x1 = row * CUBE_SIZE
                y1 = col * CUBE_SIZE
                x2 = x1 + CUBE_SIZE
                y2 = y1 + CUBE_SIZE

                # Create a rectangle for the cell with a unique tag
                rect_tag = f"rect_{row}_{col}"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags=rect_tag)

                # Calculate the center of the cube
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                
                cell = self.world_map[row][col]
                
                temperature_text = f"{cell.tempreture}°"
                wind_direction_icon = cp.CELL_WIND_DIRECTION_TO_ICON_DICT[cell.wind_direction]

                text_to_display = f"{temperature_text}{wind_direction_icon}"

                text_tag = f"text_{row}_{col}"
                
                self.canvas.create_text(center_x, center_y, text=text_to_display, fill='black',
                                        font=('Helvetica', 10, 'bold', 'bold'), tags=text_tag)
                  
    #Get neighbors of a specific cell
    #return an array of Cell neighbors
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
        cell = world_map[x][y]
        text_tag = f"text_{x}_{y}"
        rect_tag = f"rect_{x}_{y}"
        # new_temp = self.calc_next_temp(x, y)
        new_temp = 0
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
    
    # get cell neighbor correspond to wind direction
    def get_neighbor_cell_by_wind(self, c: Cell) -> Optional[Cell]:

       coordiante_val_to_shift: int = c.x if c.wind_on_x else c.y
       
       new_val: int = coordiante_val_to_shift + cp.CELL_WIND_DIRECTION_TO_AXIS_VALUE_DICT[c.wind_direction]

       new_val_is_within_world_limits: bool = (new_val >= 0) and (new_val < GRID_SIZE)

       if new_val_is_within_world_limits:
         return self.get_cell_by_coordinate(new_val, c.y) if c.wind_on_x else self.get_cell_by_coordinate(c.x, new_val)
       
       return None


    def calc_next_gen_temp(self):

        next_gen_map: List[List[Cell]] = \
            [[None for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.world_map[row][col]
                next_gen_map[row][col] = deepcopy(cell)
                curr_cell_is_city: bool = cell.cell_type == 'C'

                affected_cell = \
                    deepcopy(self.get_neighbor_cell_by_wind(cell)) if curr_cell_is_city else None

                if affected_cell:
                    # affected_cell = self.create_copy_of_cell(neighbor_cell) if neighbor_cell is not None else None
                    # if affected_cell is not None:
                    affected_cell.tempreture += 1
                    next_gen_map[affected_cell.y][affected_cell.x] = affected_cell

        self.world_map = next_gen_map
    
            
    def update_canvas(self):
        if self.curr_gen > self.total_num_gen:
            return
        
        if self.curr_gen > 1:
            self.calc_next_gen_temp()

        self.draw_next_gen_canvas()
        self.curr_gen += 1
            
        self.window.title(f"Cellular Automaton World Simulation: Generation {self.curr_gen}")    
        self.window.after(self.refresh_rate, self.update_canvas)
            


    def create_world_map(self):
        self.window = tk.Tk()
        self.window.title(f"Cellular Automaton World Simulation: Generation {self.curr_gen}")
        self.window.resizable(False, False)

        # Create a Canvas widget
        self.canvas = tk.Canvas(self.window, width=GRID_SIZE * CUBE_SIZE, height=GRID_SIZE * CUBE_SIZE + 5, bg="white")
        self.canvas.pack()

        self.draw_next_gen_canvas()
        self.print_index()

        # Schedule the initial call to draw_canvas after a delay
        self.window.after(self.refresh_rate, self.update_canvas)

        print('world map has been created...')
        
        # Start the Tkinter event loop
        self.window.mainloop()



    #  ----------- TEST -----------
    def test_print_matrix(self, world_map):
            for row in world_map:
                for cell in row:
                    print(f"cell tempreture {cell.tempreture}")
                    
    def print_matrix(self, world_map):
        print('world_map: ', world_map)
        
    def print_index(self):
        for row in self.world_map:
            for cell in row:
                print(f"[{cell.y}][{cell.x}]", end =" ")
            print('\n')