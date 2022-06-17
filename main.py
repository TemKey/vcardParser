from ParseVCF import VcardFile
#import WhatsUp

if __name__ == '__main__':
    vcf = VcardFile()
    vcf.openvcard("Contacts.vcf")
    vcf.savetocsv()
    print('compete')