  #  ----------- PRINT TESTS -----------
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
        
def test_cell_pollution(self):
    for row in self.world_map:
        for cell in row:
            print(f"[{cell.y}][{cell.x}] , Pol: {cell.pollution} , temp: {cell.tempreture}|", end =" ")
        print('\n')

def print_specific_cell_pollution_and_temp(self, x: int, y:int, world_map):
    cell = world_map[y][x]
    print(f"cell Temp: {cell.tempreture} | Pollution: {cell.pollution}" )