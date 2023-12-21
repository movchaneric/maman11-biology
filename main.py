import tkinter as tk
from world import World

                
if __name__ == '__main__':
     main_world = World()
     main_world.update_wind_direction(39,39, main_world.world_map)
     main_world.window.mainloop()
     

             
