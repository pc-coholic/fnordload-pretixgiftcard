import logging
from lcd2usb import LCD as LCDServer


class LCD(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.__lcd = LCDServer.find_or_die()
        self.__lcd.clear()
        self.backlight_on()

    def write(self, line1="", line2="", line3="", line4=""):
        self.__lcd.clear()
        self.__lcd.write(line1, 0, 0)
        self.__lcd.write(line2, 0, 1)
        self.__lcd.write(line3, 0, 2)
        self.__lcd.write(line4, 0, 3)

        self._logger.info('{} | {} | {} | {} '.format(line1, line2, line3, line4))

    def setup(self):
        self.write("Fnordload booting", "", "Please stand by...")

    def show_accepted_values(self, values):
        accepted = [str(x) for x in values]

        if len(accepted) == 0:
            self.write("Sorry!","No change available", "", "             The MGT")
        else:
            self.write("Giving Change", "Accepting (Euro):", ", ".join(accepted),"        Insert money")

    def backlight_off(self):
        self.__lcd.set_brightness(0)

    def backlight_on(self):
        self.__lcd.set_brightness(255)

    def out_of_order(self):
        self.write("Sorry!","Fnordload is currently", "out of order.", "             The MGT")
        #self.backlight_off()

    def reading_note(self, value=0):
        #self.backlight_off()

        if value == 0:
            self.write("Reading note...")
        else:
            self.write("{} Euro note read".format(value))

    def cashed_note(self, value):
        self.backlight_on()

        self.write("Cashed {} Euro".format(value))

    def payout_in_progress(self):
        self.write("Payout in Progress", "", "", "Please stand by")

    def rejected_note(self):
        self.write("Sorry, this note", "cannot be accepted" , "at this time.")

    def thinking(self):
        self.write("Thinking...", "", "", "Please stand by")
