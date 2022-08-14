import telebot
from print_item import PrintItem
from config import Config

config = Config().load_from_file('./config/config.json')
bot = telebot.TeleBot(config.get_bot_token())


def process_image(item_id, file_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = config.get_data_path()
    filename = save_path + item_id + '.jpg'
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    item = PrintItem(item_id, filename, 100, False, 0, 0)
    item.save_to_file(save_path + item_id + '.json')


@bot.message_handler(content_types=['photo'])
def photo(message):
    if not config.is_in_white_list(message.from_user.id):
        return
    file_id = message.photo[-1].file_id
    item_id = str(message.from_user.id) + '-' + str(message.id)
    process_image(item_id, file_id)


@bot.message_handler(content_types=['document'])
def document(message):
    if not config.is_in_white_list(message.from_user.id):
        return
    file_id = message.document.file_id
    item_id = str(message.from_user.id) + '-' + str(message.id)
    process_image(item_id, file_id)


@bot.message_handler(content_types=['text'])
def text(message):
    if not config.is_in_white_list(message.from_user.id):
        return
    item_id = str(message.from_user.id) + '-' + str(message.id)
    item = PrintItem(item_id)
    item.set_text(message.text)
    save_path = config.get_data_path()
    item.save_to_file(save_path + item_id + '.json')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Печать стикеров на brother ql-700 просто отправьте картинку")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
