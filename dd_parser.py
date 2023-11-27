lookup = ['No emotion', 
          'Anger',
          'Disgust',
          'Fear',
          'Happiness',
          'Sadness',
          'Surprise']

dialogue = [ "Hi , Becky , what's up ? ", " Not much , except that my mother-in-law is driving me up the wall . ", " What's the problem ? ", " She loves to nit-pick and criticizes everything that I do . I can never do anything right when she's around . ", " For example ? ", " Well , last week I invited her over to dinner . My husband and I had no problem with the food , but if you listened to her , then it would seem like I fed her old meat and rotten vegetables . There's just nothing can please her . ", " No , I can't see that happening . I know you're a good cook and nothing like that would ever happen . ", " It's not just that . She also criticizes how we raise the kids . ", " My mother-in-law used to do the same thing to us . If it wasn't disciplining them enough , then we were disciplining them too much . She also complained about the food we fed them , the schools we sent them too , and everything else under the sun . ", " You said she used to ? How did you stop her ? ", " We basically sat her down and told her how we felt about her constant criticizing , and how we welcomed her advice but hoped she'd let us do our things . She understood , and now everything is a lot more peaceful . ", " That sounds like a good idea . I'll have to try that . " ]
label = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 ]

# parse the conversationt to
# A [EMOTION]: DIALOGUE
# B [EMOTION]: DIALOGUE
# ...

def parse_dialogue(dialogue, label):
    result = "Here is a generated examples:\n"
    for i in range(len(dialogue)):
        if i % 2 == 0:
            result += "A "
        else:
            result += "B "
        result += "[" + lookup[label[i]] + "]: " + dialogue[i].strip() + "\n"
    return result.strip()

with open('dd_examples.txt', 'w') as f:
    f.write(parse_dialogue(dialogue, label))