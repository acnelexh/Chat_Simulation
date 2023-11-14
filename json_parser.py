# parser to handle the output from openai
import json


class Parser:
    def __init__(self):
        pass
    
    def read_json(self, file):
        with open(file) as f:
            data = json.load(f)
        return data
    
    def parse(self, data):
        key = []