# simulation engine
import tqdm
import json
import random
from pathlib import Path
from openai import OpenAI
from persona import PersonaGenerator, generate_emotions_and_arousals

class Engine:
    '''
    Simulation engine for the chatbot
    '''
    def __init__(self, save_dir: str, resume: Path = None):
        # init openai client
        with open("MY_KEY", "r") as f:
            self.client = OpenAI(api_key=f.read().strip())
        # init emotion combination
        self.emotion_combination = generate_emotions_and_arousals() # list of ((emotion1, emotion2), (arousal1, arousal2))
        # check for resume
        if resume is None:
            # init two personas
            self.agents = self._init_agents() # initialize chatbot and user agents
            self.chatbot_persona = str(self.agents[0])
            self.user_persona = str(self.agents[1])
        else:
            # gather left over emotion combination
            # gather persona from resume dir
            self.resume_simulation(resume)
        # init conversation
        self.conversation = [] # list of list of (agent_type, content)
        # TODO keep or not?
        self.conversation_str = "" # keep track of conversation in string format
        # file io stuff
        if resume is None:
            self.output_dir = Path(save_dir)
            if self.output_dir.exists() == False:
                self.output_dir.mkdir()
            # save persona to output dir
            with open(f'{self.output_dir}/chatbot_persona.txt', 'w') as f:
                f.write(self.chatbot_persona)
            with open(f'{self.output_dir}/user_persona.txt', 'w') as f:
                f.write(self.user_persona)
        else:
            self.output_dir = resume
        # error io incase of crash from previous simulation
        self.error_log = self.output_dir/"log.txt"
        if self.error_log.exists() == False:
            self.error_log.touch()
    
    def format_save_name(self, emotion_shift):
        '''
        format the save name for the simulation
        args:
            emotion_shift: ((emotion1, emotion2), (arousal1, arousal2))
        return:
            save_name: str, save name for the simulation in the format of
            "emotion1_emotion2_arousal1_arousal2.txt"
        '''
        emotion1, emotion2 = emotion_shift[0]
        arousal1, arousal2 = emotion_shift[1]
        return f"{emotion1}_{emotion2}_{arousal1}_{arousal2}.txt"

    def resume_simulation(self, resume_dir: Path):
        '''
        resume simulation from previous simulation
        args:
            resume_dir: Path, path to the resume directory
        '''
        # glob all json file
        json_files = resume_dir.glob("*.json")
        # "emotion1_emotion2_arousal1_arousal2"
        file_stem = [str(f.stem)+".txt"  for f in json_files] 
        # turn them into emotion combination
        left_over = set([self.format_save_name(x) for x in self.emotion_combination]) - set(file_stem)
        if len(left_over) == 0:
            raise ValueError("No simulation to resume")
        # remove emotion combination that has been simulated
        self.emotion_combination = [x for x in self.emotion_combination if self.format_save_name(x) in left_over]
        # read in chatbot and user persona
        self.chatbot_persona = resume_dir.joinpath("chatbot_persona.txt").read_text()
        self.user_persona = resume_dir.joinpath("user_persona.txt").read_text()

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
        args:
            emotion_shift: ((emotion1, emotion2), (arousal1, arousal2))
            curr_conversation: list of (agent_type, content)
        '''
        if len(self.conversation_str) == 0:
            self.conversation_str = "Heres some example conversation thats are previously generated:\n"
        formatted_conv = self.format_dialogue(emotion_shift, curr_conversation)
        self.conversation_str += formatted_conv + "\n"
    
    def format_dialogue(self, emotion_shift, dialogue):
        '''
        Format the dialogue into a string for display
        Args:
            emotion_shift: ((emotion1, emotion2), (arousal1, arousal2))
            dialogue: list of (agent_type, content)
        Return:
            formatted string of the dialogue
        '''
        emotion1, emotion2 = emotion_shift[0]
        arousal1, arousal2 = emotion_shift[1]
        format_str = f"({emotion1}, {arousal1}) -> ({emotion2}, {arousal2})"
        format_str += f"EMOTION SHIFT: {emotion_shift}\n"
        for d in dialogue:
            if d[0] == 1:
                format_str += f"CHATBOT: {d[1]}\n"
            else:
                format_str += f"USER: {d[1]}\n"
        return format_str

    def parameter_generation(self, emotion_shift):
        '''
        generate parameter for the current simulation iteration
        args:
            emotion_shift: ((emotion1, emotion2), (arousal1, arousal2))
        return:
            params: dict of parameters
        '''
        emotion1, emotion2 = emotion_shift[0]
        arousal1, arousal2 = emotion_shift[1]
        emotion_shift = f"({emotion1}, {arousal1}) -> ({emotion2}, {arousal2})"
        number_of_turns = random.randint(7, 12)
        params = {
            'MOOD SHIFT': emotion_shift,
            'TURNS PER SIMULATION': number_of_turns
        }
        return params

    def prompt_generation(self, chatbot_start, params):
        '''
        generate prompt for the current simulation iteration
        args:
            chatbot_start: bool, whether chatbot start first
            params: dict of parameters
        return:
            msg: str, prompt for the current simulation
        '''
        # randomly select a which agent to start first
        generation_format = "CHATBOT: [...]\nUSER: [...]" if chatbot_start else "USER: [...]\nCHATBOT: [...]"
        # prompt for message generation
        msg = "Rules for the simulation:\n"
        msg = f"1. Simulate a conversation between the CHATBOT and USER, aligning with their individual persona.\n"
        msg += "2. The USER dialogue should follow the emotion shift as specified in the parameter.\n"
        msg += f"3. Generate {params['TURNS PER SIMULATION']} turns of conversation, with the following format:\n"
        msg += f"{generation_format}\n"
        msg += f"4. The USER should make their emotion shift implicit.\n"
        msg += f"5. The USER language ability should be consistent with their age.\n"
        return msg

    def simulate(self, emotion_shift):
        '''
        Simulate a entire conversation between chatbot and user agents
        args:
            emotion_shift: ((emotion1, emotion2), (arousal1, arousal2))
        return:
            dialogue: list of (agent_type, content)
        '''
        # randomly select a which agent to start first
        chatbot_start = True if random.random() > 0.5 else False
        params = self.parameter_generation(emotion_shift)
        params_str = "PARAMETER:\n" + ''.join([f'{k}: {v}\n' for k, v in params.items()]).strip()
        # prompt for message generation
        msg = self.prompt_generation(chatbot_start, params)
        system = "CHATBOT PERSONA:\n" + self.chatbot_persona + "\n"
        system += "USER PERSONA:\n" + self.user_persona + "\n"
        content = f"{params_str}\n\n{msg}"
        # save to tmp to see format, sanity check
        with open(f'{self.output_dir}/{self.format_save_name(emotion_shift)}', 'w') as f:
            f.write("============================================\n")
            f.write("SYSTEM:\n")
            f.write(system)
            f.write("============================================\n")
            f.write("CONTENT:\n")
            f.write(content)
        # send to gpt
        response = self.sent_to_gpt(system, content)
        dialogue = self.process_response(response, emotion_shift)
        if len(dialogue) != 0:
            self.conversation.append(dialogue)
        return dialogue

    def process_response(self, response, emotion_shift):
        '''
        process response from chatgpt, assume response is in the right format
        args:
            response: str, response from chatgpt
            emotion_shift: ((emotion1, emotion2), (arousal1, arousal2))
        return:
            dialogue: list of (agent_type, content)
        '''
        new_dialogue = []
        dialogue_parsed = response.strip().split('\n')
        for dialogue in dialogue_parsed:
            if len(dialogue) == 0:
                continue
            try:
                agent, content = dialogue.split(':')
            except ValueError:
                # exist the current simulation and log it
                with open(self.error_log, 'a') as f:
                    f.write('Value Error while simulating: ' + self.format_save_name(emotion_shift) + '\n')
                    f.write('Response: ' + response + '\n')
                    return []
            if agent == 'CHATBOT':
                new_dialogue.append((1, content))
            else:
                new_dialogue.append((2, content))
        return new_dialogue        

    def start(self):
        '''
        start simulation
        '''
        # end conversation after 100 turn
        # simulate over all possible emotion combination
        for emotion_shift in tqdm.tqdm(self.emotion_combination):
            dialogue = self.simulate(emotion_shift)
            if len(dialogue) == 0:
                # dont save if error, just log it and resume to the next simulation
                continue
            self.append_conversation_str(emotion_shift, dialogue)
            # save to output dir
            with open(f'{self.output_dir}/{self.format_save_name(emotion_shift).strip(".txt")}.json', 'w') as f:
                f.write(json.dumps(dialogue))
    
    def sent_to_gpt(self, system: int, content: str):
        '''
        send message to gpt for response
        args:
            system: str, system persona
            content: str, content of the message
        return:
            
        '''
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": content}])
        # save to output dir and parse response
        response = completion.choices[0].message.content
        return response
