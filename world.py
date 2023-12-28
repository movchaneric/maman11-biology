import tkinter as tk
from copy import deepcopy
from typing import List, Optional
import random

from cell import Cell
import constants as consts
import cell_properties as cp

GRID_SIZE = 40
CUBE_SIZE = 28

# TODO: canvas to __canvas + set init vals in main func
class World:
    # def __init__(self, world_map, refresh_rate, start_gen, last_gen, world_size):

    def __init__(self, refresh_rate, starting_gen, last_gen, pollution_factor):
        self.world_map: List[List[Cell]] = list()
        self.canvas = None # Initialize canvas
        self.window = None
        
        self.refresh_rate = refresh_rate # in ms
        self.curr_gen = starting_gen
        self.total_num_gen = last_gen
        
        self.world_size = consts.GRID_SIZE
        self.pollution_factor = pollution_factor
        self.create_world_map()

        
    def get_cell_by_coordinate(self, x: int, y: int) -> Cell:
        return self.world_map[y][x]
    
    
    def init_map_matrix(self, file_content):
        for i in range(GRID_SIZE):
            row_cells = []
            for j in range(GRID_SIZE):
                file_cell_type = file_content[j * GRID_SIZE + i]
                color = cp.COLOR_MAP[file_cell_type]
                
                cell = Cell(j, i,file_cell_type, color)
                row_cells.append(cell)    
            self.world_map.append(row_cells) 


    def draw_next_gen_canvas(self):
        #Get the content of the file 'earth.dat'
        with open('earth.dat', 'r') as file:
            file_content = file.read().replace('\n', '')
    
        if len(self.world_map) == 0:
            self.init_map_matrix(file_content)  
    
        #exists => remove canvas to redraw                     
        if self.canvas:
            self.canvas.delete('all')
        
        for row in self.world_map:
            for cell in row:
                color = cell.color
                
                x1 = cell.y * CUBE_SIZE
                y1 = cell.x * CUBE_SIZE
                x2 = x1 + CUBE_SIZE
                y2 = y1 + CUBE_SIZE

                # Create a rectangle for the cell with a unique tag
                rect_tag = f"rect_{cell.y}_{cell.x}"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags=rect_tag)

                # Calculate the center of the cube
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                
                cell = self.world_map[cell.y][cell.x]
                
                temperature_text = f"{cell.tempreture}°"
                wind_direction_icon = cp.CELL_WIND_DIRECTION_TO_ICON_DICT[cell.wind_direction]

                # text_to_display = f"{temperature_text}{wind_direction_icon}"
                text_to_display = f"{temperature_text}"
                
                text_tag = f"text_{cell.x}_{cell.y}"
                
                self.canvas.create_text(center_x, center_y, text=text_to_display, fill='black', font=('Helvetica', 9, 'bold', 'bold'), tags=text_tag)
          

    def init_pollution_to_city_cells(self, pollution_factor):
        for row in self.world_map:
            for cell in row:
                if cell.type == 'C':
                    cell.pollution += pollution_factor
    
    # get cell neighbor correspond to wind direction
    def get_neighbor_cell_by_wind(self, c: Cell) -> Optional[Cell]:

       coordiante_val_to_shift: int = c.x if c.wind_on_x else c.y
       
       new_val: int = coordiante_val_to_shift + cp.CELL_WIND_DIRECTION_TO_AXIS_VALUE_DICT[c.wind_direction]

       new_val_is_within_world_limits: bool = (new_val >= 0) and (new_val < GRID_SIZE)

       if new_val_is_within_world_limits:
         return self.get_cell_by_coordinate(new_val, c.y) if c.wind_on_x else self.get_cell_by_coordinate(c.x, new_val)
       
       return None

  
    def passed_pollution_limit(self, c: Cell) -> bool:
        return c.pollution % 10 == 0 and c.pollution >= 10
    
    def passed_pollution_decrease_limit(self, c: Cell) -> bool:
        return c.pollution % 10 == 2 and abs(c.pollution) > 0
    
    # CURRENTLY NOT USING
    def control_temperature_change_by_pollution(self, cell: Cell) -> int:
        #check if pollution is stable 0 or 2 default values = meaning pollution_meter = 0
        #TODO: Check maybe the values of cell.pollution
        #cell.pollution % 10 == 0 or cell.pollution % 10 == 2:
        if self.pollution_factor == 0:
            return round(random.uniform(-2, 2))
        #pollution is not stable meaning pollution_meter != 0
        else:
            if cell.rain > 0:
                return -1
            else:
                return 1
    
    
    def calc_next_gen_temp(self): 
        next_gen_map: List[List[Cell]] = [[None for j in range(GRID_SIZE)] for i in range(GRID_SIZE)] #create a temp map 
            
        for row in self.world_map:
            for cell in row:
                next_gen_map[cell.y][cell.x] = deepcopy(cell) 
                
                curr_cell_is_city: bool = cell.type == 'C'
        
                affected_cell = deepcopy(self.get_neighbor_cell_by_wind(cell)) if curr_cell_is_city else None
                
                # city cell pointing to the cell that the wind directing to
                if affected_cell:
                    
                    if self.pollution_factor > 0 and affected_cell.rain > 0:   
                        self.choose_rand_option(affected_cell, next_gen_map)
                    
                    if self.pollution_factor > 0: 
                        if self.passed_pollution_limit(affected_cell):
                            affected_cell.tempreture += 1     
                            
                        affected_cell.pollution += self.pollution_factor 
                        
                        next_gen_map[affected_cell.y][affected_cell.x] = affected_cell 
                    
                    #pollution is stable
                    elif self.pollution_factor == 0: 
                        affected_cell.tempreture = round(random.uniform(-2, 1))
                        
                        next_gen_map[affected_cell.y][affected_cell.x] = affected_cell 
                     
                    
                           
                # To propagate the pollution use the neighbor of cell
                neighbor = self.get_neighbor_cell_by_wind(cell)
                
                if neighbor:
                    
                    if self.pollution_factor > 0 and neighbor.rain > 0:
                        self.choose_rand_option(neighbor, next_gen_map)

                    elif self.pollution_factor > 0:
                        if self.passed_pollution_limit(neighbor):
                            neighbor.tempreture += 1
                            
                        neighbor.pollution += self.pollution_factor
                    
                        next_gen_map[neighbor.y][neighbor.x] = neighbor
                        
                    elif self.pollution_factor == 0:
                        neighbor.tempreture += round(random.uniform(-1, 1))
                        
                        next_gen_map[neighbor.y][neighbor.x] = neighbor
                          
                         
        self.world_map = next_gen_map
    
    
    def choose_rand_option(self, cell: Cell, next_gen_map):
        option = random.choice([1, 2])
        if option == 1:
            if self.passed_pollution_decrease_limit(cell):
                            cell.tempreture -= 2            
            cell.pollution -= self.pollution_factor
            next_gen_map[cell.y][cell.x] = cell 
        
        if option == 2:
            if self.passed_pollution_limit(cell):
                            cell.tempreture += 1            
            cell.pollution += self.pollution_factor
            next_gen_map[cell.y][cell.x] = cell 
    
    
    def update_map_colors(self):
        for row in self.world_map:
            for cell in row:
                updated_cell = self.change_cell_type_with_temp(cell)

                if cell.type == 'I':
                    cell.color = cp.COLOR_MAP['I']
                elif cell.type == 'L':
                    cell.color = cp.COLOR_MAP['L']
                elif cell.type == 'G':
                    cell.color = cp.COLOR_MAP['G']
                elif cell.type == 'S':
                    cell.color = cp.COLOR_MAP['S']
                elif cell.type == 'U':
                    cell.color = cp.COLOR_MAP['U']
                
            self.world_map[cell.x][cell.y] = updated_cell
                
            
    def change_cell_type_with_temp(self, c: Cell) -> Cell:
        if c.type == 'I':
            if c.tempreture >= 0 and c.tempreture < 25:
                c.type = 'S'
            elif c.tempreture >= 25 and c.tempreture < 45:
                c.type = 'L'
            elif c.tempreture > 45:
                c.type = 'G'
        
        elif c.type == 'S':
            if c.tempreture >= 45:
                c.type = 'G'
                
        elif c.type == 'L':
            if c.tempreture >= 45 and c.tempreture < 60:
                c.type = 'G'
            elif c.tempreture >= 60:
                c.type = 'U'
        
        elif c.type == 'C':
            if c.tempreture >= 45 and c.tempreture < 60:
                c.type = 'G'
            elif c.tempreture >= 60:
                c.type = 'U'
        
        elif c.type == 'G':
            if c.tempreture >= 60:
                c.type = 'U'
        
        return c

    
    def update_canvas(self):
        if self.curr_gen > self.total_num_gen:
            return
        
        if self.curr_gen > 1:
            self.calc_next_gen_temp()
            self.update_map_colors()
            self.draw_next_gen_canvas()
        
        self.curr_gen += 1
            
        self.window.title(f"Cellular Automaton World Simulation: Generation {self.curr_gen},  Pollution: {self.pollution_factor}")   
        self.window.after(self.refresh_rate, self.update_canvas)
            
                  
    def create_world_map(self):
        self.window = tk.Tk()
        self.window.title(f"Cellular Automaton World Simulation: Generation {self.curr_gen} , Pollution: {self.pollution_factor}")
        # self.window.resizable(False, False)

        # Create a Canvas widget
        self.canvas = tk.Canvas(self.window, width=GRID_SIZE * CUBE_SIZE, height=GRID_SIZE * CUBE_SIZE + 5, bg="white")
        self.canvas.pack()

        self.draw_next_gen_canvas()
        self.init_pollution_to_city_cells(2) 

        # Schedule the initial call to draw_canvas after a delay
        self.window.after(self.refresh_rate, self.update_canvas)

        print('world map has been created...')
        
        # Start the Tkinter event loop
        self.window.mainloop()


