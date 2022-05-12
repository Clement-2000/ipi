def createVol(numero_vol, numero_avion, depart, destination, heure_depart, heure_arivee):
    vol = {
        "numero_vol": numero_vol,
        "numero_avion": numero_avion,
        "depart": depart,
        "destination": destination,
        "heure_depart": heure_depart,
        "heure_arivee": heure_arivee,
        "est_parti": False
    }

    return vol

def getInfoVol(vol):
    if vol["est_parti"] :
        print(f"Le vol n°{vol['numero_vol']}, à destination de {vol['destination']}, est parti à {vol['heure_depart']} et arrivera à destination à {vol['heure_arivee']}")
    else : 
        print(f"Le vol n°{vol['numero_vol']}, à destination de {vol['destination']}, partira à {vol['heure_depart']}")

def setVolParti(vol):
    vol["est_parti"] = True

vol_test = createVol("4492", "484", "Paris", "Tourcouing", "14:12", "18:64")

getInfoVol(vol_test)

setVolParti(vol_test)

getInfoVol(vol_test)

print(vol_test["est_parti"])


print("**************** AVEC UNE CLASSE ****************")

class Vol():
    def __init__(self, numero_vol, avion, depart, destination, heure_depart, heure_arivee):
        self.numero_vol = numero_vol
        self.avion = avion
        self.depart = depart
        self.destination = destination
        self.heure_depart = heure_depart
        self.heure_arivee = heure_arivee
        self.est_parti = False
    
    def getInfoVol(self):
        if self.est_parti :
            print(f"Le vol n°{self.numero_vol}, à destination de {self.destination}, est parti à {self.heure_depart} et arrivera à destination à {self.heure_arivee}, assuré par un {self.avion.modele} n°{self.avion.numero}")
        else : 
            print(f"Le vol n°{self.numero_vol}, à destination de {self.destination}, partira à {self.heure_depart}")
    
    def setVolParti(self):
        self.est_parti = True

class Avion():
    def __init__(self, modele, numero):
        self.modele = modele
        self.numero = numero

avion_test = Avion("A320", "64485mékoui")

avion_test.numero

vol_test_classe = Vol("4492", avion_test, "Paris", "Tourcouing", "14:12", "18:64")
vol_test_classe_2 = Vol("4493", avion_test, "Tourcouing", "Porto", "19:20", "00:00")

vol_test_classe.getInfoVol()

vol_test_classe.setVolParti()

vol_test_classe.getInfoVol()

vol_test_classe_2.getInfoVol()

vol_test_classe_2.setVolParti()

vol_test_classe_2.getInfoVol()

print(vol_test_classe.est_parti)
