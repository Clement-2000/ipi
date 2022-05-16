import Engine, time, traceback

test_result = ""
display = None

def assertEquals(test, expected) -> bool:
    global test_result
    if test == expected : 
        test_result += "-- OK --\n"
    else : 
        test_result += f"-- ASSERTATION ERROR --\n  TESTED:\n    {test}\n  EXPECTED:\n    {expected}\n"

def testGraphics():
    test_file_path = "test_char_graphic.cg"
    expected = [
        [['╔', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['╗', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['╚', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['╝', 202, 16, False, False]]
    ]

    file_graphic = Engine.FileGraphic(test_file_path)

    graphic = file_graphic.getGraphic()

    assertEquals(graphic, expected)

    box_graphic = Engine.BoxGraphic(10, 5, 202, 16, 7)

    box = box_graphic.getGraphic()

    assertEquals(box, expected)

def testDisplay():
    global display

    display = Engine.Display()
    assertEquals(display.getStatus(), False)

    display.start()
    assertEquals(display.getStatus(), True)
    time.sleep(.1)
    
    display.loadGraphic("test_box_0", Engine.BoxGraphic(20, 3, 0, 163, 0))
    display.loadGraphic("test_box_1", Engine.BoxGraphic(20, 1, 0, 133, 0))
    display.loadGraphic("test_box_2", Engine.BoxGraphic(20, 3, 0, 26, 0))

    display.loadGraphic("surround_box", Engine.BoxGraphic(display.getWidth() - 4, display.getHeight() - 2, 8, 0, 7))
    display.addElement("surround_box", "surround_box", 2, 1)
    display.update()

    for n in range(25):
        display.loadGraphic("surround_box", Engine.BoxGraphic(display.getWidth() - 4, display.getHeight() - 2, 8, 0, 7))

        display.addElement("1", "test_box_0", n, 5)
        display.addElement("2", "test_box_1", n, 8)
        display.addElement("3", "test_box_2", n, 9)
        display.update()
        time.sleep(0.04)

    display.clear()
    display.update()

    time.sleep(1)

    display.end()

def test(event):
    print("test")

def testEventHandler():
    handler = Engine.EventHandler()

    handler.addEvent("test_start_event", "start", [], test)

    handler.start()

try :
    #testGraphics()
    #testDisplay()
    testEventHandler()

    print(test_result)

except Exception as e : 
        #display.end()
        print(test_result)
        print("")
        traceback.print_exc()
        print(e.__traceback__)