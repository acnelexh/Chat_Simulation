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
        # init conversaion with chitchat
        chitchat = ['How are you?', 'Whats up', 'How is your day?', 'How is the weather?', 'Hows your weekend?']
        self.conversation = [(0, 'NEUTRAL', chitchat[2]), (1, 'NEUTRAL', chitchat[3])] #TMP TODO for testing, might need better way to init
        # init openai client
        with open("MY_KEY", "r") as f:
            self.client = OpenAI(api_key=f.read().strip())
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
        REDACTED
        initialize context randomly
        return:
            context: nlp description of the context
        '''
        context = []
        return context

    def get_previous_conversation(self, turn):
        '''
        generate previous conversation
        '''
        dialog = "The previous conversation:\n"
        for conv in self.conversation:
            if conv[0] % 2 == turn % 2:
                dialog += f'You: {conv[2]}\n'
            else:
                dialog += f'User {conv[0]}: {conv[2]}\n'
        return dialog.strip()

    def get_persona(self, turn):
        persona = "Forget all previous instructions. You are now taking on the role of a persona with the following information.\n"
        # TODO add persona from get_persona in persona.py
        persona += "Age: 20\nPhysical Health: Go to gym\nStress Trigger:Deadline\nLikes:Sushi and beaches\ndislike:bugs\n"
        return persona

    def mood_generation(self):
        '''
        generate mood for the user
        '''
        # randomly generate mood TODO
        # CONST SAD for now
        return 'SAD' # make it sad
    
    def parameter_generation(self):
        '''
        generate parameter for the user
        '''
        params = {
            'MOOD': 'SAD',
            'RESPONSE LENGTH': 'SHORT'
        }
        params = ''.join([f'{k}: {v}\n' for k, v in params.items()])
        return "PARAMETER:\n" + params

    def user_turn(self, turn):
        persona = self.get_persona(turn%2)
        # get user input
        previous_conversation = self.get_previous_conversation(turn)
        #label = "The label for [MOOD] include {anger, sad, happy, stress}"
        parameter = self.parameter_generation()
        format = f"You [$MOOD]: [...]"
        msg = f"Generate a 1-sentence response that remains consistent with the mood and previous dialogues, aligning with your persona. Present it in the format: {format}"
        content = f"{persona}\n\n{previous_conversation}\n\n{parameter}\n\n{msg}"
        # save to tmp to see format
        with open(f'{self.output_dir}/{turn}.txt', 'w') as f:
            f.write(content)
        # send to gpt
        response = self.sent_to_gpt(turn%2, content)
        mood, content = self.process_response(response)
        self.conversation.append((turn % 2, mood, content))
        return response

    def process_response(self, response):
        '''
        process response
        '''
        header, content = response.split(':')
        mood = header.split(' ')[1]
        return mood.strip("[").strip(']'), content.strip()

    def start(self):
        # end conversation after 100 turn
        for i in range(5):
            # user turn
            response = self.user_turn(i) # assuming two users
        # save all diaglogues as transcript
        with open(f'{self.output_dir}/transcript.txt', 'w') as f:
            for conv in self.conversation:
                f.write(f'User {conv[0]}: {conv[2]}\n')
        print("Conversation ended")

    
    def sent_to_gpt(self, turn: int, msg: str):
        #return "You [MOOD]: I'm feeling pretty happy, and I hope the weather is nice for a beach day soon. How about you?" # Hardcode for testing
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.get_persona(turn)},
                {"role": "user", "content": msg}])
        # save to output dir and parse response
        response = completion.choices[0].message.content
        return response
