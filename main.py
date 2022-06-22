from ParseVCF import VcardFile
#import WhatsUp

if __name__ == '__main__':
    vcf = VcardFile()
    print("from vCard csv - 1; from csv to vCard - 2")
    opencard = input(1)
    if opencard == 1:
        vcf.openvcard("Contacts.vcf")
        vcf.saveimage()
        vcf.savetocsv()
    if opencard == 2:
        vcf.savevcard("Contacts_new.vcf")
    else:
        print("bad number")
    print('compete')