class Intents:
    def __init__(self):
        self.messages = False
        self.message_content = False
        self.guilds = False
    @classmethod
    def default(cls):
        return cls()

def setup():
    pass
