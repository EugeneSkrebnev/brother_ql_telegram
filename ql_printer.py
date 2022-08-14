from PIL import Image
from brother_ql.conversion import convert
from brother_ql.backends.helpers import discover
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
from print_item import PrintItem
import time
from image_processor import *


class QLPrinterStatus:
    def __init__(self):
        self.is_on = False
        self.error = ''
        self.is_ok = False

    def set_error(self, error):
        print(error)
        self.error = error
        self.is_ok = False
        return 0

    def set_ok(self):
        self.is_on = True
        self.error = ''
        self.is_ok = True
        return self

    def set_on_status(self, is_on):
        if self.is_ok:
            self.is_on = is_on
        return self


class QLPrinter:
    def __init__(self, test_mode=True):
        self.test_mode = test_mode
        self.pin = 4
        if not self.test_mode:
            import RPi.GPIO as GPIO  # на Raspberry
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
        self.qlr = None
        self.usb_address = ''
        self.status = QLPrinterStatus()
        self.init_printer()

    def __del__(self):
        if not self.test_mode:
            GPIO.cleanup()

    def init_printer_obj(self, usb):
        self.usb_address = usb
        self.status.set_ok()

    def init_printer(self, try_count=3):
        printers = discover()
        if len(printers) == 0:
            self.click_switch()
            if try_count > 0:
                return self.init_printer(try_count - 1)
            self.status.set_error('No printers found')
            return -1
        else:
            if len(printers) > 1:
                self.status.set_error('More than one printer found')
                return -1
            else:
                self.init_printer_obj(printers[0]['identifier'])
                return 0

    def status(self):
        return self.status

    def click_switch(self):
        if not self.test_mode:
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.pin, GPIO.LOW)
        else:
            print('Switch printer')
            time.sleep(1)

    def print_item(self, item: PrintItem):
        img = image_with_696_width_from_path(item.get_filename())
        if img is None:
            return {'instructions_sent': False, 'outcome': 'Image not found',
                    'did_print': False, 'ready_for_next_job': True}

        self.qlr = BrotherQLRaster('QL-700')
        self.qlr.exception_on_warning = True
        instructions = convert(
            qlr=self.qlr,
            images=[img],  # Takes a list of file names or PIL objects.
            label='62',
            rotate='0',  # 'Auto', '0', '90', '270'
            threshold=70.0,  # Black and white threshold in percent.
            dither=False,
            compress=False,
            red=False,  # Only True if using Red/Black 62 mm label tape.
            dpi_600=False,
            hq=True,  # False for low quality.
            cut=True
        )
        status = send(instructions=instructions, printer_identifier=self.usb_address,
                      backend_identifier='linux_kernel', blocking=True)
        return status
