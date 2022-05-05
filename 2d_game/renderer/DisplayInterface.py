import os
from PIL import ImageColor
import math
import random
import sys

class TerminalDisplayInterface():
    def __init__(self):
        self._status = False
        self._width  = os.get_terminal_size()[0]
        self._height = os.get_terminal_size()[1]
        
        self._loaded_elements = {}
        self._elements = [
            ["name", x, y]
        ]

        self._console_text = ""
        self._show_console = False

        self._display_buffer = [
            ["C", 0, 0],
        ]
    
    def start(self): 
        sys.stdout.write("\033[s\033[?47h\033[2J\033[H")
        sys.stdout.flush()
        self._status = True
    
    def end(self): 
        sys.stdout.write("\033[?47l\033[u")
        sys.stdout.flush()
        self._status = False

    def exit(self):
        self.end()
        exit()
    
    def clearBuffer(self):
        self._display_buffer = [" " * self._width for n in range(self.height)]
    
    def update(self):
        self.clearBuffer()
        for element in self._elements():
            loaded_element = self._loaded_elements[element.name]
            if element.x + loaded_element.width > 0 and element.y + loaded_element.height > 0 \
               and element.x < self._width and element.y < self.height :
               pass
    
    def exitWithError(self, stacktrace):
        self.end()
        print(stacktrace)
        exit()
    
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