import os, sys

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
    
    def addElement(self, element_name)
    
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
