CELL_TYPE_TO_TEMPERATURE_DICT = {
     'C': 25,
     'S': 15,
     'L': 30,
     'I': -10,
     'G': 45
}

CELL_TYPE_TO_WIND_DIRECTION_DICT = {
    'S': 'S',
    'L': 'N',
    'G': 'N',
    'I': 'E',
    'C': 'W'
}   

CELL_CURR_WIND_DIRECTION_TO_REVERSE_DICT = {
    'S': 'N',
    'N': 'S',
    'W': 'E',
    'E': 'W',
}

CELL_WIND_DIRECTION_TO_ICON_DICT = {
    'S': '↓',
    'N': '↑',
    'E': '→',
    'W': '←'
}

CELL_WIND_DIRECTION_TO_AXIS_VALUE_DICT = {
    'N': -1,
    'S': 1,
    'W': -1,
    'E': 1
} 

COLOR_MAP = {
    'S': "#3399FF",   # Sea
    'I': 'white',     # Ice
    'G': '#D2B48C',   # Ground (Light brown)
    'C': 'yellow',    # City
    'L': "#009900",   # Land
    'U': '#FFA500'    # Orange - unhabitable
}