from expyriment import design, control, stimuli, io, misc
import sys
import os
import random
import pandas as pd
from pathlib import Path

INSTRUCTIONS_DIR = Path('instructions')
QUESTION_LPP = Path('questions_lpp.tsv')

## Triggers
pp = io.ParallelPort('/dev/parport0')

def send_trigger():
    pp.set_data(255)
    # wait for 50ms
    end_time = time.perf_counter() + 0.05   
    while time.perf_counter() < end_time:
        pass
    pp.set_data(0)

if len(sys.argv) != 3:
    raise ValueError('The script needs two arguments: the subject number and the run number')

sub = int(sys.argv[1])
run = int(sys.argv[2])

AUDIO = f'small_chapters/ch{run}.wav'

df = pd.read_csv(INSTRUCTIONS_DIR / f'sub-{sub}_instructions.tsv', sep="\t")
df_questions = pd.read_csv(QUESTION_LPP, sep="\t")

current_run = df[df.run == run]

##
exp = design.Experiment(name="Le_Petit_Prince")
control.defaults.initialize_delay = 0

#control.set_develop_mode(True)

## Initialization 

control.initialize(exp)

stim = stimuli.Audio(AUDIO)
stim.preload()

fixcrossGreen = stimuli.FixCross(size=(45, 45), line_width=5,
                                 colour=(0, 255, 0))
fixcrossGreen.preload()
fixcrossGrey = stimuli.FixCross(size=(45, 45), line_width=3,
                                colour=(192, 192, 192))
fixcrossGrey.preload()

def clear_screen():
    exp.screen.clear()
    exp.screen.update()

control.start(exp, subject_id=sub, skip_ready_screen=True)

exp.add_data_variable_names(['instruction','audio_listening', 'lpp_question', 'is_correct'])

clear_screen()

if current_run.type.values[0] != 'NoTask':
    stimuli.TextBox(current_run.instruction.values[0], 
                    (1024, 100),
                     text_size=32, 
                     text_colour=(255, 255, 255)).present()
    key, _ = exp.keyboard.wait([misc.constants.K_SPACE])

stimuli.TextLine("Press Spacebar when ready...", text_size=50, text_colour=(245, 167, 66)).present()
exp.keyboard.read_out_buffered_keys()
exp.keyboard.wait(misc.constants.K_SPACE)

clear_screen()

# Core
send_trigger()
exp.clock.wait(2000) 
fixcrossGrey.present(clear=True, update=True)
exp.clock.wait(5000)
send_trigger()
stim.present()
control.wait_end_audiosystem(process_control_events=True)
send_trigger()

io.Keyboard.process_control_keys()

## Ask questions
lpp_text_question = df_questions.iloc[run]['question']
choices = [
    df_questions.iloc[run]['choice_a'],
    df_questions.iloc[run]['choice_b'],
    df_questions.iloc[run]['choice_c'],
    df_questions.iloc[run]['choice_d']]

stimuli.TextScreen("Question", lpp_text_question + "\n\n" + "\n".join(choices), text_size=32).present()
exp.keyboard.wait()
lpp_answer = io.TextInput("Your answer?").get()

stimuli.TextLine('Sur une échelle entre 0 (pas du tout) et 4 (parfaitement), quelle attention avez-vous porté à l\'audio ?', text_size=32, text_colour=(255, 255, 255)).present()
exp.keyboard.wait()
audio_listening = io.TextInput("Your note?").get()
# Check if participant's response is correct
correct_answer = df_questions.iloc[run]['answer']
is_correct = 1 if lpp_answer == correct_answer else 0

exp.data.add([current_run.instruction.values[0], audio_listening, lpp_answer, is_correct])

control.end()