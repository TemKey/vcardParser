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
        self.__peple = pd.DataFrame()
        self.__phones = pd.DataFrame()
        self.__address = pd.DataFrame()
        self.__mails = pd.DataFrame()

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
                peple.update({'photo': image})

            if pref == 'END':
                for p in phones:
                    p.update({'UID': peple["UID"]})
                for e in emails:
                    e.update({'UID': peple["UID"]})
                for a in addres:
                    a.update({'UID': peple["UID"]})
                p = pd.DataFrame(peple, index=[peple["UID"]])
                self.__peple = pd.concat([self.__peple, p])
                if len(phones) != 0:
                    p = pd.DataFrame(phones, index=[peple['UID']])
                    self.__phones = pd.concat([self.__phones, p])
                if len(emails) != 0:
                    self.__mails = self.__mails.append(emails, ignore_index=True)
                if len(addres) != 0:
                    self.__address = self.__address.append(addres, ignore_index=True)
        print(f'{vcard.name} is parsing')
    def savetocsv(self):
        self.__peple.to_csv("peple.csv")
        self.__phones.to_csv("phones.csv")
        self.__mails.to_csv("mails.csv")
        self.__address.to_csv("addres.csv")

    # def saveimage(self):
        # UID = self.__peple['UID']
        # UID = f'images/{UID}.jpg'
        # image.save(UID)

