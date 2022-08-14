import json
import time


class PrintItem:
    def __init__(self, item_id='', filename='', scale=100, rotation=False, width=0, height=0, text='', qr_code=False):
        self.item_id = str(item_id)
        self.filename = str(filename)
        self.scale = int(scale)
        self.rotation = bool(rotation)
        self.width = int(width)
        self.height = int(height)
        self.timestamp = time.time()
        self.text = str(text)
        self.qr_code = bool(qr_code)
        self.printed = False

    def to_json(self):
        return json.dumps(self.__dict__)

    def from_json(self, json_str):
        self.__dict__ = json.loads(json_str)
        return self

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            return self.from_json(f.read())

    def save_to_file(self, filename):
        print('Saving to file: ' + filename)
        with open(filename, 'w') as f:
            f.write(self.to_json())
        return 0

    def get_item_id(self):
        return self.item_id

    def get_filename(self):
        return self.filename

    def get_scale(self):
        return self.scale

    def get_rotation(self):
        return self.rotation

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_timestamp(self):
        return self.timestamp

    def get_printed(self):
        return self.printed

    def get_text(self):
        return self.text

    def get_qr_code(self):
        return self.qr_code

    def set_printed(self, printed):
        self.printed = printed
        return 0

    def set_scale(self, scale):
        self.scale = scale
        return 0

    def set_rotation(self, rotation):
        self.rotation = rotation
        return 0

    def set_width(self, width):
        self.width = width
        return 0

    def set_height(self, height):
        self.height = height
        return 0

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
        return 0

    def set_text(self, text):
        self.text = text
        return 0

    def set_qr_code(self, qr_code):
        self.qr_code = qr_code
        return 0