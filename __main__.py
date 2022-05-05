import DisplayInterface
from PIL import Image
import time

im = Image.open("citaro.jpg")
#im = Image.open("test_image_big.png")

di = DisplayInterface.TerminalDisplayInterface()

di.start()

try : 
    time.sleep(1)
    
except Exception as e : 
    di.exitWithError(e)

di.end()