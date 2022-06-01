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
                                    'url': [""], 'ORG': [""], 'bday': ['22.01.1989'], 'photo': [""], 'title': [""]})
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

            if pref == 'BEGIN':
                peple = {}
                phones = []
                emails = []
                addres = []
            if pref == "N":
                peple.update({'N': telo})
            if pref == "FN":
                peple.update({'FN': telo})
            if pref == "TITLE":
                peple.update({'title': telo})
            if pref == "BDAY":
                peple.update({'BDAY': telo})
            if pref == "UID":
                peple.update({'UID': telo})
            if pref == "url":
                peple.update({'url': telo})
            if pref == "EMAIL":
                emails.append({'email': telo})
            if pref == "ORG":
                peple.update({'ORG': telo})
            'запоминаем телефоны'
            if pref == "TEL":
                phones.append({'Phone': telo})
            'запоминаем адреса'
            if pref == "ADR":
                addres.append({'Address': telo})
            if pref.find("PHOTO") != -1 and len(telo) > 50:
                img = base64.b64decode(telo)
                image = Image.open(BytesIO(img))
                image.show()
                peple.update({'photo': image})
            if pref == 'END':
                for p in phones:
                    p.update({'UID': peple["UID"]})
                for e in emails:
                    e.update({'UID': peple["UID"]})
                for a in addres:
                    a.update({'UID': peple["UID"]})
                self.__peple = self.__peple.append(peple, ignore_index=True)
                self.__phones = self.__phones.append(phones, ignore_index=True)
                self.__mails = self.__mails.append(emails, ignore_index=True)
                self.__address = self.__address.append(addres, ignore_index=True)

        print(f'{vcard.name} is parsing')