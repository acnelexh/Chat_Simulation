from datasets import load_dataset
import random
import json

lookup = ['No_emotion', 
          'Anger',
          'Disgust',
          'Fear',
          'Happiness',
          'Sadness',
          'Surprise']

def parse_dialogue(dialogue, label):
    # parse the conversationt to
    # A [EMOTION]: DIALOGUE
    # B [EMOTION]: DIALOGUE
    # ...
    result = ""
    for i in range(len(dialogue)):
        if i % 2 == 0:
            result += "[A]"
        else:
            result += "[B]"
        result += "[" + lookup[label[i]] + "]: " + dialogue[i].strip() + "\n"
    return result.strip()

def write_all_examples(daily_diaglogue_dataset):
    with open('dd_examples_all.txt', 'w') as f:
        #f.write("Here are all the dialogues from the Daily Dialogue dataset.\n\n")
        # Iterate through all dialogues in the training dataset
        for idx in range(len(daily_diaglogue_dataset['train'])):
            dialogue = daily_diaglogue_dataset['train'][idx]['dialog']
            label = daily_diaglogue_dataset['train'][idx]['emotion']
            f.write(parse_dialogue(dialogue, label) + "\n\n")

def write_n_samples(daily_diaglogue_dataset, NUM_EXAMPLES = 5):
    with open('dd_examples_all.txt', 'w') as f:
        f.write("Here are some simulated examples from the Daily Dialogue dataset.\n")
    # select a NUM_EXAMPLES that contain at least 3 of the 7 emotions
    dd_examples = []
    while len(dd_examples) < NUM_EXAMPLES:
        idx = random.randint(0, len(daily_diaglogue_dataset['train']) - 1)
        dialogue = daily_diaglogue_dataset['train'][idx]['dialog']
        label = daily_diaglogue_dataset['train'][idx]['emotion']
        if len(set(label)) >= 2:
            dd_examples.append(idx)

    for idx in dd_examples:
        dialogue = daily_diaglogue_dataset['train'][idx]['dialog']
        label = daily_diaglogue_dataset['train'][idx]['emotion']
        with open('dd_examples_all.txt', 'a') as f:
            f.write(parse_dialogue(dialogue, label))
            f.write("\n\n")

def parse_examples_into_json(num_samples = 1000):
    output_file = f'dd_examples_{num_samples}.json'
    with open('dd_examples_all.txt', 'r') as f:
        # readall
        examples = f.read().split("\n\n")
        for i in range(num_samples):
            dialogue = examples[i].split("\n")
            # put them in json format
            # {"messages": [{"role": "system", "content": "Generate a following dialogue based on the previous one."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]}
            with open(output_file, 'a') as f:
                for j in range(1, len(dialogue)):
                    json_dict = {}
                    json_dict["messages"] = []
                    json_dict["messages"].append({"role": "system", "content": "Generate a following dialogue based on the previous one."})
                    json_dict["messages"].append({"role": "user", "content": dialogue[j-1]})
                    json_dict["messages"].append({"role": "assistant", "content": dialogue[j]})
                    json.dump(json_dict, f)
                    f.write("\n")


def main():
    #daily_diaglogue_dataset = load_dataset("daily_dialog")
    #write_all_examples(daily_diaglogue_dataset)
    parse_examples_into_json(1000)

if __name__ == "__main__":
    main()


