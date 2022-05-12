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
        
        self._loaded_elements = {
            # "name" : extends AbstractGraphic
        }
        self._displayed_elements = {
            # class DisplayedElement
        }

        self._console_text = ""
        self._show_console = False

        self._display_buffer = [
            ["C", 0, 0]
        ]
    
    def getStatus(self):
        return self._status
    
    def getWidth(self):
        return self._width
    
    def getHeight(self):
        return self._height
    
    def getLoadedElements(self):
        return self._loaded_elements
    
    def getDisplayedElements(self):
        return self._displayed_elements
    
    def getConsoleText(self):
        return self._console_text
    
    def getShowConsole(self):
        return self._show_console
    
    def getDisplayBuffer(self):
        return self._display_buffer
    
    def start(self): 
        sys.stdout.write("\033[s\033[?47h\033[2J\033[H")
        sys.stdout.flush()
        self._status = True
    
    def end(self): 
        sys.stdout.write("\033[?47l\033[u")
        sys.stdout.flush()
        self._status = False
    
    def clearBuffer(self):
        self._display_buffer = [[[" ", 0, 0]] * self._width] * self._height
    
    def loadGraphic(self, name, element):
        self._loaded_elements[name] = element
    
    def unloadGraphic(self, name):
        del self._loaded_elements[name]
    
    def addElement(self, element_name):
        pass
    
    def update(self):
        self._width  = os.get_terminal_size()[0]
        self._height = os.get_terminal_size()[1]
        self.clearBuffer()
        for element in self._displayed_elements():
            loaded_element = self._loaded_elements[element.name]
            if element.x + loaded_element.width > 0 and element.y + loaded_element.height > 0 \
               and element.x < self._width and element.y < self.height :
                truncate_left = 0
                truncate_right = 0
                truncate_top = 0
                truncate_bottom = 0
                if element.x < 0 : 
                    truncate_left = -element.x
                if element.y < 0 : 
                    truncate_top = -element.y 
                if element.x + element.width > self._width:
                    truncate_right = element.x + element.width - self._width
                if element.y + element.height > self._height:
                    truncate_bottom = element.y + element.height - self._height
                
                for y in range(truncate_top, element.height - truncate_bottom):
                    global_y = y + element.y
                    for x in range(truncate_left, element.width - truncate_right):
                        global_x = x + element.x

                        self._display_buffer[global_y][global_x] = loaded_element[y][x]

    def showConsole(self):
        self._show_console = True
    
    def hideConsole(self):
        self._show_console = False
    
    def print(self, text, end="\n"):
        self._console_text += text + end
    
    def clearConsole(self):
        self._console_text = ""

    def getDisplaySize(self):
        return (self._width, self._height)

class DisplayedElement():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.graphic = None

class AbstractGraphic():
    def __init__(self): 
        self.width = 0
        self.height = 0
    
    def getGraphic(self):
        pass

class FileGraphic(AbstractGraphic):
    def __init__(self, file_path): 
        super().__init__()
        self._file_path = file_path
    
    def getGraphic(self):
        with open(self._file_path, "rb") as file : 
            data = file.read()
            graphic = [[]]
            file_len = round((len(data)-len(data)%7)/7)
            for cursor in range(file_len) :
                
                char_data = data[cursor*7:(cursor+1)*7]
                extra_data = ord(char_data[6:7])
                
                graphic[-1].append([
                    char_data[:4].decode("utf-32"), 
                    ord(char_data[4:5]), 
                    ord(char_data[5:6]),
                    bool(extra_data >> 1 & 1),
                    bool(extra_data >> 2 & 1)
                ])

                if bool(extra_data >> 0 & 1) and cursor < file_len - 1  :
                    graphic.append([])
        
        self.width = len(graphic[0])
        self.height = len(graphic)
        
        return graphic

class BoxGraphic(AbstractGraphic):
    def __init__(self, width, height, background_color, foreground_color, style): 
        super().__init__()
        self.width = width
        self.height = height
        self._foreground_color = foreground_color
        self._background_color = background_color
        self._style = style
    
    def getGraphic(self):
        graphic = [[[BOX_STYLES[self._style][0], self._background_color, self._foreground_color, False, False]] + [[BOX_STYLES[self._style][1], self._background_color, self._foreground_color, False, False]] * (self.width-2) + [[BOX_STYLES[self._style][2], self._background_color, self._foreground_color, False, False]]] + \
                  [[[BOX_STYLES[self._style][3], self._background_color, self._foreground_color, False, False]] + [[BOX_STYLES[self._style][4], self._background_color, self._foreground_color, False, False]] * (self.width-2) + [[BOX_STYLES[self._style][5], self._background_color, self._foreground_color, False, False]]] * (self.height - 2) + \
                  [[[BOX_STYLES[self._style][6], self._background_color, self._foreground_color, False, False]] + [[BOX_STYLES[self._style][7], self._background_color, self._foreground_color, False, False]] * (self.width-2) + [[BOX_STYLES[self._style][8], self._background_color, self._foreground_color, False, False]]]
        return graphic
