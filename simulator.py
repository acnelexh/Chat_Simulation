import enum
from pathlib import Path

class STATE(enum.Enum):
    SYSTEM = 0
    USER = 1


class simulator():
    def __init__(self):
        self.context = None # keep track of past conversation
        self.turn = STATE.SYSTEM # keep track of whose turn it is
        

    def context(self):
        pass

    def generate_persona(self):
        # generate a persona for the user
        param_list = Path('templates').glob('*.txt')
        param_list = [str(x).strip('.txt') for x in param_list]
        