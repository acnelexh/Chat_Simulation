# simulation engine
import enum
import time
from pathlib import Path
from openai import OpenAI
from persona import Persona, PersonaGenerator
# simulate conversation between two users for now

class Engine:
    def __init__(self, save_dir: str):
        # init two personas
        self.users = self._init_user()
        # init random context
        #self.context = self._init_context()
        # init conversaion with chitchat
        chitchat = ['How are you?', 'Whats up', 'How is your day?', 'How is the weather?', 'Hows your weekend?']
        # chatbot dont need no emotion
        # 1 = chatbot, 2 = human
        self.conversation = [(1, 'NULL', chitchat[2])] # (agent_type, mood, content)
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

    def get_previous_conversation(self, chatbot):
        '''
        generate previous conversation
        '''
        # TODO add previous conversation
        conversation = "Here is the previous conversation:\n"
        if chatbot:
            for c in self.conversation:
                if c[0] == 1:
                    conversation += f"You: {c[2]}\n"
                else:
                    conversation += f"User: {c[2]}\n"
        else:
            for c in self.conversation:
                if c[0] == 2:
                    conversation += f"You: {c[2]}\n"
                else:
                    conversation += f"Chatbot: {c[2]}\n"
        return conversation.strip()

    def get_persona(self, turn):
        persona = "Forget all previous instructions. You are now taking on the role of a persona with the following information.\n"
        # TODO add persona from get_persona in persona.py
        #persona += "Age: 20\nPhysical Health: Go to gym\nStress Trigger:Deadline\nLikes:Sushi and beaches\ndislike:bugs\n"
        persona += self.users[turn].get_persona()
        return persona + '\n'

    def mood_generation(self):
        '''
        generate mood for the user
        '''
        # randomly generate mood TODO
        # CONST SAD for now
        return 'SAD' # make it sad
    
    def is_chatbot_turn(self, turn):
        if self.users[turn % 2].p_type == 1:
            return True
        return False

    def parameter_generation(self, chatbot):
        '''
        generate parameter for the user
        '''
        # TODO randomly generate emotion parameters
        # only human should have emotion
        if chatbot:
            params = {
                'RESPONSE LENGTH': 'SHORT'
            }
        else:
            params = {
                'MOOD': self.mood_generation(),
                'RESPONSE LENGTH': 'SHORT'
            }
        params = ''.join([f'{k}: {v}\n' for k, v in params.items()])
        return "PARAMETER:\n" + params

    def user_turn(self, turn):
        # get user input
        chatbot_turn = self.is_chatbot_turn(turn)
        previous_conversation = self.get_previous_conversation(chatbot_turn)
        parameter = self.parameter_generation(chatbot_turn)
        # format based on chatbot or human persona
        format = "You: [...]" if chatbot_turn else "You [$MOOD]: [...]"
        # prompt for message generation
        msg = f"Generate a 1-sentence response that remains consistent with the mood and previous dialogues, aligning with your persona.\nPresent it in the format: {format}"
        content = f"{previous_conversation}\n\n{parameter}\n\n{msg}"
        persona = self.get_persona(turn%2)
        # save to tmp to see format
        with open(f'{self.output_dir}/{turn}.txt', 'w') as f:
            f.write("SYSTEM:\n")
            f.write(persona)
            f.write("CONTENT:\n")
            f.write(content)
        # send to gpt
        response = self.sent_to_gpt(persona, content)
        mood, content = self.process_response(response, chatbot_turn)
        self.conversation.append((1 if chatbot_turn else 2, mood, content))
        return response

    def process_response(self, response, chatbot):
        '''
        process response
        '''
        if chatbot:
            content = response.split(':')[1]
            mood = "NULL"
        else:
            header, content = response.split(':')
            mood = header.split(' ')[1]
        return mood.strip("[").strip(']'), content.strip()

    def start(self):
        # end conversation after 100 turn
        for i in range(1,5):
            # user turn
            response = self.user_turn(i) # assuming two users
        # save all diaglogues as transcript
        with open(f'{self.output_dir}/transcript.txt', 'w') as f:
            for conv in self.conversation:
                f.write(f'User {conv[0]}: {conv[2]}\n')
        print("Conversation ended")

    
    def sent_to_gpt(self, persona: int, msg: str):
        #return "You [MOOD]: I'm feeling pretty happy, and I hope the weather is nice for a beach day soon. How about you?" # Hardcode for testing
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": msg}])
        # save to output dir and parse response
        response = completion.choices[0].message.content
        return response