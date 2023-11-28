import json
import argparse
import pandas as pd
from pathlib import Path

'''
Parse json into csv file
command line: python make_df.py --dir <dir>
e.g. python make_df.py --dir output/1
'''
def make_df(dir):
    '''
    turn all json files in dir into a dataframe
    '''
    df = pd.DataFrame(columns=["dialog", "emotion", "emotion_by_sentence"])
    lookup_table = {1: "Chatbot", 2: "User"}
    all_json = [x for x in dir.glob("*.json")]
    for j_file in all_json:
        with open(j_file, "r") as f:
            emotion1, emotion2 = j_file.stem.split("_")
            data = json.load(f) # list of (int, str) or (int, str, str)
            formatted_data = ""
            emotion_label_by_sentence = []
            for d in data:
                formatted_data += f"{lookup_table[d[0]]}: {d[1]}\n"
                if d[0] == 1:
                    # chatbot no emotion
                    emotion_label_by_sentence.append("Neutral")
                else:
                    emotion_label_by_sentence.append(d[2])
            df = df._append({
                "dialog": formatted_data,
                "emotion": (emotion1, emotion2),
                "emotion_by_sentence": emotion_label_by_sentence}, ignore_index=True)
    return df

def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default=None, help="directory that holds all the json files")
    args = parser.parse_args()
    # init engine
    df = make_df(Path(args.dir))
    df.to_csv(f"{args.dir}/output.csv", index=False)

main()