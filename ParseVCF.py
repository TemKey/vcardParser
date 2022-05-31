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
        self.__peple = pd.DataFrame({'UID': [""], 'N': [""], 'FN': [""],
                                    'url': [""], 'org': [""], 'bday': ['22.01.1989'], 'photo': [""], 'title': [""]})
        self.__peple = self.__peple.drop(index=0)

        self.__phones = pd.DataFrame({'UID': [""], 'Phone': [""]})
        self.__phones = self.__phones.drop(index=0)

        self.__address = pd.DataFrame({'UID': [""], 'Address': [""]})
        self.__address = self.__address.drop(index=0)
        self.__mails = pd.DataFrame({'UID': [""], 'email': [""]})
        self.__mails = self.__mails.drop(index=0)

        vcard = open(vcardfilename, "r", encoding='UTF-8')
        print(f'{vcard.name} start parsing')

        for line in vcard:
            pref = line[:line.find(":")]
            telo = line[line.find(":") + 1:line.find("\n")]
            if pref.find(";") >= 0:
                pref = pref[:pref.find(";")]
            if pref == "N":
                name = telo
            if pref == "FN":
                fname = telo
            if pref == "TITLE":
                title = telo
            if pref == "BDAY":
                bday = telo
            if pref == "UID":
                UID = telo
            if pref == "url":
                url = telo
            if pref == "EMAIL":
                email = telo
            if pref == "ORG":
                org = telo
            if pref == "TEL":
                tel = telo
            if pref == "ADR":
                adr = telo
            if pref.find("PHOTO") != -1 and len(telo) > 50:
                img = base64.b64decode(telo)
                image = Image.open(BytesIO(img))
                image.show()
            if pref == 'END':
                peple = {'UID': UID, 'N': name, 'FN': fname, 'bday': bday, 'photo': image, 'org': org, 'url': url, 'title': title}
                phones = {'UID': UID, 'Phone': name}
                addres = {'UID': UID, 'Addres': adr}
                emails = {'UID': UID, 'email': email}
                self.__peple = self.__peple.append(peple, ignore_index=True)
                self.__phones = self.__phones.append(phones, ignore_index=True)
                self.__mails = self.__mails.append(emails, ignore_index=True)
                self.__address = self.__address.append(addres, ignore_index=True)

        print(f'{vcard.name} is parsing')