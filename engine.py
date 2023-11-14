# simulation engine
import enum
import time
from pathlib import Path
from openai import OpenAI
from persona import Persona
# simulate conversation between two users for now

class Engine:
    def __init__(self, save_dir: str):
        # init two personas
        self.users = self._init_user()
        # init random context
        self.context = self._init_context()
        # init openai client
        self.client = OpenAI()
        # file io stuff
        self.output_dir = Path(save_dir)
        if self.output_dir.exists() == False:
            self.output_dir.mkdir()

    def _init_user(self) -> str:
        '''
        initialize user persona
        return:
            user_persona: nlp description of the user
        '''

        user_persona = [Persona(1), Persona(2)]
        return user_persona
    
    def _init_context(self) -> str:
        '''
        initialize context randomly
        return:
            context: nlp description of the context
        '''
        context = None
        return context

    def user_turn(self, turn):
        persona = self.users[turn]
        # get user input
        msg = input("User: ")
        # send to gpt
        response = self.sent_to_gpt(persona, msg)

    def start(self):
        # end conversation after 100 turn
        for i in range(100):
            # user turn
            self.user_turn(i % 2) # assuming two users
    
    def sent_to_gpt(self, persona: Persona, msg: str):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": persona.get_persona()},
                {"role": "user", "content": msg}])

        # save to output dir and parse response
        response = completion.choices[0].message.content
        return response

