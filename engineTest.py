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

    box_graphic = Engine.BoxGraphic(10, 5, 202, 16, 6)

    box = box_graphic.getGraphic()

    assertEquals(box, expected)

def testDisplay():
    global display

    display = Engine.Display()
    assertEquals(display.getStatus(), False)

    display.start()
    assertEquals(display.getStatus(), True)
    time.sleep(.1)

    display.loadGraphic("test_box_1", Engine.BoxGraphic(10, 5, 1, 0, 6))
    time.sleep(.1)

    display.addElement("test_1", "test_box_1", 5, 5)
    display.update()
    time.sleep(1)

    display.end()

try :
    testGraphics()
    testDisplay()

    print(test_result)

except : 
        display.end()
        print(test_result)
        traceback.print_exc()