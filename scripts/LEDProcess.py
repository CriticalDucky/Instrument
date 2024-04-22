class LEDProcess:
    def __init__(self, name):
        self.name = name
        # {pixel_num: (r, g, b)}
        self.data = {}
        self.stopped = False

    def update(self):
        pass

    def report(self):
        return self.data

    def stop(self):
        self.stopped = True