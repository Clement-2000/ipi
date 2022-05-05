"""
def getNextElements(element):
    return {
        "top" : None,
        "bottom" : None,
        "left" : None,
        "rignt" : None
    }

def getElementType(element): 
    return None

def getElementCoords(element):
    return (element["x"], element["y"])

def isConnectedByRoad(element_a, element_b):
    timeout = 15
    n_cycles = 0

    road = []

    lastSide = None

    nextElements = getNextElements(element_a)

    while n_cycles < timeout :
        if lastSide != None :
            del nextElements[lastSide]
            
        for side, element in : 
            if element == element_b:
                return road
            elif getElementType(element) == "road":
                road.append(getElementCoords(element))
                pass
        return False
    
    return False
"""

case = {
    "type" : "route",
    "x" : 10, 
    "y" : 5
}

cursor = {
    "x" = 1,
    "y" = 1,
}

env_world = [
    ["A", "B", "C"],
    [None, None, None],
    ["D", None, None],
    ["D", None, None]
]

GRID_WIDTH = 5
GRID_HEIGHT = 3

GRAPHICS = {
    "A" = 
}

def render(world): 
    for y in range(len(world)):
        line_string = ""
        for x in range(len(world[y])):
            grid_element = world[y][x]
            if grid_element == None : 
                char = " "
            else :
                char = grid_element
            
            line_string += char*GRID_WIDTH
        line_string += "\n"
        line_string *= GRID_HEIGHT
        print(line_string)

render(env_world)