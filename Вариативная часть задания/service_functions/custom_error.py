from __future__ import annotations  # для корректной работы аннотаций типов
# --------------------------------------- КАСТОМНЫЙ КЛАСС ДЛЯ ОШИБОК -------------------------
class Error(Exception):
    text: str = None #текст ошибки
    last_error: Error = None # последняя ошибка
    def __init__(self, error_text: str):
        self.text = error_text
        Error.last_error = self

    def text_error(self):
        return self.text
# --------------------------------------------------------------------------------------------