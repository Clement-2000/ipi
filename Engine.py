import sys, os, termios

debug_file = open("debug.txt", "a")

def debug(text, end:str="\n"):
    debug_file.write(str(text) + end)

BOX_STYLES = [
    "┌─┐│ │└─┘",
    "┌╌┐╎ ╎└╌┘",
    "╭─╮│ │╰─╯",
    "╭╌╮╎ ╎╰╌╯",
    "┏━┓┃ ┃┗━┛",
    "┏╍┓╏ ╏┗╍┛",
    "╔═╗║ ║╚═╝"
]

class Display():
    def __init__(self):
        self._status = False
        self._width = 0
        self._height = 0

        self._console_text = ""
        self._show_console = False

        self._loaded_graphics = {}
        self._displayed_elements = {}

        self._display_buffer = []
        self._string_buffer = ""
    
    def getStatus(self) -> bool:
        return self._status
    
    def getWidth(self) -> int:
        return self._width
    
    def getHeight(self) -> int:
        return self._height
    
    def getLoadedElements(self) -> dict:
        return self._loaded_elements
    
    def getDisplayedElements(self) -> dict:
        return self._displayed_elements
    
    def getConsoleText(self) -> str:
        return self._console_text
    
    def getShowConsole(self) -> bool:
        return self._show_console
    
    def getDisplayBuffer(self) -> list:
        return self._display_buffer
    
    def getStringBuffer(self) -> str: 
        return self._buff
    
    def start(self) -> None: 
        fd = sys.stdin.fileno()
        new = termios.tcgetattr(fd)
        new[3] &= ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, new)

        sys.stdout.write("\33[s\33[?47h\33[2J\33[H")
        sys.stdout.flush()

        self._status = True
    
    def end(self) -> None: 
        sys.stdout.write("\33[?47l\33[u")
        sys.stdout.flush()
        
        fd = sys.stdin.fileno()
        new = termios.tcgetattr(fd)
        new[3] |= termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, new)

        self._status = False
    
    def clearBuffer(self) -> None:
        self._display_buffer = [[[" ", 0, 0]] * self._width] * self._height
        self._string_buffer = ""
    
    def loadGraphic(self, name, element :str) -> None:
        self._loaded_graphics[name] = element
    
    def unloadGraphic(self, graphic_name :str) -> None:
        del self._loaded_graphics[graphic_name]
    
    def addElement(self, name :str, graphic_name :str, x :int, y :int) -> None:
        self._displayed_elements[name] = DisplayedElement(graphic_name, x, y)
    
    def moveElement(self, name :str, new_x :int, new_y :int) -> None:
        self._displayed_elements[name].x = new_x
        self._displayed_elements[name].y = new_y
    
    def shitElement(self, name :str, shift_x :int, shift_y :int) -> None:
        self._displayed_elements[name].x += shift_x
        self._displayed_elements[name].y += shift_y
    
    def replaceElement(self, name :str, new_graphic_name :str) -> None:
        self._displayed_elements[name].graphic_name = new_graphic_name
    
    def removeElement(self, name :str) -> None:
        del self._displayed_elements[name]
    
    def update(self) -> None:
        self._width  = os.get_terminal_size()[0]
        self._height = os.get_terminal_size()[1]
        self.clearBuffer()
        for element_name in self._displayed_elements:
            element = self._displayed_elements[element_name]
            loaded_element = self._loaded_graphics[element.graphic_name]
            
            if element.x + loaded_element.width > 0 and element.y + loaded_element.height > 0 \
               and element.x < self._width and element.y < self._height :
                truncate_left = 0
                truncate_right = 0
                truncate_top = 0
                truncate_bottom = 0
                if element.x < 0 : 
                    truncate_left = -element.x
                if element.y < 0 : 
                    truncate_top = -element.y 
                if element.x + loaded_element.width > self._width:
                    truncate_right = element.x + loaded_element.width - self._width
                if element.y + loaded_element.height > self._height:
                    truncate_bottom = element.y + loaded_element.height - self._height

                for y in range(truncate_top, loaded_element.height - truncate_bottom):

                    global_y = y + element.y

                    for x in range(truncate_left, loaded_element.width - truncate_right):
                        global_x = x + element.x

                        self._display_buffer[global_y][global_x] = loaded_element.getGraphic()[y][x][:3]
        
        """
        for y in range(self._height):
            for x in range(self._width):
                char = self._display_buffer[y][x]
                self._string_buffer += f"\33[38;5;{char[1]}m\33[48;5;{char[2]}m{char[0]}"

            self._string_buffer += "\n"
        self._string_buffer = self._string_buffer[:-1]

        sys.stdout.write(self._string_buffer)
        sys.stdout.write("\33 [ 1 ; 1 H")
        """

    def showConsole(self) -> None:
        self._show_console = True
    
    def hideConsole(self) -> None:
        self._show_console = False
    
    def print(self, text :str, end :str ="\n") -> None:
        self._console_text += text + end
    
    def clearConsole(self) -> None:
        self._console_text = ""

class DisplayedElement():
    def __init__(self, graphic_name :str, x :int, y :int):
        self.x = x
        self.y = y
        self.graphic_name = graphic_name

class AbstractGraphic():
    def __init__(self): 
        self.width = 0
        self.height = 0
        self._graphic = []
    
    def getGraphic(self) -> list:
        return self._graphic

class FileGraphic(AbstractGraphic):
    def __init__(self, file_path :str): 
        super().__init__()
        self._file_path = file_path

        with open(self._file_path, "rb") as file : 
            data = file.read()
            self._graphic = [[]]
            file_len = round((len(data)-len(data)%7)/7)
            for cursor in range(file_len) :
                
                char_data = data[cursor*7:(cursor+1)*7]
                extra_data = ord(char_data[6:7])
                
                self._graphic[-1].append([
                    char_data[:4].decode("utf-32"), 
                    ord(char_data[4:5]), 
                    ord(char_data[5:6]),
                    bool(extra_data >> 1 & 1),
                    bool(extra_data >> 2 & 1)
                ])

                if bool(extra_data >> 0 & 1) and cursor < file_len - 1  :
                    self._graphic.append([])
        
        self.width = len(self._graphic[0])
        self.height = len(self._graphic)

class BoxGraphic(AbstractGraphic):
    def __init__(self, width :int, height :int, background_color :int, foreground_color :int, style :int): 
        super().__init__()
        self.width = width
        self.height = height
        self._foreground_color = foreground_color
        self._background_color = background_color
        self._style = style
    
        self._graphic = [[[BOX_STYLES[self._style][0], self._background_color, self._foreground_color, False, False]] + [[BOX_STYLES[self._style][1], self._background_color, self._foreground_color, False, False]] * (self.width-2) + [[BOX_STYLES[self._style][2], self._background_color, self._foreground_color, False, False]]] + \
                        [[[BOX_STYLES[self._style][3], self._background_color, self._foreground_color, False, False]] + [[BOX_STYLES[self._style][4], self._background_color, self._foreground_color, False, False]] * (self.width-2) + [[BOX_STYLES[self._style][5], self._background_color, self._foreground_color, False, False]]] * (self.height - 2) + \
                        [[[BOX_STYLES[self._style][6], self._background_color, self._foreground_color, False, False]] + [[BOX_STYLES[self._style][7], self._background_color, self._foreground_color, False, False]] * (self.width-2) + [[BOX_STYLES[self._style][8], self._background_color, self._foreground_color, False, False]]]
