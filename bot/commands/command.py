class Command:
    def __init__(self, settings):
        self.session = {}
        self.settings = settings

    def run(self):
        self.process()
        self.session.clear()

    def process(self):
        raise NotImplementedError
