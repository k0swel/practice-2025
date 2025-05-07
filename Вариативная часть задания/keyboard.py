from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

def start_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    list_of_buttons: list[KeyboardButton] = [KeyboardButton(text='Узнать погоду в городе🌆'),
                                             KeyboardButton(text='Узнать погоду в моём местоположении🌎',
                                                            request_location=True)]  # список кнопок
    [markup.add(button) for button in list_of_buttons]
    return markup

def stop_trying() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    list_of_buttons: list[KeyboardButton] = [KeyboardButton(text='🔴Прекратить попытки')]
    [markup.add(button) for button in list_of_buttons]
    return markup