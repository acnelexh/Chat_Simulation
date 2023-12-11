from pathlib import Path
import pandas as pd

def build_dialog_lookup(data_dir: list) -> dict:
    '''
    data_dir: list of Path that contain simulated result
    return: dict of {dialogue: persona}
    '''
    persona_lookup = dict()
    emotion_shift_lookup = dict()
    emotion_by_sentence_lookup = dict()
    for d in data_dir:
        # persona file
        with open(d / 'user_persona.txt') as f:
            persona = f.read()
            persona = persona.split('\n')
        # read output csv
        df = pd.read_csv(d / 'output.csv')
        dialogues = df['dialog'].values
        emotion_shift = df['emotion'].values
        emotion_by_sentence = df['emotion_by_sentence'].values
        # zip them
        for dialog, emotion, emotion_by_sentence in zip(dialogues, emotion_shift, emotion_by_sentence):
            persona_lookup[dialog] = persona
            emotion_shift_lookup[dialog] = emotion
            emotion_by_sentence_lookup[dialog] = emotion_by_sentence
    return {'persona': persona_lookup, 'emotion_shift': emotion_shift_lookup, 'emotion_by_sentence': emotion_by_sentence_lookup}

def read_human_annotation(data_dir: Path) -> pd.DataFrame:
    # glob all csv
    csv_files = list(data_dir.glob('*.csv'))
    for f in csv_files:
        df = pd.read_csv(f)
        print(df.columns)

def main():
    read_human_annotation(Path('./make_dataset/human_annotation'))
    lookup_tables = build_dialog_lookup([Path('output/22')])
    
if __name__ == '__main__':
    main()