import pandas as pd

class VcardFile:
    @property
    def cardcount(self):
        count = self.__cardcount
        return count

    def __init__(self, vcardfilename):
        self.__cardcount = 0
        vcard = open(vcardfilename, "r", encoding='UTF-8')
        print(f'{vcard.name} start parsing')
        for line in vcard:
            liter = getliter(line)
            if line == 'BEGIN:VCARD\n':
                self.__cardcount = self.__cardcount + 1
            isname = 'N' in liter
            if isname:
                name = line[line.find(':'):]

        print(vcard)
        print(f'{vcard.name} is parsing')


def getliter(line):
    liter = line[:line.find(";")]
    print(liter.find(";"))
    if line.find(";") == -1:
        liter = ""
    return liter;