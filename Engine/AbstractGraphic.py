class AbstractGraphic():
    def __init__(self): 
        self.width = 0
        self.height = 0
        self._graphic = None
    
    def getGraphic(self):
        return self._graphic