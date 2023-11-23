# simulation engine
import json
import random
from pathlib import Path
from openai import OpenAI
from persona import PersonaGenerator, generate_emotions_and_arousals

class Engine:
    def __init__(self, save_dir: str, turn_per_simulation = 10):
        # init two personas
        self.turn_per_simulation = turn_per_simulation # number of conversation turns per simulation
        self.agents = self._init_agents() # initialize chatbot and user agents
        self.chatbot_persona = str(self.agents[0])
        self.user_persona = str(self.agents[1])
        self.emotion_combination = generate_emotions_and_arousals() # list of ((emotion1, emotion2), (arousal1, arousal2))
        self.conversation = [] # list of list of (agent_type, content)
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
        emotion1, emotion2 = emotion_shift[0]
        arousal1, arousal2 = emotion_shift[1]
        emotion_shift = f"({emotion1}, {arousal1}) -> ({emotion2}, {arousal2})"
        formatted_conv = f"Dialogue {len(self.conversation) + 1}:\n"
        formatted_conv += f"EMOTION SHIFT: {emotion_shift}\n"
        for dialogue in curr_conversation:
            if dialogue[0] == 1:
                formatted_conv += f"CHATBOT: {dialogue[1]}\n"
            else:
                formatted_conv += f"USER: {dialogue[1]}\n"
        self.conversation_str += formatted_conv + "\n"
    

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
        generation_format = "CHATBOT: [...]\nUSER: [...]" if chatbot_start else "USER: [...]\nCHATBOT: [...]"
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
        system = "CHATBOT PERSONA:\n" + self.chatbot_persona + "\n"
        system += "USER PERSONA:\n" + self.user_persona + "\n"
        content = f"{parameter}\n\n{msg}"
        # save to tmp to see format, sanity check
        with open(f'{self.output_dir}/{emotion_shift}.txt', 'w') as f:
            f.write("============================================\n")
            f.write("SYSTEM:\n")
            f.write(system)
            f.write("============================================\n")
            f.write("CONTENT:\n")
            f.write(content)
        # send to gpt
        response = self.sent_to_gpt(system, content)
        dialogue = self.process_response(response)
        self.conversation.append(dialogue)
        return dialogue

    def process_response(self, response):
        '''
        process response from chatgpt, assume response is in the right format
        '''
        new_dialogue = []
        dialogue_parsed = response.strip().split('\n')
        for dialogue in dialogue_parsed:
            if len(dialogue) == 0:
                continue
            agent, content = dialogue.split(':')
            if agent == 'CHATBOT':
                new_dialogue.append((1, content))
            else:
                new_dialogue.append((2, content))
        return new_dialogue
                

    def start(self):
        # end conversation after 100 turn
        # simulate over all possible emotion combination
        for emotion_shift in self.emotion_combination:
            dialogue = self.simulate(emotion_shift)
            self.append_conversation_str(emotion_shift, dialogue)
            # save to output dir
            with open(f'{self.output_dir}/{emotion_shift}.json', 'w') as f:
                f.write(json.dumps(dialogue))
            print(f"Finished simulation for emotion shift: {emotion_shift}")
    
    def sent_to_gpt(self, system: int, content: str):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": content}])
        # save to output dir and parse response
        response = completion.choices[0].message.content
        return response