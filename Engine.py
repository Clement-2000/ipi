import time
import sys
import os
import termios
import asyncio
import pynput

with open("debug.txt", "w") as debug_file:
    debug_file.write("")

debug_file = open("debug.txt", "a")

def debug(text, end:str="\n"):
    debug_file.write(str(text) + end)
    debug_file.flush()

BOX_STYLES = [
    "         ",
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
        self._width  = os.get_terminal_size()[0]
        self._height = os.get_terminal_size()[1]

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
        self.purge()

        sys.stdout.write("\33[?47l\33[u")
        sys.stdout.flush()
        
        fd = sys.stdin.fileno()
        new = termios.tcgetattr(fd)
        new[3] |= termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, new)

        self._status = False
    
    def clear(self):
        self._displayed_elements = {}
    
    def purge(self):
        self._console_text = ""
        self._show_console = False

        self._loaded_graphics = {}
        self._displayed_elements = {}

        self._display_buffer = []
        self._string_buffer = ""
    
    def clearBuffer(self) -> None:
        self._display_buffer = [[[" ", 0, 0] for _ in range(self._width)] for __ in range(self._height)]
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
    
    def shiftElement(self, name :str, shift_x :int, shift_y :int) -> None:
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
            graphic = loaded_element.getGraphic()
            
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
                
                loop_x = range(truncate_left, loaded_element.width - truncate_right)
                loop_y = range(truncate_top, loaded_element.height - truncate_bottom)

                for y in loop_y:
                    global_y = y + element.y

                    for x in loop_x:
                        global_x = x + element.x

                        self._display_buffer[global_y][global_x] = graphic[y][x][:3]
        
        self._string_buffer = "\n".join("".join(f"\33[38;5;{char[1]}m\33[48;5;{char[2]}m{char[0]}" for char in line) for line in self._display_buffer)

        sys.stdout.write(self._string_buffer)

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

class EventHandler():
    def __init__(self):
        self._init_clock = 0
        self._clock = 0
        self._last_loop_clock = 0
        self._loop_count = 0
        self._event_buffer = {}
        self._events = {}
        self._loop = True
    
    def keyboardUpdate(self):
        pass

    def addEvent(self, name :str, event :Event) -> None:
        # delay [delay millisecs]
        # repeat [gap millisecs, delay millisecs, number, ]
        # key_down [keys, gap millisecs]
        # key_press [keys, is_down]
        # loop
        self._event_buffer[name] = Event(trigger, options, action, args)

    def removeEvent(self, name :str) -> None:
        del self._event_buffer[name]
    
    def updateEvents(self):
        self._events = self._event_buffer.copy()

    async def main(self):

        self._init_clock = self._clock = round(time.time()*1000)

        self.updateEvents()
        for event_name, event in self._events.items(): 
            if event.trigger == "start":
                event.action(EventFiringInfo(self._init_clock, self._clock, self._loop_count, event.loop_count, event.args))
                self.removeEvent(event_name)

        self._clock = self._last_loop_clock = round(time.time()*1000)

        while self._loop : 
            self._clock = round(time.time()*1000)
            time_gap = self._clock - self._last_loop_clock

            self.updateEvents()
            for event_name, event in self._events.items(): 
                if event.trigger == "loop":
                    event.action(EventFiringInfo(self._init_clock, self._clock, self._loop_count, event.loop_count, event.args))

                elif event.trigger == "repeat":
                    event.options[1] -= time_gap
                    if event.options[1] <= 0 : 
                        event.action(EventFiringInfo(self._init_clock, self._clock, self._loop_count, event.loop_count, event.args))
                        event.options[1] = event.options[0]
                        if event.options[2] > 1 :
                            event.options[2] -= 1
                        elif event.options[2] == 1 :
                            self.removeEvent(event_name)
                
                elif event.trigger == "delay":
                    event.options[0] -= time_gap
                    if event.options[0] <= 0 : 
                        event.action(EventFiringInfo(self._init_clock, self._clock, self._loop_count, event.loop_count, event.args))
                        self.removeEvent(event_name)

                elif event.trigger == "delay" and event.options[0]:
                    event.action()
                    self.removeEvent(event_name)

            await asyncio.sleep(0.04)

            self._loop_count += 1
            self._last_loop_clock = self._clock
        
        self.updateEvents()
        for event_name, event in self._events.items(): 
            if event.trigger == "end":
                event.action(EventFiringInfo(self._init_clock, self._clock, self._loop_count, event.loop_count, event.args))
            
    def end(self):
        self._loop = False

class Event():
    def __init__(self, trigger :str, options :list, action :callable, args = None):
        self.trigger = trigger
        self.options = options
        self.action = action
        self.loop_count = 0
        self.args = args

class EventFiringInfo():
    def __init__(self, init_clock :int, clock :int, loop_count :int, event_loop_count :int, args):
        self.init_clock = init_clock
        self.clock = clock
        self.loop_count = loop_count
        self.event_loop_count = event_loop_count
        self.args = args

class Engine():
    def __init__(self):
        self.event_handler = EventHandler()

    def test(self, e):
        print("Test")

    def end(self, e):
        self.event_handler.end()
    
    def printEnd(self, e):
        print("END")

    async def main(self):

        self.event_handler.addEvent("test_event", "start", [], self.test)
        self.event_handler.addEvent("end_test", "end", [], self.printEnd)

        task = asyncio.create_task(self.event_handler.main())

        self.event_handler.addEvent("test", "repeat", [1000, 0, 0], self.test)
        self.event_handler.addEvent("end", "delay", [900], self.end)

        await task
    
    def run(self):
        asyncio.run(self.main())