import Engine

def assertEquals(test, expected):
    if test == expected : 
        print("OK")
    else : 
        print(f"ASSERTATION ERROR : {test}")

def testFileGraphic():
    test_file_path = "test_char_graphic.cg"
    expected = [
        [['╔', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['╗', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['╚', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['╝', 202, 16, False, False]]
    ]

    graphic = Engine.FileGraphic(test_file_path)

    parsed = graphic.getGraphic()

    assertEquals(parsed, expected)

def testBoxGraphic():
    expected = [
        [['╔', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['╗', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['║', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], [' ', 202, 16, False, False], ['║', 202, 16, False, False]],
        [['╚', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['═', 202, 16, False, False], ['╝', 202, 16, False, False]]
    ]

    graphic = Engine.BoxGraphic(10, 5, 202, 16, 6)

    box = graphic.getGraphic()

    assertEquals(box, expected)

testFileGraphic()
testBoxGraphic()