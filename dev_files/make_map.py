from PIL import Image
from httplib2 import ServerNotFoundError

def serialize(char :str, bg :int, fg :int, newline :bool, bg_transparency :bool, fg_transparency :bool) -> bytes:
    extra_data = newline + (bg_transparency << 1) + (fg_transparency << 2)
    return char.encode("utf-32")[4:] + bytes([bg, fg, extra_data])

file = open("map.cg", "ab")

im = Image.open("dev_files/map.png")
px = im.load()

for y in range(im.height):
    d = b""
    for x in range(im.width):
        nl = x >= im.width - 1
        p = px[x, y]

        if p == (0, 255, 0, 255):
            d += serialize("%", 40, 22, nl, False, False)
        elif p == (255, 255, 0, 255):
            d += serialize("~", 26, 38, nl, False, False)
        elif p == (255, 0, 255, 255):
            d += serialize("x", 26, 51, nl, False, False)
        elif p == (0, 0, 255, 255):
            d += serialize("~", 18, 27, nl, False, False)
        elif p == (255, 0, 0, 255):
            d += serialize("x", 214, 227, nl, False, False)
    
    file.write(d)
file.close()