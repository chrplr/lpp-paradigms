from expyriment import design, control, stimuli, io, misc
import sys
import os
import random
import pandas as pd
from pathlib import Path
import time
import argparse

#import subprocess
#subprocess.call("ProPixxsetup.sh")

SHIFT_CENTER = -150
INSTRUCTIONS_DIR = Path('instructions')
QUESTION_LPP = Path('questions_lpp.tsv')

## Trigger on parallel port (This worked on the 5 th of June 2024)
#pp = io.ParallelPort('/dev/parport1')

def send_trigger():
    pp.set_data(255)
    # wait for 50ms
    end_time = time.perf_counter() + 0.05   
    while time.perf_counter() < end_time:
        pass
    pp.set_data(0)

def clear_screen():
    exp.screen.clear()
    exp.screen.update()
    
##### main 

parser = argparse.ArgumentParser(description='Le_Petit_Prince_MEG_Distraction stimulation script')

parser.add_argument('--subject', type=int, required=True)  
parser.add_argument('--run', type=int, required=True)  
args = parser.parse_args()
sub = args.subject
run = args.run


df = pd.read_csv(INSTRUCTIONS_DIR / f'sub-{sub}_instructions.tsv', sep="\t")
current_run = df[df.run == run]

audio_file = f'small_chapters/ch{run}.wav'

##
exp = design.Experiment(name="Le_Petit_Prince_MEG_Distraction")
control.defaults.initialize_delay = 0
control.defaults.audio_system_buffer_size = 2048 
control.audiosystem_channels = 2
control.audiosystem_sample_rate = 44100

#control.set_develop_mode(True)

## Initialization 

control.initialize(exp)

stim = stimuli.Audio(audio_file)
stim.preload()

fixcrossGrey = stimuli.FixCross(size=(45, 45), line_width=3,
                                colour=(192, 192, 192), position=(SHIFT_CENTER, 0))
fixcrossGrey.preload()


control.start(exp, subject_id=sub, skip_ready_screen=True)

#pp.set_data(0)

exp.add_data_variable_names(['instruction','audio_listening'])

clear_screen()

if current_run.type.values[0] != 'NoTask':
    stimuli.TextBox(current_run.instruction.values[0], 
                    (1600, 400),
                     text_size=22, 
                     text_colour=(255, 255, 255)).present()
    key, _ = exp.keyboard.wait([misc.constants.K_SPACE])

stimuli.TextLine("Press Spacebar when ready...", text_size=50, text_colour=(245, 167, 66), position=(SHIFT_CENTER, 0)).present()
exp.keyboard.read_out_buffered_keys()
exp.keyboard.wait(misc.constants.K_SPACE)

clear_screen()

# Core
#send_trigger()
exp.clock.wait(2000) 
fixcrossGrey.present(clear=True, update=True)
exp.clock.wait(5000)
#send_trigger()
stim.present()
control.wait_end_audiosystem(process_control_events=True)
#send_trigger()

io.Keyboard.process_control_keys()

## Ask question about audio listening
stimuli.TextLine('Sur une échelle entre 0 (pas du tout) et 4 (parfaitement), quelle attention avez-vous porté à l\'audio ?', text_size=40, text_colour=(255, 255, 255)).present()
exp.keyboard.wait()
audio_listening = io.TextInput("Score ?").get()

exp.data.add([current_run.instruction.values[0], audio_listening])

control.end()