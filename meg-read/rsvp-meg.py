#! /usr/bin/env python
# Time-stamp: <2024-04-23 11:45:25 chistophe@pallier.org>

""" Display text, word by word, at the center of the screen.

    Usage: 

     python rsvp-mri.py --chapter 4

    where 4 is the number of the chapter wanted
"""

import argparse
from queue import PriorityQueue
import pandas as pd
import expyriment
from expyriment import stimuli, io, control
from expyriment.misc import Clock

#expyriment.control.set_develop_mode(on=True, intensive_logging=False, skip_wait_methods=True)
#expyriment.control.defaults.window_mode = True

# VERSION CHOICE:
# Version 1: 350 ms between each word; 300 ms of word + 50 ms of black screen
# Version 2: 250 ms / 50 ms + 500 ms at the end of each sentence
VERSION = 2

# Triggers
# port_address_output = "/dev/parport1"
# port1 = io.ParallelPort(port_address_output)

# Const
TEXT_FONT = "Inconsolata.ttf"
TEXT_SIZE = 40
# TEXT_COLOR = (255, 255, 255)  # white
TEXT_COLOR = (230, 230, 230)  # white but not too white
# BACKGROUND_COLOR = (64, 64, 64)  # grey
BACKGROUND_COLOR = (30, 30, 30)  # black
WINDOW_SIZE = 1024, 768
CHAPTER = 1
FIXED_WORD_DURATION = 250  # Overriding tsv file
FIXED_BS_DURATION = 50  # Overriding tsv file
SPEED = 0.9
END_OF_SENTENCE_BLANK = True

######## command-line arguments
parser = argparse.ArgumentParser()

# parser.add_argument('csv_files',
#                     nargs='+',
#                     action="append",
#                     default=[])
parser.add_argument(
    "--text-font", type=str, default=TEXT_FONT, help="set the font for text stimuli"
)
parser.add_argument(
    "--text-size",
    type=int,
    default=TEXT_SIZE,
    help="set the vertical size of text stimuli",
)
parser.add_argument(
    "--text-color",
    nargs="+",
    type=int,
    default=TEXT_COLOR,
    help="set the font for text stimuli",
)
parser.add_argument(
    "--background-color",
    nargs="+",
    type=int,
    default=BACKGROUND_COLOR,
    help="set the background color",
)
parser.add_argument(
    "--window-size",
    nargs="+",
    type=int,
    default=WINDOW_SIZE,
    help="in window mode, sets the window size",
)
parser.add_argument(
    "--chapter",
    nargs="+",
    type=int,
    default=CHAPTER,
    help="choose which chapter to play",
)
args = parser.parse_args()
TEXT_SIZE = args.text_size
TEXT_COLOR = tuple(args.text_color)
TEXT_FONT = args.text_font
BACKGROUND_COLOR = tuple(args.background_color)
WINDOW_SIZE = tuple(args.window_size)
CHAPTER = args.chapter[0]

if VERSION == 1:
    csv_file = f"./v1/run{CHAPTER}_v1_word_0.3_end_sentence_0.2.tsv"
else:
    csv_file = f"./v2/run{CHAPTER}_v2_0.25_0.5.tsv"
    

stimlist = pd.read_csv(csv_file, sep="\t", quoting=True)

def clear_screen():
    exp.screen.clear()
    exp.screen.update()
    
###############################
# expyriment.control.defaults.window_mode = True
# expyriment.control.defaults.window_size = WINDOW_SIZE
# expyriment.design.defaults.experiment_background_colour = BACKGROUND_COLOR

exp = expyriment.design.Experiment(
    name="RSVP",
    background_colour=BACKGROUND_COLOR,
    foreground_colour=TEXT_COLOR,
    text_size=TEXT_SIZE,
    text_font=TEXT_FONT)
control.defaults.initialize_delay = 0
expyriment.control.initialize(exp)
exp._screen_colour = BACKGROUND_COLOR
kb = expyriment.io.Keyboard()


####################################################
# Prepare the queue of events
bs = stimuli.BlankScreen(colour=BACKGROUND_COLOR)
photodiode = stimuli.Rectangle((90, 90), position=(900, -500))

fixcrossGreen = stimuli.FixCross(size=(45, 45), line_width=5,
                                 colour=(0, 255, 0))
fixcrossGreen.preload()

events = PriorityQueue()
map_text_surface = dict()

max_onset = 0

for row in stimlist.itertuples():
    text = row.word

    onset = row.onset
    duration = row.duration
    max_onset = max(onset, max_onset)

    if text in map_text_surface.keys():
        stim = map_text_surface[text]
    else:
        stim = stimuli.TextLine(
            text,
            text_font=TEXT_FONT,
            text_size=TEXT_SIZE,
            text_colour=TEXT_COLOR,
            background_colour=BACKGROUND_COLOR,
        )
        map_text_surface[text] = stim

    events.put((onset * 1000 * SPEED, text, stim))
    events.put(((onset + duration) * 1000 * SPEED, "", bs))

# Adding a 3s blackscreen at the end 

end_bs = ((max_onset*1000)+10000)
events.put((end_bs * SPEED, "", bs))

#############################################################
# let's go

def wait_for_start():
    fixcrossGreen.present(clear=True, update=True)
    exp.keyboard.wait()

expyriment.control.start(subject_id=0, skip_ready_screen=True)
io.Keyboard.process_control_keys()

wait_for_start()
clear_screen()
exp.clock.wait(6000)
# init triggers
# port1.send(data=0)

a = Clock()

# Initialize

# port1.send(data=CHAPTER)

while not events.empty():
    onset, text, stim = events.get()
    value_trigger = len(text)
    while a.time < (onset - 10):
        a.wait(1)
        k = kb.check()
        if k is not None:
           exp.data.add([a.time, "keypressed,{}".format(k)])
    # port1.send(data=value_trigger)
    
    if value_trigger != 0:
        stim.present(clear=True)
        photodiode.present(clear=False)
        exp.data.add([a.time, stim.text])
    else:
        stim.present(clear=True)

stimuli.TextLine("Run terminé !", text_size=50, text_colour=(245, 167, 66)).present()
exp.data.add([a.time, "end"])
exp.keyboard.wait()
