from telebot.types import  ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

# -------------------------------------------------Клавиатура при вводе /start-------------------------------------------
def start_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    list_of_buttons: list[KeyboardButton] = [KeyboardButton(text='Узнать погоду в городе🌆'),
                                             KeyboardButton(text='Узнать погоду в моём местоположении🌎',
                                                            request_location=True)]  # список кнопок
    [markup.add(button) for button in list_of_buttons]
    return markup
# -----------------------------------------------------------------------------------------------------------------------



# -----------------------------Inline клавиатура с предложением прекратить попытки получения погоды--------------------------
def stop_trying() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    list_of_buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text='🔴Прекратить попытки', callback_data='stop_trying')]
    [markup.add(button) for button in list_of_buttons]
    return markup
# ----------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------УДАЛЕНИЕ КЛАВИАТУРЫ---------------------------------------------------------
def delete_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
# ----------------------------------------------------------------------------------------------------------------------------