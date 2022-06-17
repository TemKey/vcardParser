import pandas as pd
import base64
from io import BytesIO


from PIL import Image

class VcardFile:
    def savevcard(self, vcardfilename):
        for index, vcard in self.__peple.iterrows():
            fam = vcard["fam"]

        print(f"file {vcardfilename} is saved.")

    def openvcard(self, vcardfilename):
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
                emailtype = line[6:line.find(":", 6)]
                emails.append({'email': telo, 'type': emailtype})
            if pref == "ORG":
                peple.update({'ORG': telo})
            if pref == "CATEGORIES":
                peple.update({'CATEGORIES': telo})
            'запоминаем телефоны'
            if pref == "TEL":
                phonetype = line[4:line.find(":", 4)]
                phones.append({'Phone': telo, 'type': phonetype})
            'запоминаем адреса'
            if pref == "ADR":
                adrtype = line[4:line.find(";", 4)]
                addres.append({'Address': telo, 'type': adrtype})
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
                    for phon in phones:
                        p = pd.DataFrame(phon, index=[peple['UID']])
                        self.__phones = pd.concat([self.__phones, p])
                if len(emails) != 0:
                    for mai in emails:
                        p = pd.DataFrame(mai, index=[peple['UID']])
                        self.__mails = pd.concat([self.__mails, p])
                if len(addres) != 0:
                    for adr in addres:
                        p = pd.DataFrame(adr, index=[peple['UID']])
                        self.__address = pd.concat([self.__address, p])
        self.__peple['fam'] = getFam(self.__peple['N'], "fam")
        self.__peple['fname'] = getFam(self.__peple['N'], "fname")
        self.__peple['sname'] = getFam(self.__peple['N'], "sname")
        del self.__peple['N']
        del self.__peple['FN']
        vcard.close()
        print(f'{vcard.name} stop parsing')

    def savetocsv(self):
        ppl = self.__peple
        del ppl["photo"]
        ppl.to_csv("peple.csv", index=False)
        self.__phones.to_csv("phones.csv", index=False)
        self.__mails.to_csv("mails.csv", index=False)
        self.__address.to_csv("addres.csv", index=False)

    # def saveimage(self):
    #     UID = self.__peple['UID']
    #     UID = f'images/{UID}.jpg'
    #     image.save(UID)

def splitN(pdpeple):
    newArr = []
    for name in pdpeple:
        find = name.find(" ")
        if find > 0:
            name = name.replace(" ", ";")
            name = name[:-1]
        newArr.append(name)
    return newArr
def getFam(pdpeple, index):
    fio = pd.DataFrame(columns=["fam", "fname", "sname"])
    for name in pdpeple:
        name = name.replace(" ", ";")
        arr = name.split(";")
        fam = arr[0]
        fname = arr[1]
        sname = arr[2]
        f = pd.DataFrame({'fam': [fam], 'fname': [fname], 'sname': [sname]})
        fio = pd.concat([fio, f])
    result = fio[index].array
    return result