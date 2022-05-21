import logging
import logging.config
import logging.handlers
import sys
import time

import fnordload_pretixgiftcard as fnordload


class Fnordload(object):
    def __init__(self, eSSPport="/dev/ttyACM0"):
        if len(sys.argv) < 7:
            print("fnordload.py etc/logging.ini https://pretix.eu 12345token67890 organizer event 123")
            sys.exit()
        self._logger = logging.getLogger(__name__)
        self._lcd = fnordload.LCD()
        self._pretix = fnordload.pretixAPI(
            sys.argv[2],  # host
            sys.argv[3],  # token
            sys.argv[4],  # organizer
            sys.argv[5],  # event
            sys.argv[6],  # product
        )
        self._printer = fnordload.VKP80('VKP80')
        self._note_validator = fnordload.NoteValidator(device=eSSPport)
        self._setup()
        self._order_code = None
        self._order_creation_in_progress = False
        self._order_created = False

    def _setup(self):
        self._lcd.setup()

    def main(self):
        self._note_validator._set_inhibits(inhibits=[1, 1, 1, 1, 1, 0])
        accepted_values = self._note_validator.get_accepted_values()
        self._lcd.show_accepted_values(accepted_values)

        try:
            amount = self._note_validator.read_note(
                think_callback=self._lcd.thinking,
                bill_in_callback=self.noteread_callback
            )
            self._lcd.payout_in_progress()
            print('Converting {} to voucher with cart_id {}'.format(amount, self._order_code))
            state = self._pretix.mark_order_as_paid(self._order_code)
            print('Payment state for order {}: {}'.format(self._order_code, state))
            if state == 'confirmed':
                secret = self._pretix.get_secret(self._order_code)
                print('Giftcard secret for order {}: {}'.format(self._order_code, secret))
                self._printer.print_giftcard(self._order_code, secret, amount)
                self.cleanup()
        except fnordload.InvalidNoteError:
            self._lcd.rejected_note()
            self.cleanup()
            time.sleep(2)
        except fnordload.TimeoutError:
            self.cleanup()
            pass

    def cleanup(self):
        self._order_code = None
        self._order_creation_in_progress = False
        self._order_created = False

    def noteread_callback(self, value):
        if not self._order_creation_in_progress:
            self._order_creation_in_progress = True
            self._lcd.reading_note(value)
            self.create_cart(value)
            return False
        else:
            if self._order_created:
                return True

        return False

    def create_cart(self, value):
        self._order_code = self._pretix.create_order(value)
        if self._order_code:
            self._order_created = True
            print("order created", self._order_code)


if __name__ == "__main__":
    logging.config.fileConfig(sys.argv[1])
    logger = logging.getLogger("fnordload")
    logger.info('Starting fnordload')

    try:
        fl = Fnordload()

        while True:
            fl.main()
    except Exception as e:
        logger.exception(e)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
