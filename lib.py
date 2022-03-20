import os
from datetime import datetime

DEBUG = True


class Logger:
    dir = "logs"

    def __init__(self, name="misc"):
        self.name = name
        self.date = datetime.now()
        self.filename = f"logs/logs_{name}_{str(self.date).replace(' ', 'T').replace(':', '-')}.txt"

        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def log(self, *args, **kwargs):
        # Print message in console
        if DEBUG:
            print(*args, **kwargs)
        # Log message
        with open(self.filename, 'a') as file:
            file.write(f"[{datetime.now()}]: {' '.join(args)}\n")
