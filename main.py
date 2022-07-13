from ParseVCF import VcardFile
import WhatsUp

def makephonelist():
    phones = []
    with open("vcard/phones.csv") as file:
        file.readline()
        while True:
            line = file.readline()
            if not line:
                break
            line = line.split(",")
            if line[0][0] == "+":
                phones.append(line[0].replace(" ", ""))
        return phones
makephonelist()

if __name__ == '__main__':
    vcf = VcardFile()
    print("from vCard csv - 1; from csv to vCard - 2")
    opencard = input()
    if opencard == 1:
        vcf.openvcard("Contacts.vcf")
        vcf.saveimage()
        vcf.savetocsv()
    if opencard == 2:
        vcf.savevcard("Contacts_new.vcf")
    if opencard == "3":
        WhatsUp.connectwp(makephonelist())
    else:
        print("bad number")
    print('compete')