from ParseVCF import VcardFile
#import WhatsUp

if __name__ == '__main__':
    vcf = VcardFile()
    vcf.openvcard("Contacts.vcf")
    vcf.saveimage()
    vcf.savetocsv()
    vcf.savevcard("Contacts_new.vcf")
    print('compete')