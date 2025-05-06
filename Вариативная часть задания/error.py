class Error(Exception):
    text: str = None #текст ошибки
    def __init__(self, error_text: str):
        self.text = error_text

    def text_error(self):
        return self.text