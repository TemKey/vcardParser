import pandas as pd
import base64
from io import BytesIO
import os.path
import pyodbc
from PIL import Image
import progressbar
import sys

class VcardFile:
    def savevcard(self, vcardfilename):
        self.__peple = pd.read_csv("vcard/people.csv", dtype={'BDAY': 'Int64', 'fam': 'object'})
        self.__mails = pd.read_csv("vcard/mails.csv")
        self.__address = pd.read_csv("vcard/adress.csv")
        self.__phones = pd.read_csv("vcard/phones.csv")
        self.__peple["fam"] = self.__peple["fam"].fillna("")
        self.__peple["fname"] = self.__peple["fname"].fillna("")
        self.__peple["sname"] = self.__peple["sname"].fillna("")
        self.__address["streethouse"] = self.__address["streethouse"].fillna("")
        self.__address["city"] = self.__address["city"].fillna("")
        self.__address["region"] = self.__address["region"].fillna("")
        self.__address["pindex"] = self.__address["pindex"].fillna("")
        self.__address["country"] = self.__address["country"].fillna("")

        data = ""
        for index, vcard in self.__peple.iterrows():
            phones = self.__phones.loc[self.__phones['UID'] == vcard['UID']]
            adress = self.__address.loc[self.__address['UID'] == vcard['UID']]
            emails = self.__mails.loc[self.__mails['UID'] == vcard['UID']]
            vcardfile = open(vcardfilename, "w", encoding='UTF-8')
            data = data + makestring(vcard, phones, adress, emails)

        vcardfile.write(data)
        vcardfile.close()

    def savevcardfromaccess(self, vcardfilename):
        print("save VCard from MS Access")
        conn = pyodbc.connect(
            'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\TemKey\\PycharmProjects\\vcardParser\\vcard.accdb;')
        cursor = conn.cursor()  # создается курсор
        self.__peple = pd.read_sql("SELECT * FROM people;", conn)
        self.__mails = pd.read_sql("SELECT * FROM mails", conn)
        self.__address = pd.read_sql("SELECT * FROM addres", conn)
        self.__phones = pd.read_sql("SELECT * FROM phones", conn)
        self.__peple["fam"] = self.__peple["fam"].fillna("")
        self.__peple["fname"] = self.__peple["fname"].fillna("")
        self.__peple["sname"] = self.__peple["sname"].fillna("")
        self.__peple["ORG"] = self.__peple["ORG"].apply(makekavi)
        self.__address["streethouse"] = self.__address["streethouse"].fillna("")
        self.__address["city"] = self.__address["city"].fillna("")
        self.__address["region"] = self.__address["region"].fillna("")
        self.__address["pindex"] = self.__address["pindex"].fillna("")
        self.__address["country"] = self.__address["country"].fillna("")
        self.__peple['photo'] = self.__peple['image'].apply(getphotosql)
        data = ""
        for index, vcard in self.__peple.iterrows():

            phones = self.__phones.loc[self.__phones['UID'] == vcard['UID']]
            adress = self.__address.loc[self.__address['UID'] == vcard['UID']]
            emails = self.__mails.loc[self.__mails['UID'] == vcard['UID']]
            print(vcard["fname"])
            if vcard["photo"] != None:
                image = Image.open(vcard["image"])
                image.show()
            with open(vcardfilename, "w", encoding='UTF-8') as vcardfile:
                data = data + makestring(vcard, phones, adress, emails)
                vcardfile.write(data)
        conn.close()

        print(f"file {vcardfilename} is saved.")
    def openvcard(self, vcardfilename):
        barсounter = 0
        self.__peple = pd.DataFrame()
        self.__phones = pd.DataFrame()
        self.__address = pd.DataFrame()
        self.__mails = pd.DataFrame()

        vcard = open(vcardfilename, "r", encoding='UTF-8')
        print(f'{vcard.name} start parsing')
        pict = ""
        isphoto = False
        with progressbar.ProgressBar() as bar:
            for line in vcard:
                pref = line[:line.find(":")]
                telo = line[line.find(":") + 1:line.find("\n")]
                telo = telo.replace("\\", "")
                if pref.find(";") >= 0:
                    pref = pref[:pref.find(";")]
                if pref == 'BEGIN':
                    barсounter += 1
                    bar.update(barсounter)
                    peple = {}
                    phones = []
                    emails = []
                    addres = []
                if pref == "N":
                    peple.update({'N': telo})
                if pref == "FN":
                    peple.update({'FN': telo})
                if pref == "NOTE":
                    peple.update({'NOTE': telo})
                if pref == "TITLE":
                    peple.update({'title': telo})
                if pref == "BDAY":
                    peple.update({'BDAY': telo})
                if pref == "UID":
                    peple.update({'UID': telo})
                if pref == "URL":
                    peple.update({'url': telo})
                if pref == "X-ANNIVERSARY":
                    peple.update({'X-ANNIVERSARY': telo})
                if pref == "EMAIL":
                    emailtype = line[line.find("=")+1:line.find(":", 6)]
                    emails.append({'email': telo, 'type': emailtype})
                if pref == "ORG":
                    peple.update({'ORG': telo})
                if pref == "CATEGORIES":
                    peple.update({'CATEGORIES': telo})
                # 'запоминаем телефоны'
                if pref == "TEL":
                    phonetype = line[line.find("=")+1:line.find(":", 4)]
                    phones.append({'Phone': telo, 'type': phonetype})
                # 'запоминаем адреса'
                if pref == "ADR":
                    adrtype = line[line.find("=")+1:line.find(":")]
                    addres.append({'Address': telo, 'type': adrtype})
                if pref.find("PHOTO") != -1:
                    isphoto = True
                if isphoto and telo != "VCARD":
                    pict = pict + telo
                if pref == 'END':
                    if isphoto:
                        pict = pict.replace("\n", "")
                        try:
                            if len(pict) % 4:
                                pict += '=' * (len(pict) % 4)
                            img = base64.b64decode(pict)
                            image = Image.open(BytesIO(img))
                            peple.update({'photo': image})
                        except:
                            print(peple['N'] + " bad photo")
                            return 0
                        pict = ""
                        isphoto = False
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
        self.__address["streethouse"] = getAdr(self.__address['Address'], "streethouse")
        self.__address["city"] = getAdr(self.__address['Address'], "city")
        self.__address["region"] = getAdr(self.__address['Address'], "region")
        self.__address["pindex"] = getAdr(self.__address['Address'], "pindex")
        self.__address["country"] = getAdr(self.__address['Address'], "country")
        del self.__peple['N']
        del self.__peple['FN']
        del self.__address['Address']
        vcard.close()
        print(f'{vcard.name} stop parsing')

    def savetocsv(self):
        ppl = self.__peple
        del ppl["photo"]
        ppl.to_csv("vcard/people.csv", index=False)
        self.__phones.to_csv("vcard/phones.csv", index=False)
        self.__mails.to_csv("vcard/mails.csv", index=False)
        self.__address.to_csv("vcard/adress.csv", index=False)
        print("Files saves to *.csv")
    def toaccess(self):
        barсounter = 0
        print("save data to MS Access")
        # self.__peple['hash'] = (self.__peple['fname'].apply(hash) + self.__peple['ORG'].apply(hash) +
        #                         self.__peple['title'].apply(hash)) % sys.maxsize
        conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\TemKey\\PycharmProjects\\vcardParser\\vcard.accdb;')
        cursor = conn.cursor()  # создается курсор
        people =  self.__peple.astype(object).where(pd.notnull(self.__peple), None)
        people["ORG"] = people["ORG"].replace('\\"', "")
        for r, p in people.iterrows():
            try:
                cursor.execute("INSERT INTO people ("
                               "title, "
                               "ORG, "
                               "UID, "
                               "CATEGORIES, "
                               "notes, "
                               "BDAY, "
                               "url, "
                               "ANNIVERSARY, "
                               "fam, "
                               "fname, "
                               "sname) "
                               "VALUES ("
                               "?,?,?,?,?,?,?,?,?,?,?)",
                               ([
                                p["title"],
                                p["ORG"],
                                p["UID"],
                                p["CATEGORIES"],
                                p["NOTE"],
                                p["BDAY"],
                                p["url"],
                                p["X-ANNIVERSARY"],
                                p["fam"],
                                p["fname"],
                                p["sname"]
                               ]))
                cursor.commit()
            except:
                pass
        for r, p in self.__mails.iterrows():
            try:
                cursor.execute("INSERT INTO mails ("
                               "mail, "
                               "type, "
                               "UID) "
                               "VALUES ("
                               "?,?,?)",
                               ([
                                p["email"],
                                p["type"],
                                p["UID"]
                               ]))
                cursor.commit()
            except:
                pass
        for r, p in self.__phones.iterrows():
            try:
                cursor.execute("INSERT INTO phones ("
                               "phone, "
                               "type, "
                               "UID) "
                               "VALUES ("
                               "?,?,?)",
                               ([
                                   p["Phone"],
                                   p["type"],
                                   p["UID"]
                               ]))
                cursor.commit()
            except:
                pass
        for r, p in self.__address.iterrows():
            try:
                cursor.execute("INSERT INTO addres ("
                               "UID, "
                               "type, "
                               "streethouse, "
                               "city, "
                               "region, "
                               "pindex, "
                               "country) "
                               "VALUES ("
                               "?,?,?,?,?,?,?)",
                               ([
                                   p["UID"],
                                   p["type"],
                                   p["streethouse"],
                                   p["city"],
                                   p["region"],
                                   p["pindex"],
                                   p["country"]
                               ]))
                cursor.commit()
            except:
                pass
        conn.close()

    def saveimage(self):
        i = self.__peple
        i = i.dropna(subset="photo")
        for id, images in i.iterrows():
            UID = images['UID']
            UID = f'vcard/images/{UID}.jpg'
            if not os.path.exists(UID):
                image = images['photo']
                image.save(UID)

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
def getAdr(adress, index):
    adr = pd.DataFrame()
    for name in adress:
        arr = name.split(";")
        street = arr[2]
        city = arr[3]
        region = arr[4]
        pindex = arr[5]
        country = arr[6]
        f = pd.DataFrame({'streethouse': [street], 'city': [city], 'region': [region],
                          'pindex': [pindex], 'country': [country]})
        adr = pd.concat([adr, f])
    result = adr[index].array
    return result
def makestring(peple, phonebook=None, adressbook=None, emeilsbook=None):
    tels = ""
    adress = ""
    email = ""
    FN = " ".join([peple["fam"], peple["fname"], peple["sname"]]).strip()
    for i, tel in phonebook.iterrows():
        tels = tels + f'TEL;TYPE={tel["type"]}:{tel["Phone"]}\n'
    for i, mail in emeilsbook.iterrows():
            email = email + f'EMAIL;TYPE={mail["type"]}:{mail["mail"]}\n'
    for i, adr in adressbook.iterrows():
        adress = adress + f'ADR;TYPE={adr["type"]}:;;{adr["streethouse"]};' \
                          f'{adr["city"]};{adr["region"]};{adr["pindex"]};{adr["country"]}\n'
    if pd.isna(peple["ORG"]):
        org = ""
    else:
        org = f'ORG:{peple["ORG"]}\n'
    if pd.isna(peple["CATEGORIES"]):
        cat = ""
    else:
        cat = f'CATEGORIES:{peple["CATEGORIES"]}\n'
    if pd.isna(peple["BDAY"]):
        bday = ""
    else:
        bday = f'BDAY:{peple["BDAY"]}\n'
    if pd.isna(peple["photo"]):
        photo = ""
    else:
        photo = f'PHOTO;ENCODING=BASE64;TYPE=JPEG:{peple["photo"]}\n'
    if pd.isna(peple["notes"]):
        note = ""
    else:
        note = f'NOTE:{peple["notes"]}\n'
    try:
        if pd.isna(peple["url"]):
            url = ""
        else:
            url = f'URL:{peple["url"]}\n'
    except:
        print("in csv file not column URL")
        url = ""
        pass
    try:
        if pd.isna(peple["ANNIVERSARY"]):
            ANNIVERSARY = ""
        else:
            ANNIVERSARY = f'X-ANNIVERSARY:{peple["ANNIVERSARY"]}\n'
    except:
        print("in csv not coumn X-ANNIVERSARY")
        ANNIVERSARY = ""
    s = f'BEGIN:VCARD\nVERSION:3.0\n' \
        f'N:{peple["fam"]};{peple["fname"]};{peple["sname"]};;\n' \
        f'FN:{FN}\n{tels}{adress}{email}{org}{cat}{bday}{note}{url}{ANNIVERSARY}' \
        f'UID:{peple["UID"]}\n' \
        f'X-ACCOUNT:com.android.huawei.phone;Phone\n{photo}' \
        f'END:VCARD\n'
    return s

def getphoto(UIDlist):
    photolist = []
    for id in UIDlist:
        path = f'vcard/images/{id}.jpg'
        if os.path.exists(path):
            img = open(path, 'rb')
            imgr = img.read()
            image = base64.b64encode(imgr)
            photolist.append(image.decode('utf-8'))
        else:
            photolist.append(float("nan"))
    result = pd.Series(photolist)
    return result

def getphotosql(path):
    photolist = []
    # for id, path in imagepath.iterrows():
    if path == None:
        return
    if os.path.exists(path):
        img = open(path, 'rb')
        imgr = img.read()
        image = base64.b64encode(imgr)
        # photolist.append(image.decode('utf-8'))
        return image.decode('utf-8')
    # else:
        # photolist.append(float("nan"))
    # result = pd.Series(photolist)
    # return result
def makekavi(string):
    if string == None:
        return
    return string.replace("\"", "\\\"")