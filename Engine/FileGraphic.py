from Engine import AbstractGraphic

class FileGraphic(AbstractGraphic):
    def __init__(self, file_path): 
        super(FileGraphic, self).__init__()
        self._file_path = file_path
    
    def getGraphic(self):
        with open(self._file_path, "rb") as file : 
            data = file.read()
            self._graphic = [[]]
            for cursor in range(round((len(data)-len(data)%7)/7)) :
                
                char_data = data[n*7:(n+1)*7]
                extra_data = ord(char_data[6:7])

                if bool(extra_data >> 0 & 1) :
                    self._graphic.append([])
                
                self._graphic[-1].append([
                    char_data[:4].decode("utf-32"), 
                    ord(char_data[4:5]), 
                    ord(char_data[5:6]),
                    bool(extra_data >> 1 & 1),
                    bool(extra_data >> 2 & 1)
                ])
        
        self.width = len(self._graphic[0])
        self.height = len(self.graphic)

        super(FileGraphic, self).getGraphic()
