# simulation engine
import enum
import time
import json
import random
from pathlib import Path
from openai import OpenAI
from persona import PersonaGenerator, generate_emotions_and_arousals
# simulate conversation between two users for now

class Engine:
    def __init__(self, save_dir: str, turn_per_simulation = 10):
        # init two personas
        self.turn_per_simulation = turn_per_simulation # number of conversation turns per simulation
        self.agents = self._init_agents() # initialize chatbot and user agents
        self.chatbot_persona = str(self.agents[0])
        self.user_persona = str(self.agents[1])
        self.emotion_combination = generate_emotions_and_arousals() # list of ((emotion1, emotion2), (arousal1, arousal2))
        self.conversation = [] # list of list of (agent_type, mood, content)
        self.conversation_str = "" # keep track of conversation in string format
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

    def append_conversation_str(self, emotion_shift, curr_conversation):
        '''
        gather and format all previous conversation
        '''
        if len(self.conversation_str) == 0:
            self.conversation_str = "Heres some example conversation thats are previously generated:\n"
        formatted_conv = ""
        formatted_conv += f"Emotion Shift: {emotion_shift}\n"
        for dialogue in curr_conversation:
            if dialogue[0] == 1:
                # chatbot
                formatted_conv += f"Chatbot: {dialogue[2]}\n"
            else:
                # user
                formatted_conv += f"User: {dialogue[2]}\n"
        self.conversation_str += formatted_conv
                    

    def parameter_generation(self, emotion_shift):
        '''
        generate parameter for the current simulation iteration
        '''
        emotion1, emotion2 = emotion_shift[0]
        arousal1, arousal2 = emotion_shift[1]
        emotion_shift = f"({emotion1}, {arousal1}) -> ({emotion2}, {arousal2})"
        params = {
            'MOOD SHIFT': emotion_shift,
            'TURN PER SIMULATION': self.turn_per_simulation
        }
        params = ''.join([f'{k}: {v}\n' for k, v in params.items()])
        return "PARAMETER:\n" + params.strip()

    def prompt_generation(self, chatbot_start):
        # randomly select a which agent to start first
        generation_format = "CHATBOT: [...]\nUSER: [...]\n" if chatbot_start else "USER: [...]\nCHATBOT: [...]\n"
        # prompt for message generation
        msg = f"Simulate a conversation between the CHATBOT and USER, aligning with their individual persona.\n"
        msg += "The USER dialogue should follow the emotion shift as specified in the parameter.\n"
        msg += f"Generate {self.turn_per_simulation} turns of conversation, with the following format:\n"
        msg += f"{generation_format}"
        return msg

    def simulate(self, emotion_shift):
        '''
        Simulate a entire conversation between chatbot and user agents
        '''
        # randomly select a which agent to start first
        chatbot_start = True if random.random() > 0.5 else False
        parameter = self.parameter_generation(emotion_shift)
        # prompt for message generation
        msg = self.prompt_generation(chatbot_start)
        content = f"{self.conversation_str}\n\n{parameter}\n\n{msg}"
        # save to tmp to see format, sanity check
        with open(f'{self.output_dir}/{emotion_shift}.txt', 'w') as f:
            f.write("============================================\n")
            f.write("SYSTEM:\n")
            f.write("CHATBOT PERSONA:\n" + self.chatbot_persona + "\n")
            f.write("USER PERSONA:\n" + self.user_persona + "\n")
            f.write("============================================\n")
            f.write("CONTENT:\n")
            f.write(content)
        print(emotion_shift)
        # send to gpt
        #response = self.sent_to_gpt(persona, content)
        #mood, content = self.process_response(response, chatbot_turn)
        #self.conversation.append((1 if chatbot_turn else 2, mood, content))
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

    def start(self):
        # end conversation after 100 turn
        # simulate over all possible emotion combination
        for emotion_shift in self.emotion_combination:
            self.simulate(emotion_shift)
            self.append_conversation_str(emotion_shift, self.conversation)
            

    
    def sent_to_gpt(self, persona: int, msg: str):
        return "You [MOOD]: I'm feeling pretty happy, and I hope the weather is nice for a beach day soon. How about you?" # Hardcode for testing
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": msg}])
        # save to output dir and parse response
        response = completion.choices[0].message.content
        return response