import pandas as pd
import base64
from io import BytesIO


from PIL import Image

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
    pref = line[:line.find(":")]
    pdor = line[line.find(":")+1:line.find("\n")]
    str = line.split(';')
    if pref.find("PHOTO") == 0 and len(pdor) > 50:
        img = base64.b64decode(pdor)
        image = Image.open(BytesIO(img))
        image.show()
    if line.find(";") == -1:
        liter = ""
        return ""
    return liter