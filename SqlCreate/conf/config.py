import configparser

class Config:
    def __init__(self, path):
        self.path = path
        self.cf = configparser.ConfigParser()
        self.cf.read(self.path)
    
    def printSections(self):
        for section in self.cf.sections():
            print(section)

    def getSections(self):
        return self.cf.sections()

    def getSectItems(self, name):
        return self.cf.items(name)
    