from ParseVCF import VcardFile
import WhatsUp
import os

def makephonelist():
    phones = []
    fiels = os.listdir("images/WhastUp")
    files = list(map(lambda suf: suf.replace(".jpg", ""), fiels))
    badfiles = open("images/WhastUp/nopict.txt").readlines()
    badfiles = [line.rstrip('\n') for line in badfiles]

    with open("vcard/phones.csv") as file:
        file.readline()
        while True:
            line = file.readline()
            if not line:
                break
            line = line.split(",")
            if line[0][0] == "+":
                phones.append(line[0].replace(" ", ""))
    phones = list(set(phones) - set(files) - set(badfiles))
    return phones
makephonelist()

if __name__ == '__main__':
    vcf = VcardFile()
    print("from vCard csv - 1; from csv to vCard - 2")
    opencard = input()
    if opencard == "1":
        vcf.openvcard("Contacts.vcf")
        vcf.toaccess()
        #vcf.saveimage()
        #vcf.savetocsv()
    if opencard == "2":
        # vcf.savevcard("Contacts_new.vcf")
        vcf.savevcardfromaccess("Contacts_new.vcf")
    if opencard == "3":
        WhatsUp.connectwp(makephonelist())
    if opencard not in ["1", "2", "3"]:
        print("bad number")
    print('compete')