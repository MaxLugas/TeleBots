import os
import logging
import telebot
from telebot import types
from Converter import Converter

TOKEN = os.getenv('TOKEN')    # token for the telegram API is located in .env
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    name = message.chat.first_name if message.chat.first_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.chat.id}) started bot")
    welcome_mess = 'Привет! Отправляй голосовое, я расшифрую!'
    bot.send_message(message.chat.id, welcome_mess)


@bot.message_handler(content_types=['voice'])
def get_audio_messages(message: types.Message):
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = str(message.message_id)
    name = message.chat.first_name if message.chat.first_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.chat.id}) download file {file_name}")

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    converter = Converter(file_name)
    os.remove(file_name)
    message_text = converter.audio_to_text()
    del converter
    bot.send_message(message.chat.id, message_text, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    logger.info("Starting bot")
    bot.polling(none_stop=True, timeout=123)