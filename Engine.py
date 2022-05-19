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

class Display():
    def __init__(self):
        self.status = False
        self.width  = os.get_terminal_size()[0]
        self.height = os.get_terminal_size()[1]

        self.loaded_graphics = {}
        self.displayed_elements = []

        self.display_buffer = []
        self.string_buffer = ""

        self.BOX_STYLES = [
            "         ",
            "┌─┐│ │└─┘",
            "┌╌┐╎ ╎└╌┘",
            "╭─╮│ │╰─╯",
            "╭╌╮╎ ╎╰╌╯",
            "┏━┓┃ ┃┗━┛",
            "┏╍┓╏ ╏┗╍┛",
            "╔═╗║ ║╚═╝"
        ]
    
    def start(self) -> None: 
        sys.stdout.write("\33[s\33[?47h\33[2J\33[H")
        sys.stdout.flush()

        self.status = True
    
    def end(self) -> None: 
        self.purge()

        sys.stdout.write("\33[?47l\33[u")
        sys.stdout.flush()

        self.status = False
    
    def clear(self):
        self.displayed_elements = {}
    
    def purge(self):
        self.loaded_graphics = {}
        self.displayed_elements = []

        self.display_buffer = []
        self.string_buffer = ""
    
    def clearBuffer(self) -> None:
        self.display_buffer = [[[" ", 0, 0] for _ in range(self.width)] for __ in range(self.height)]
        self.string_buffer = ""
    
    def loadGraphic(self, name, element :str) -> None:
        self.loaded_graphics[name] = element
    
    def unloadGraphic(self, graphic_name :str) -> None:
        del self.loaded_graphics[graphic_name]
    
    def addElement(self, element) -> None:
        self.displayed_elements.append(element)
    
    def removeElement(self, element) -> None:
        if element in self.displayed_elements : 
            self.displayed_elements.remove(element)
    
    def update(self) -> None:
        self.width  = os.get_terminal_size()[0]
        self.height = os.get_terminal_size()[1]
        self.clearBuffer()
        for element_name in self.displayed_elements:
            element = self.displayed_elements[element_name]
            loaded_element = self.loaded_graphics[element.graphic_name]
            graphic = loaded_element.graphic
            
            if element.x + loaded_element.width > 0 and element.y + loaded_element.height > 0 \
               and element.x < self.width and element.y < self.height :
                truncate_left = 0
                truncate_right = 0
                truncate_top = 0
                truncate_bottom = 0
                if element.x < 0 : 
                    truncate_left = -element.x
                if element.y < 0 : 
                    truncate_top = -element.y 
                if element.x + loaded_element.width > self.width:
                    truncate_right = element.x + loaded_element.width - self.width
                if element.y + loaded_element.height > self.height:
                    truncate_bottom = element.y + loaded_element.height - self.height
                
                loop_x = range(truncate_left, loaded_element.width - truncate_right)
                loop_y = range(truncate_top, loaded_element.height - truncate_bottom)

                for y in loop_y:
                    global_y = y + element.y

                    for x in loop_x:
                        global_x = x + element.x

                        self.display_buffer[global_y][global_x] = graphic[y][x][:3]
        
        self.string_buffer = "\n".join("".join(f"\33[38;5;{char[1]}m\33[48;5;{char[2]}m{char[0]}" for char in line) for line in self.display_buffer)

        sys.stdout.write(self.string_buffer)

class DisplayElement():
    def __init__(self, graphic_name :str, x :int, y :int):
        self.x = x
        self.y = y
        self.graphic_name = graphic_name

class AbstractGraphic():
    def __init__(self): 
        self.width = 0
        self.height = 0
        self.graphic = []

class FileGraphic(AbstractGraphic):
    def __init__(self, file_path :str): 
        super().__init__()
        self.file_path = file_path

        with open(self.file_path, "rb") as file : 
            data = file.read()
            self.graphic = [[]]
            file_len = round((len(data)-len(data)%7)/7)
            for cursor in range(file_len) :
                
                char_data = data[cursor*7:(cursor+1)*7]
                extra_data = ord(char_data[6:7])
                
                self.graphic[-1].append([
                    char_data[:4].decode("utf-32"), 
                    ord(char_data[4:5]), 
                    ord(char_data[5:6]),
                    bool(extra_data >> 1 & 1),
                    bool(extra_data >> 2 & 1)
                ])

                if bool(extra_data >> 0 & 1) and cursor < file_len - 1  :
                    self.graphic.append([])
        
        self.width = len(self.graphic[0])
        self.height = len(self.graphic)

class BoxGraphic(AbstractGraphic):
    def __init__(self, width :int, height :int, background_color :int, foreground_color :int, style :int): 
        super().__init__()
        self.width = width
        self.height = height
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.style = style
    
        self.graphic = [[[self.BOX_STYLES[self.style][0], self.background_color, self.foreground_color, False, False]] + [[self.BOX_STYLES[self.style][1], self.background_color, self.foreground_color, False, False]] * (self.width-2) + [[self.BOX_STYLES[self.style][2], self.background_color, self.foreground_color, False, False]]] + \
                       [[[self.BOX_STYLES[self.style][3], self.background_color, self.foreground_color, False, False]] + [[self.BOX_STYLES[self.style][4], self.background_color, self.foreground_color, False, False]] * (self.width-2) + [[self.BOX_STYLES[self.style][5], self.background_color, self.foreground_color, False, False]]] * (self.height - 2) + \
                       [[[self.BOX_STYLES[self.style][6], self.background_color, self.foreground_color, False, False]] + [[self.BOX_STYLES[self.style][7], self.background_color, self.foreground_color, False, False]] * (self.width-2) + [[self.BOX_STYLES[self.style][8], self.background_color, self.foreground_color, False, False]]]

class Event():
    def __init__(self, priority :int, trigger :str, options :list, action :callable, args = None):
        self.priority = trigger
        self.trigger = trigger
        self.options = options
        self.action = action
        self.args = args

        self.loop_count = 0

class EventFiringInfo():
    def __init__(self, init_clock :int, clock :int, loop_count :int, event_loop_count :int, args):
        self.init_clock = init_clock
        self.clock = clock
        self.loop_count = loop_count
        self.event_loop_count = event_loop_count
        self.args = args

class EventHandler():
    def __init__(self):
        self.init_clock = 0
        self.clock = 0
        self.last_loop_clock = 0
        self.loop_count = 0
        self.events_to_add = []
        self.events_to_delete = []
        self.events = []
        self.loop = True

    def addEvent(self, event :Event) -> None:
        self.events_to_add.append(event)

    def removeEvent(self, event :Event) -> None:
        self.events_to_delete.append(event)
    
    def updateEvents(self):
        for event in self.events_to_delete : 
            if event in self.events : 
                self.events.remove(event)
        
        for event in self.events_to_add : 
            if not event in self.events : 
                self.events.append(event)
        
        self.events.sort(key = lambda event : event.priority, reverse = True)

    async def main(self):
        self.init_clock = self.clock = round(time.time()*1000)

        self.updateEvents()
        for event in self.events: 
            if event.trigger == "start":
                event.action(EventFiringInfo(self.init_clock, self.clock, self.loop_count, event.loop_count, event.args))
                self.removeEvent(event)

        self.clock = self.last_loop_clock = round(time.time()*1000)

        while self.loop : 
            self.clock = round(time.time()*1000)
            time_gap = self.clock - self.last_loop_clock

            self.updateEvents()
            for event in self.events: 
                if event.trigger == "loop":
                    event.action(EventFiringInfo(self.init_clock, self.clock, self.loop_count, event.loop_count, event.args))

                elif event.trigger == "repeat":
                    event.options[1] -= time_gap
                    if event.options[1] <= 0 : 
                        event.action(EventFiringInfo(self.init_clock, self.clock, self.loop_count, event.loop_count, event.args))
                        event.options[1] = event.options[0]
                        if event.options[2] > 1 :
                            event.options[2] -= 1
                        elif event.options[2] == 1 :
                            self.removeEvent(event)
                
                elif event.trigger == "delay":
                    event.options[0] -= time_gap
                    if event.options[0] <= 0 : 
                        event.action(EventFiringInfo(self.init_clock, self.clock, self.loop_count, event.loop_count, event.args))
                        self.removeEvent(event)

                elif event.trigger == "delay" and event.options[0]:
                    event.action()
                    self.removeEvent(event)

            await asyncio.sleep(0.04)

            self.loop_count += 1
            self.last_loop_clock = self.clock
        
        self.updateEvents()
        for event in self.events: 
            if event.trigger == "end":
                event.action(EventFiringInfo(self.init_clock, self.clock, self.loop_count, event.loop_count, event.args))
            
    def end(self):
        self.loop = False

class App():
    def __init__(self):
        self.event_handler = EventHandler()
        self.display = Display()
    
    def start(self, e):
        self.display.start()
        self.display.loadGraphic("test", "test_char_graphic.cg")
        self.display.addElement(DisplayElement())
    
    def end(self, e):
        self.event_handler.end()
        self.display.end()

    async def main(self):
        self.event_handler.addEvent(Event(0, "start", [], self.start))

        task = asyncio.create_task(self.event_handler.main())

        self.event_handler.addEvent(Event(0, "delay", [1000], self.end))

        await task
    
    def run(self):
        asyncio.run(self.main())
