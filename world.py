import tkinter as tk
from cell import Cell

GRID_SIZE = 40
CUBE_SIZE = 20
COLOR_MAP = {
    'S': "#3399FF",   # Sea
    'I': 'white',  # Ice
    'G': '#D2B48C',  # Ground (Light brown)
    'C': 'yellow', # City
    'L': "#009900"   # Land
}

class World:   
    #check why doest work or why not printing cell_neighbors
    def get_neighbors(x, y, world):
        cell_neighbors = []
        rows = len(world)
        cols = len(world[0]) if rows > 0 else 0

        for delta_x in [-1, 0, 1]:
            for delta_y in [-1, 0, 1]:
                new_x, new_y = x + delta_x, y + delta_y
                if(delta_x == 0 and delta_y == 0) or new_x < 0 or new_y < 0 or new_x >= cols or new_y >= rows:
                    continue
                
                cell_neighbors.append(world[new_x][new_y])
        
        print(cell_neighbors)
        return cell_neighbors


    def create_world_map():
        window = tk.Tk()
        window.title("Cellular Automaton World Simulation")
        window.resizable(False, False)

        # Create a Canvas widget
        canvas = tk.Canvas(window, width=GRID_SIZE * CUBE_SIZE, height=GRID_SIZE * CUBE_SIZE, bg="white")
        canvas.pack()

        #Get the content of the file 'earth.dat'
        with open('earth.dat', 'r') as file:
            file_content = file.read().replace('\n', '')

        world_map = []

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
                cell = Cell(i, j,file_cell_type, file_cell_type) #file_cell_type = 'S' ,
                row_cells.append(cell)

                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Calculate the center of the cube
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                canvas.create_text(center_x, center_y, text=f"{cell.get_init_temp(file_cell_type)}°C", fill='black', font=('Helvetica', 8, 'bold'))
    
            world_map.append(row_cells)
        
        window.mainloop()



