import subprocess

from escpos.printer import File


class VKP80(object):
    def __init__(self, printername):
        self.printername = printername
        self.printfile = '/tmp/fnordload_giftcard'

    def print_giftcard(self, ordercode, secret, amount):
        self.p = File(self.printfile)
        self.p.textln("Order Code: {}".format(ordercode))
        self.p.textln("Secret: {}".format(secret))
        self.p.textln("Amount: {}".format(amount))
        self.p.qr(secret, size=13, center=True)
        self.p.ln(2)
        self.p.set(bold=True)
        self.p.textln("Please keep this barcode safe and treat it like cash, as it is non-replaceable.")
        self.p.set()
        self.p.ln(2)
        self.p.control('FF')
        self.print()

    def print_failure(self, ordercode):
        self.p = File(self.printfile)
        self.p.textln("Order Code: {}".format(ordercode))
        self.p.ln(2)
        self.p.textln("Sorry!")
        self.p.ln(2)
        self.p.textln("Due to technical issues, your order could not be completed.")
        self.p.ln(2)
        self.p.textln("Please call DECT# CASH (2274) and we will sort you out.")
        self.p.ln(2)
        self.p.set(bold=True)
        self.p.textln("Please keep this receipt as it serves as your proof of purchase!")
        self.p.set()
        self.p.ln(2)
        self.p.textln("Please accept our sincere apologies for the inconvenience caused.")
        self.p.ln(2)
        self.p.control('FF')
        self.print()

    def print(self):
        subprocess.check_call(
            #['lpr', '-P', self.printername, '/tmp/fnordload_giftcard']
            ['lp', '-d', self.printername, '/tmp/fnordload_giftcard']
        )