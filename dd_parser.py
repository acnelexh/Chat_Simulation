lookup = ['No_emotion', 
          'Anger',
          'Disgust',
          'Fear',
          'Happiness',
          'Sadness',
          'Surprise']

from datasets import load_dataset
import random

daily_diaglogue_dataset = load_dataset("daily_dialog")

#dialogue = [ "Hi , Becky , what's up ? ", " Not much , except that my mother-in-law is driving me up the wall . ", " What's the problem ? ", " She loves to nit-pick and criticizes everything that I do . I can never do anything right when she's around . ", " For example ? ", " Well , last week I invited her over to dinner . My husband and I had no problem with the food , but if you listened to her , then it would seem like I fed her old meat and rotten vegetables . There's just nothing can please her . ", " No , I can't see that happening . I know you're a good cook and nothing like that would ever happen . ", " It's not just that . She also criticizes how we raise the kids . ", " My mother-in-law used to do the same thing to us . If it wasn't disciplining them enough , then we were disciplining them too much . She also complained about the food we fed them , the schools we sent them too , and everything else under the sun . ", " You said she used to ? How did you stop her ? ", " We basically sat her down and told her how we felt about her constant criticizing , and how we welcomed her advice but hoped she'd let us do our things . She understood , and now everything is a lot more peaceful . ", " That sounds like a good idea . I'll have to try that . " ]
#label = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 ]

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


with open('dd_examples_all.txt', 'w') as f:
    #f.write("Here are all the dialogues from the Daily Dialogue dataset.\n\n")
    # Iterate through all dialogues in the training dataset
    for idx in range(len(daily_diaglogue_dataset['train'])):
        dialogue = daily_diaglogue_dataset['train'][idx]['dialog']
        label = daily_diaglogue_dataset['train'][idx]['emotion']
        f.write(parse_dialogue(dialogue, label) + "\n\n")

# NUM_EXAMPLES = 5
# # with open('dd_examples_all.txt', 'w') as f:
# #     f.write("Here are some simulated examples from the Daily Dialogue dataset.\n")
# # select a NUM_EXAMPLES that contain at least 3 of the 7 emotions
# dd_examples = []
# while len(dd_examples) < NUM_EXAMPLES:
#     idx = random.randint(0, len(daily_diaglogue_dataset['train']) - 1)
#     dialogue = daily_diaglogue_dataset['train'][idx]['dialog']
#     label = daily_diaglogue_dataset['train'][idx]['emotion']
#     if len(set(label)) >= 2:
#         dd_examples.append(idx)

# for idx in dd_examples:
#     dialogue = daily_diaglogue_dataset['train'][idx]['dialog']
#     label = daily_diaglogue_dataset['train'][idx]['emotion']
#     with open('dd_examples_all.txt', 'a') as f:
#         f.write(parse_dialogue(dialogue, label))
#         f.write("\n\n")

