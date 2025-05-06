import os
from dotenv import find_dotenv, load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot.types import ReplyKeyboardRemove
from telebot.asyncio_filters import StateFilter
import states
from keyboard import start_markup
import functions_tgbot
import asyncio

load_dotenv(find_dotenv()) # загружаем переменные из виртуального окружения в систему

BOT_TOKEN: str = os.getenv('tg_bot_token')

Bot: AsyncTeleBot = AsyncTeleBot(token=BOT_TOKEN,parse_mode='HTML')

@Bot.message_handler(commands=['start'])
async def hi_message(message: Message):
    await Bot.send_message(chat_id=message.chat.id, text='Добро пожаловать! Надеюсь я тебе понравлюсь.\n\n'
                                                   'Что я умею?\n\n'
                                                   'Ты можешь узнать погоду ☀️ в своём любомом городе, используя мой фунционал. Для этого тебе нужно нажать на кнопку ниже!\n\n'
                                                   'К сожалению мне не хватает материальной поддержки, чтобы отправлять тебе погоду из любого населенного пункта планеты(. Поэтому не обижайся, если я не смогу что-то найти❤️',
                     reply_markup=start_markup())

@Bot.message_handler(func = lambda message: message.text=='Узнать погоду в городе🌆')
async def check_weather_in_users_city(message: Message):
    await Bot.send_message(chat_id=message.json['chat']['id'], text='Старайтесь вводить название вашего города🌆 на английском языке (в противном случае я возможно не смогу найти информацию о погоде 🥺)', reply_markup=ReplyKeyboardRemove())
    await Bot.set_state(user_id=message.from_user.id, state=states.States.wait_city, chat_id=message.chat.id)

@Bot.message_handler(state=states.States.wait_city)
async def get_weather_city(message: Message):
    await Bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAM1aBkqNEts3jWS0Yd5HwABUW5Bxu_dAAIhQgACfycxSKvlnJR7gocvNgQ')
    await functions_tgbot.send_weather_by_city(message)
    await Bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)

@Bot.message_handler(content_types=['location'])
async def get_weather_location(message: Message):
    await Bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAM1aBkqNEts3jWS0Yd5HwABUW5Bxu_dAAIhQgACfycxSKvlnJR7gocvNgQ')
    await functions_tgbot.send_weather(message)


async def main(): # запускаем бота
    print('Bot launch successfully!')
    Bot.add_custom_filter(StateFilter(bot=Bot))
    await Bot.infinity_polling()

if __name__ == '__main__':
    asyncio.run(main())
