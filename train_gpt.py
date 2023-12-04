from openai import OpenAI
from datasets import load_dataset

training_json = "dd_examples_1000.json"

with open('MY_KEY') as f:
    api_key = f.read().strip()
    client = OpenAI(api_key=api_key)

client.files.create(
  file=open("training_json", "rb"),
  purpose="fine-tune"
)

