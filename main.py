import tkinter as tk
from world import World

main_world = World
                
if __name__ == '__main__':
    main_world.create_world_map()
    main_world.get_neighbors(5,5, main_world)
    print("program is running")                
