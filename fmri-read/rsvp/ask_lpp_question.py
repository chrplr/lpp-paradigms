import sys
import pandas as pd
from expyriment import design, control, stimuli, io, misc
from pathlib import Path
import csv
import os

if len(sys.argv) != 3:
    raise ValueError('The script needs two arguments: the subject number and the last run number')

sub = int(sys.argv[1])
run = int(sys.argv[2])

SHIFT_CENTER = 0 #-350
QUESTION_LPP = Path('questions_lpp.tsv')
df_questions = pd.read_csv(QUESTION_LPP, sep="\t")

def save_response(sub, lpp_text_question, lpp_answer, is_correct):
    csv_filename = f"data/lpp_answer_sub-{sub}.csv"
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(["Subject_ID", "LPP_question", "LPP_answer", "Correct"])
        
        writer.writerow([sub, lpp_text_question, lpp_answer, is_correct])
    

lpp_text_question = df_questions.iloc[run-1]['question']
choices = [
    df_questions.iloc[run-1]['choice_a'],
    df_questions.iloc[run-1]['choice_b'],
    df_questions.iloc[run-1]['choice_c'],
    df_questions.iloc[run-1]['choice_d'],
    df_questions.iloc[run-1]['choice_e']
]

exp = design.Experiment(name="Le_Petit_Prince_Questions")
control.defaults.initialize_delay = 0

control.initialize(exp)

control.start(exp, subject_id=sub, skip_ready_screen=True)

question_text = lpp_text_question + "\n\n" + "\n".join(choices)
stimuli.TextScreen("Question", question_text, text_size=60, position=(SHIFT_CENTER, 0)).present()
exp.keyboard.wait()
lpp_answer = io.TextInput("Your answer?").get()

correct_answer = df_questions.iloc[run-1]['answer']
is_correct = 1 if lpp_answer == correct_answer else 0

save_response(sub, lpp_text_question, lpp_answer, is_correct)

control.end()
