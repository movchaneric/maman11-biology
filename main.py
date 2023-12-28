
from world import World

                
if __name__ == '__main__':
     refresh_rate = 250
     starting_gen = 1
     last_gen = 365
     pollution_factor = 5 # 0 - no pollution, 2.5 - mid pollution , 5 - high pollution
     main_world = World(refresh_rate, starting_gen, last_gen, pollution_factor)
     

             