import time
import sys
import os
import asyncio

import select
import tty 
import termios

FRAMERATE = 20

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
    
    def start(self) -> None: 
        tty.setcbreak(sys.stdin.fileno())
        sys.stdout.write("\33[s\33[?47h\33[2J\33[H")
        sys.stdout.flush()

        self.status = True
    
    def end(self) -> None: 
        self.purge()
        sys.stdout.write("\33[?47l\33[u")
        sys.stdout.flush()
        fd = sys.stdin.fileno()
        
        old = termios.tcgetattr(fd)
        old[3] = old[3] | termios.ECHO
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

        self.status = False
    
    def clear(self):
        self.displayed_elements = []
    
    def purge(self):
        self.loaded_graphics = {}
        self.displayed_elements = []

        self.display_buffer = []
        self.string_buffer = ""
    
    def clearBuffer(self) -> None:
        self.display_buffer = [[[" ", 0, 0] for _ in range(self.width)] for __ in range(self.height)]
        self.string_buffer = ""
    
    def loadGraphic(self, graphic_name :str, element) -> None:
        self.loaded_graphics[graphic_name] = element
    
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
        for element in self.displayed_elements:
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
        self.BOX_STYLES = [
            "         ",
            "???????????? ????????????",
            "???????????? ????????????",
            "???????????? ????????????",
            "???????????? ????????????",
            "???????????? ????????????",
            "???????????? ????????????",
            "???????????? ????????????"
        ]

        self.width = width
        self.height = height
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.style = style
    
        self.graphic = [[[self.BOX_STYLES[self.style][0], self.background_color, self.foreground_color, False, False]] + [[self.BOX_STYLES[self.style][1], self.background_color, self.foreground_color, False, False]] * (self.width-2) + [[self.BOX_STYLES[self.style][2], self.background_color, self.foreground_color, False, False]]] + \
                       [[[self.BOX_STYLES[self.style][3], self.background_color, self.foreground_color, False, False]] + [[self.BOX_STYLES[self.style][4], self.background_color, self.foreground_color, False, False]] * (self.width-2) + [[self.BOX_STYLES[self.style][5], self.background_color, self.foreground_color, False, False]]] * (self.height - 2) + \
                       [[[self.BOX_STYLES[self.style][6], self.background_color, self.foreground_color, False, False]] + [[self.BOX_STYLES[self.style][7], self.background_color, self.foreground_color, False, False]] * (self.width-2) + [[self.BOX_STYLES[self.style][8], self.background_color, self.foreground_color, False, False]]]

class TextGraphic(AbstractGraphic):
    def __init__(self, text :str, background_color :int, foreground_color :int): 
        super().__init__()

        self.width = len(text)
        self.height = 1

        self.foreground_color = foreground_color
        self.background_color = background_color
    
        graphic = [[]]

        for char in text :
            graphic[0].append([char, self.background_color, self.foreground_color, False, False])
        
        self.graphic = graphic

class Event():
    def __init__(self, priority :int, trigger :str, options :list, action :callable, args:any = None):
        self.priority = priority
        self.trigger = trigger
        self.options = options
        self.action = action
        self.args = args

        self.loop_count = 0

class EventFiringInfo():
    def __init__(self, init_clock :int, clock :int, loop_count :int, event_loop_count :int, args:any):
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
        self.pressed_keys = ""
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

            pressed_keys = ""
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                pressed_keys = sys.stdin.read(1)
            termios.tcflush(sys.stdin,termios.TCIFLUSH)

            self.updateEvents()
            for event in self.events: 
                if event.trigger == "loop":
                    event.action(EventFiringInfo(self.init_clock, self.clock, self.loop_count, event.loop_count, event.args))

                elif event.trigger == "repeat": # [gap, delay]
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
                
                elif (event.trigger == "key") and event.options[0] in pressed_keys: 
                    event.action(EventFiringInfo(self.init_clock, self.clock, self.loop_count, event.loop_count, event.args))

            await asyncio.sleep(1/FRAMERATE)

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

        self.fish_level = 0
    
    def start(self, e):

        self.display.start()

        self.display.loadGraphic("map", FileGraphic("assets/map.cg"))

        self.display.loadGraphic("fish_0", BoxGraphic( 8, 3, 15, 0, 4))
        self.display.loadGraphic("fish_1", BoxGraphic(10, 3, 15, 0, 4))
        self.display.loadGraphic("fish_2", BoxGraphic(15, 5, 15, 0, 4))
        self.display.loadGraphic("fish_3", BoxGraphic(17, 7, 15, 0, 4))

        self.display.loadGraphic("fish_0_label", TextGraphic("MINI FISH", 11, 9))
        self.display.loadGraphic("fish_1_label", TextGraphic("PETI FISH", 11, 9))
        self.display.loadGraphic("fish_2_label", TextGraphic("MOYEN FISH", 11, 9))
        self.display.loadGraphic("fish_3_label", TextGraphic("GRO FISH", 11, 9))

        self.map = DisplayElement("map", -745, -65)
        self.fish = DisplayElement("fish_0", 0, 0)
        self.fish_label = DisplayElement("fish_0_label", 0, 0)

        self.display.addElement(self.map)
        self.display.addElement(self.fish)
        self.display.addElement(self.fish_label)

    def end(self, e):
        self.event_handler.end()
        self.display.end()

    def displayUpdate(self, e):
        self.fish.x = round((self.display.width - self.display.loaded_graphics[self.fish.graphic_name].width)/2)
        self.fish.y = round((self.display.height - self.display.loaded_graphics[self.fish.graphic_name].height)/2 + 1)

        self.fish_label.x = round((self.display.width - self.display.loaded_graphics[self.fish_label.graphic_name].width)/2)
        self.fish_label.y = round(self.display.height/2 + 1)

        self.display.update()
    
    def loop(self, e):
        pass
    
    def move(self, e):
        self.map.x += e.args[0] * 2
        self.map.y += e.args[1]
    
    def updateFishLevel(self):
        self.fish.graphic_name = f"fish_{self.fish_level}"
        self.fish_label.graphic_name = f"fish_{self.fish_level}_label"

    def levelUp(self, e):
        if self.fish_level < 3:
            self.fish_level += 1
            self.updateFishLevel()

    def levelDown(self, e):
        if self.fish_level > 0:
            self.fish_level -= 1
            self.updateFishLevel()

    async def init(self):
        self.event_handler.addEvent(Event(1, "start", [], self.start))

        task = asyncio.create_task(self.event_handler.main())

        self.event_handler.addEvent(Event(-1, "loop", [], self.displayUpdate))

        self.event_handler.addEvent(Event(0, "repeat", [100, 0, 0], self.loop))

        self.event_handler.addEvent(Event(-2, "key", ["\x1b"], self.end))

        self.event_handler.addEvent(Event(0, "key", ["z"], self.move, [0, 1]))
        self.event_handler.addEvent(Event(0, "key", ["s"], self.move, [0, -1]))
        self.event_handler.addEvent(Event(0, "key", ["q"], self.move, [1, 0]))
        self.event_handler.addEvent(Event(0, "key", ["d"], self.move, [-1, 0]))

        self.event_handler.addEvent(Event(0, "key", ["9"], self.levelUp))
        self.event_handler.addEvent(Event(0, "key", ["3"], self.levelDown))

        await task
    
    def run(self):
        asyncio.run(self.init())
