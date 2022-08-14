import json


class Config:
    def __init__(self):
        self.data_path = ''
        self.processed_path = ''
        self.bot_token = ''
        self.white_list = []

    def to_json(self):
        return json.dumps(self.__dict__)

    def from_json(self, json_str):
        self.__dict__ = json.loads(json_str)
        return 0

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            self.from_json(f.read())
        return self

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.to_json())
        return 0

    def get_data_path(self):
        return self.data_path

    def get_bot_token(self):
        return self.bot_token

    def set_data_path(self, data_path):
        self.data_path = data_path
        return 0

    def set_bot_token(self, bot_token):
        self.bot_token = bot_token
        return 0

    def is_in_white_list(self, user_id):
        if len(self.white_list) == 0:
            return True
        return user_id in self.white_list
