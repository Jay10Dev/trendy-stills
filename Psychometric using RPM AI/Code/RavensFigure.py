import os

class RavensFigure:

    def __init__(self, name, problemName, setName):
        self.name=name
        self.objects={}
        self.visualFilename="Problems" + os.sep + setName + os.sep + problemName + os.sep + name + ".png"
