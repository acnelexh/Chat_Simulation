from pathlib import Path
import pandas as pd

def parse_dialog(dialog: str) -> (list, list):
    '''
    dialog: string of dialog
    return: list of dialog, list of agents
    '''
    agent_lookup = {"Chatbot": 0, "User": 1}
    dialog = dialog.split('\n')
    dialog = [x for x in dialog if x != '']
    result_agents = []
    result_sentences = []
    for d in dialog:
        agent, sentence = d.split(':')
        result_agents.append(agent_lookup[agent])
        result_sentences.append(sentence.strip())
    return result_sentences, result_agents

def build_dialog_lookup(data_dir: list) -> dict:
    '''
    data_dir: list of Path that contain simulated result
    return: dict of {dialogue: {index, user_persona, dialog_parsed (list), character_list ([bot, user...}], gpt annotation shift, gpt dialogue emotion annotatin}}
    '''
    lookup = dict()
    for d in data_dir:
        # persona file
        with open(d / 'user_persona.txt') as f:
            persona = f.read()
        # read output csv
        df = pd.read_csv(d / 'output.csv')
        dialogues = df['dialog'].values
        emotion_shift = df['emotion'].values
        emotion_by_sentence = df['emotion_by_sentence'].values
        # parse dialog
        dialogs, agents = parse_dialog(dialogues[0])
        # zip them
        train_gpt = False
        if int(d.stem) >= 33: # its trained model
            train_gpt = True
        for dialog, emotion, emotion_by_sentence in zip(dialogues, emotion_shift, emotion_by_sentence):
            lookup[dialog.strip()] = {
                'persona': persona,
                'emotion_gpt': emotion,
                'emotion_by_sentence_gpt': emotion_by_sentence,
                'train_gpt': train_gpt,
                'dialog_parsed': dialogs,
                'agents': agents
            }
    return lookup

def merge_emo(df: pd.DataFrame, lookup_correction: dict, column_name: str):
    '''
    lookup_correction: dict of {wrong: correct}
    column_name: column name to correct
    '''
    for k, v in lookup_correction.items():
        df.loc[df[column_name] == k, column_name] = v
    

def cross_validate(df: pd.DataFrame):
    '''
    Cross validate df, make sure same dialogue has same annoatation
    '''
    # dialog, emotion1, emotion2
    new_df = pd.DataFrame(columns=['dialog', 'emotion1', 'emotion2'])
    count_consistent = 0
    consistent_dialoges = []
    for dialog, group in df.groupby('Dialogue'):
        if len(group) >= 3:
                # check majority of emotion
                emotion1_count = group['User Emotion 1'].value_counts().max()
                emotion2_count = group['User Emotion 2 '].value_counts().max()
                if emotion1_count / len(group) >= 0.5 and emotion2_count / len(group) >= 0.5:
                    count_consistent += 1
                    consistent_dialoges.append(dialog)
                    new_entry = dialog, group['User Emotion 1'].value_counts().idxmax(), group['User Emotion 2 '].value_counts().idxmax()
                    new_df = new_df._append(pd.Series(new_entry, index=new_df.columns), ignore_index=True)
        if len(group) < 3:
            # check if all emotion is same
            emotion1_count = group['User Emotion 1'].value_counts().max()
            emotion2_count = group['User Emotion 2 '].value_counts().max()
            if emotion1_count == len(group) and emotion2_count == len(group):
                count_consistent += 1
                consistent_dialoges.append(dialog)
                new_entry = dialog, group['User Emotion 1'].value_counts().idxmax(), group['User Emotion 2 '].value_counts().idxmax()
                new_df = new_df._append(pd.Series(new_entry, index=new_df.columns), ignore_index=True)
    print(f'Consistent: {count_consistent} / {len(df["Dialogue"].unique())}')
    return new_df

def fix_typo(df: pd.DataFrame):
    '''
    Hardcoded fix typo
    '''
    combined_df = df.dropna(subset=['Dialogue'])
    correction_emo1 = {"Sad": "Sadness", "Suprised": "Surprised", "Disgust": "Disgusted", "Supirsed": "Surprised", "Scared": "Fear", "Happu": "Happy", "Disguested": "Disgusted", "Surprise": "Surprised"}
    merge_emo(combined_df, correction_emo1, 'User Emotion 1')
    correction_emo2 = {"Sad": "Sadness", "Suprised": "Surprised", "Disgust": "Disgusted", "Supirsed": "Surprised", "Scared": "Fear", "Happu": "Happy", "Surprise": "Surprised"}
    merge_emo(combined_df, correction_emo2, 'User Emotion 2 ')
    combined_df = combined_df.dropna(subset=['User Emotion 1', 'User Emotion 2 '])
    return combined_df

def read_human_annotation(data_dir: Path, lookup_tables: dict) -> pd.DataFrame:
    '''
    Read and organize human annotation from annotators
    '''
    # glob all csv columns: Persona 1 - 20,Dialogue,User Emotion 1,User Emotion 2 
    csv_files = list(data_dir.glob('*.csv'))
    combined_df = pd.DataFrame()
    for csv in csv_files:
        df = pd.read_csv(csv)
        # drop column that begin with Persona
        df = df.loc[:, ~df.columns.str.startswith('Persona')]
        combined_df = combined_df._append(df)
    # drop nan in Dialogue
    combined_df = combined_df.dropna(subset=['Dialogue'])
    # fix typo
    combined_df = fix_typo(combined_df)
    # cross validate and prune dialogue that has inconsistent emotion between annotators
    combined_df = cross_validate(combined_df)
    
    # merge with lookup table
    combined_df['dialog'] = combined_df['dialog'].apply(lambda x: x.strip())
    combined_df['emotion1'] = combined_df['emotion1'].apply(lambda x: x.strip().lower())
    combined_df['emotion2'] = combined_df['emotion2'].apply(lambda x: x.strip().lower())
    
    print(combined_df)


def main():
    simulated_dir = [20, 21, 22, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38]
    simulated_dir = [Path(f'output/{x}') for x in simulated_dir]
    lookup_tables = build_dialog_lookup(simulated_dir)
    read_human_annotation(Path('./make_dataset/human_annotation'), lookup_tables)

if __name__ == '__main__':
    main()