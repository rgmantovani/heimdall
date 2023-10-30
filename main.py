import logging

# https://github.com/julzhk/usb_barcode_scanner
# from "usb-barcode-scanner.scanner" import BarcodeReader
from scanner import BarcodeReader

if __name__ == '__main__':

    reader = BarcodeReader(device_path="/dev/hidraw1")
    try:
        while True:
            upcnumber = reader.read_barcode()
            print(upcnumber)
    except KeyboardInterrupt:
        logging.debug('Keyboard interrupt')
    except Exception as err:
        logging.error(err)
        