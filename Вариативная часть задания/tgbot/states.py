from telebot.handler_backends import State, StatesGroup

class States(StatesGroup):
    wait_city = State() ## состояние ожидания ввода города.