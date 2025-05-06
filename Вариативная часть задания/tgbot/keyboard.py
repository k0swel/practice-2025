from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

def start_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    list_of_buttons: list[KeyboardButton] = [KeyboardButton(text='Узнать погоду в городе🌆'),
                                             KeyboardButton(text='Узнать погоду в моём местоположении🌎',
                                                            request_location=True)]  # список кнопок
    for button in list_of_buttons:
        markup.add(button)
    return markup