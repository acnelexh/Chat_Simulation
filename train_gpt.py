from openai import OpenAI
import numpy as np
import json
from collections import defaultdict

with open('MY_KEY') as f:
    api_key = f.read().strip()
    client = OpenAI(api_key=api_key)

def upload_file(filename):
    msg = client.files.create(
    file=open("dd_examples_1000.json", "rb"),
    purpose="fine-tune"
    )
    return msg

def create_job(training_file_name, model):
    msg = client.fine_tuning.jobs.create(
        training_file=training_file_name, 
        model=model
    )
    return msg

def check_status():
    # List 10 fine-tuning jobs
    msg = client.fine_tuning.jobs.list(limit=10)
    print(msg)

    job_id = msg.data[0].id
    # Retrieve the state of a fine-tune
    msg = client.fine_tuning.jobs.retrieve(job_id)
    print(msg)

def get_model():
    msg = client.fine_tuning.jobs.list(limit=10)
    job_id = msg.data[0].id
    msg = client.fine_tuning.jobs.retrieve(job_id)
    model = msg.fine_tuned_model
    if model == None:
        # training not finish
        print("Training not finish")
    else:
        print("Training finish")
    return model

if __name__ == "__main__":
    #msg = upload_file("dd_examples_1000.json")
    #print(msg)
    #msg = create_job(msg.id, "gpt-3.5-turbo")
    #print(msg)
    #check_status()
    model_name = get_model()
    
