import eSSP
import logging


class InvalidNoteError(Exception):
    pass


class TimeoutError(Exception):
    pass


class NoteValidator(object):
    def __init__(self, device='/dev/ttyACM0', inhibits_mask=[1, 1, 1, 1, 1, 1]):
        self._logger = logging.getLogger(__name__)
        self._eSSP = eSSP.eSSP(device)
        self._inhibits_mask = inhibits_mask
        self._inhibits = [0, 0, 0, 0, 0, 0]
        self._eSSP.sync()
        self._eSSP.enable_higher_protocol()
        self._channelvalues = self._eSSP.channel_values()[1]

    def _set_inhibits(self, inhibits=[0, 0, 0, 0, 0, 0, 0, 0]):
        self._logger.info("New inhibits: %s" % str(inhibits))
        self._inhibits = inhibits
        self._eSSP.set_inhibits(self._eSSP.easy_inhibit(inhibits), '0x00')

    def get_accepted_values(self):
        accepted = [x[0] for x in zip(self._channelvalues, self._inhibits) if x[1]]
        self._logger.info("Accepted values: %s" % str(accepted))
        return accepted

    def read_note(self, think_callback=lambda: None, bill_in_callback=lambda x: None):
        self._logger.info("Read note")

        self._logger.debug("read_note:60 with self._essp_lock")
        self._eSSP.enable()
        while True:
            poll = self._eSSP.poll()
            if len(poll) > 1 and len(poll[1]) == 2 and poll[1][0] == '0xef':
                if poll[1][1] == 0:
                    think_callback()
                else:
                    processed, success = bill_in_callback(self._channelvalues[poll[1][1] - 1])
                    while not processed:
                        self._eSSP.hold()
                        processed, success = bill_in_callback(self._channelvalues[poll[1][1] - 1])
                    if processed and not success:
                        self._eSSP.reject_note()
            elif len(poll) > 1 and len(poll[1]) == 2 and poll[1][0] == '0xee':
                self._logger.debug("read_note:73 with self._essp_lock")
                self._eSSP.disable()
                value = self._channelvalues[poll[1][1] - 1]
                self._logger.info("Read note of value: %f" % value)
                return value
            elif len(poll) > 1 and poll[1] == '0xed':
                self._logger.debug("read_note:80 with self._essp_lock")
                self._eSSP.disable()
                self._logger.warning("Read invalid note")
                raise InvalidNoteError()
            elif len(poll) > 1 and poll[0] == '0xf0':
                self._logger.warning(str(poll))


        self._eSSP.disable()

        self._logger.warning("Timeout while reading a note")
        raise TimeoutError()
