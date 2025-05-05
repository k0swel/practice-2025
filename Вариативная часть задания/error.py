class Error:
    __text: str = None #текст ошибки
    def __init__(self, error_text: str):
        self.__text = error_text

    def text(self):
        return self.__text