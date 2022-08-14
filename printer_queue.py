from config import Config
from print_item import PrintItem
import time
import os
from ql_printer import QLPrinter, QLPrinterStatus

config = Config().load_from_file('./config/config.json')

if __name__ == '__main__':
    data_path = config.get_data_path()
    ql_printer = QLPrinter(False)
    while True:
        time.sleep(1)
        json_files = [pos_json for pos_json in os.listdir(data_path) if pos_json.endswith('.json')]
        for json_file in json_files:
            item = PrintItem().load_from_file(data_path + json_file)
            if item.get_printed():
                continue

            status = ql_printer.print_item(item)
            if status['outcome'] == 'printed':
                item.set_printed(True)
                item.save_to_file(data_path + json_file)
        print('.')
