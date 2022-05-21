import subprocess

from escpos.printer import File


class VKP80(object):
    def __init__(self, printername):
        self.printername = printername

    def print_giftcard(self, ordercode, secret, amount):
        p = File('/tmp/fnordload_giftcard')
        p.textln("Order Code: {}".format(ordercode))
        p.textln("Secret: {}".format(secret))
        p.textln("Amount: {}".format(amount))
        p.qr(secret, size=13, center=True)
        p.ln(2)
        p.control('FF')

        subprocess.check_call(
            #['lpr', '-P', 'VKP80', '/tmp/fnordload_giftcard']
            ['lp', '-d', 'VKP80', '/tmp/fnordload_giftcard']
        )
