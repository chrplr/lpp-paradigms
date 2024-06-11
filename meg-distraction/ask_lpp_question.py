import sys
import pandas as pd
from expyriment import design, control, stimuli, io, misc
from pathlib import Path

if len(sys.argv) != 3:
    raise ValueError('The script needs two arguments: the subject number and the last run number')

sub = int(sys.argv[1])
run = int(sys.argv[2])

QUESTION_LPP = Path('questions_lpp.tsv')
df_questions = pd.read_csv(QUESTION_LPP, sep="\t")

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

exp.add_data_variable_names(['lpp_text_question','lpp_answer', 'is_correct'])


question_text = lpp_text_question + "\n\n" + "\n".join(choices)
stimuli.TextScreen("Question", question_text, text_size=32).present()
exp.keyboard.wait()
lpp_answer = io.TextInput("Your answer?").get()

correct_answer = df_questions.iloc[run-1]['answer']
is_correct = 1 if lpp_answer == correct_answer else 0

exp.data.add([lpp_text_question, lpp_answer, is_correct])

control.end()