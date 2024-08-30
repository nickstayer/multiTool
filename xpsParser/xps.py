class Xps:
    def __init__(self, name, info, passw, passw_phrase):
        self.name = name
        self.info = info
        self.passw = passw
        self.passw_phrase = passw_phrase

    def __str__(self):
        return f"Name: {self.name}\r\nInfo: {self.info}\r\nPassword: {self.passw}\r\nPhrase: {self.passw_phrase}"
