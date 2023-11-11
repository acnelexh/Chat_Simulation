'''
Persona class for chatbot
Create persona for the chatbot from template
'''
from pathlib import Path

import enum

class PersonaType(enum.Enum):
    CHATBOT = 1
    USER = 2

class Persona():
    def __init__(self, p_type: PersonaType):
        if p_type == PersonaType.CHATBOT:
            self.persona = self._define_chatbot()
        else:
            self.persona = self._define_user()

    def _define_chatbot(self):
        '''
        Generate persona for the chatbot
        '''
        pass
    
    def _define_user(self):
        '''
        Generate persona for the chatbot
        '''
        pass
    
    def get_persona(self):
        '''
        Get persona for the chatbot
        '''
        pass
        return self.persona
    

        