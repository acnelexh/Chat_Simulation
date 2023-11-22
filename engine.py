# simulation engine
import enum
import time
from pathlib import Path
from openai import OpenAI
from persona import PersonaGenerator, generate_emotions_and_arousals
# simulate conversation between two users for now

class Engine:
    def __init__(self, save_dir: str):
        # init two personas
        self.agents = self._init_agents()
        self.tmp = generate_emotions_and_arousals()
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

    def _init_agents(self) -> str:
        '''
        initialize user persona
        return:
            user_persona: nlp description of the user
        '''
        persona_generator = PersonaGenerator()
        agents = [persona_generator.generate_chatbot(), persona_generator.generate_user()]
        return agents

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
        # TODO possibly modify the prompt
        persona = "Forget all previous instructions. You are now taking on the role of a persona with the following information.\n"
        persona += str(self.agents[turn])
        return persona + '\n'

    def mood_generation(self):
        '''
        generate mood for the user
        '''
        # randomly generate mood TODO
        # CONST SAD for now, need to define a function 
        # for mood generation, like valence = 9, arousal = 1, mood = happy
        # based on some function
        return 'SAD' # make it sad
    
    def is_chatbot_turn(self, turn):
        '''
        Prompt differntly based on chatbot or human
        '''
        if self.agents[turn % 2].p_type == 1:
            return True
        return False

    def parameter_generation(self, chatbot):
        '''
        generate parameter for the user
        '''
        # TODO randomly generate emotion parameters
        # only human should have emotion
        # TODO potentially add more parameters
        if chatbot:
            params = {
                'RESPONSE LENGTH': 'SHORT'
            }
        else:
            # Add in mood generation for human user
            params = {
                'MOOD': self.mood_generation(),
                'RESPONSE LENGTH': 'SHORT'
            }
        params = ''.join([f'{k}: {v}\n' for k, v in params.items()])
        return "PARAMETER:\n" + params.strip()

    def take_turn(self, turn):
        # get user input
        chatbot_turn = self.is_chatbot_turn(turn)
        previous_conversation = self.get_previous_conversation(chatbot_turn)
        parameter = self.parameter_generation(chatbot_turn)
        # format based on chatbot or human persona
        format = "You: [...]" if chatbot_turn else "You [$MOOD]: [...]"
        # prompt for message generation
        msg = f"Generate a 1-sentence response that remains consistent with (1) mood and (2) previous dialogues, aligning with your (3) persona.\nPresent it in the format: {format}"
        content = f"{previous_conversation}\n\n{parameter}\n\n{msg}"
        persona = self.get_persona(turn%2)
        # save to tmp to see format, sanity check
        with open(f'{self.output_dir}/{turn}.txt', 'w') as f:
            f.write("============================================\n")
            f.write("SYSTEM:\n")
            f.write(persona)
            f.write("============================================\n")
            f.write("CONTENT:\n")
            f.write(content)
        # send to gpt
        response = self.sent_to_gpt(persona, content)
        mood, content = self.process_response(response, chatbot_turn)
        self.conversation.append((1 if chatbot_turn else 2, mood, content))
        #return response

    def process_response(self, response, chatbot):
        '''
        process response from chatgpt, assume response is in the right format
        '''
        if chatbot:
            content = response.split(':')[1]
            mood = "NULL"
        else:
            header, content = response.split(':')
            mood = header.split(' ')[1]
        return mood.strip("[").strip(']'), content.strip()

    def start(self, turn = 100):
        # end conversation after 100 turn
        for i in range(1,turn):
            self.take_turn(i) # assuming two users and chatbot start first
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