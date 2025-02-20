#! /usr/bin/env python

"""
Demo script for the syntcomp experiment

christophe@pallier.org
"""

SOA = 200   # stimulus onset asynchrony (=time of display of character chunks)
BLOCDURATION = SOA * 34
NBLOCKS = 24
INITIALWAIT = 3000
BETWEEN_BLOCS = 8000
TOTAL_DURATION = INITIALWAIT + (BLOCDURATION + BETWEEN_BLOCS) * NBLOCKS



import random, sys, csv, os
from expyriment import design, control, stimuli, io, misc
import expyriment

#%%

exp = design.Experiment(name="First Experiment")

# comment out the following line to get in real mode
control.set_develop_mode(True)

control.initialize(exp)

#%%

control.start(exp)

fixcross = stimuli.FixCross(size=(30, 30), line_width=3, colour=(0, 255, 0))
fixcross.preload()

fixcross2 = stimuli.FixCross(size=(25, 25), line_width=2, colour=(128, 128, 128))
fixcross2.preload()


listname = os.path.join("french_localizer_lists", "loc_sub%03d.csv" % exp.subject)

sequences = [i for i in csv.reader(open(listname))]

block = design.Block(name="block1")

for line in sequences:
    trial = design.Trial()
    stim = []
    for w in line:
        stim = stimuli.TextLine(w.decode('utf-8'), text_font='Inconsolata.ttf',
                                text_size=28)
        trial.add_stimulus(stim)
    
    block.add_trial(trial)
    
exp.add_block(block)

#%%

for block in exp.blocks:
    fixcross.present()
    exp.keyboard.wait_char('t')  # wait_for_MRI_synchro()
    exp.screen.clear()
    exp.screen.update()

    t0 = expyriment.misc.Clock()
    exp.clock.wait(INITIALWAIT)

    for n, trial in enumerate(block.trials):
        for stim in trial.stimuli:
            stim.preload()

        while t0.time < (INITIALWAIT + n * (BLOCDURATION + BETWEEN_BLOCS - 500)):
            exp.clock.wait(10)
            io.Keyboard.process_control_keys()

        exp.clock.wait(400 - fixcross2.present())
        exp.screen.clear()
        exp.screen.update()

        while t0.time < (INITIALWAIT + n * (BLOCDURATION + BETWEEN_BLOCS)):
            exp.clock.wait(10)
            io.Keyboard.process_control_keys()


        exp.data.add(t0.time)
        for stim in trial.stimuli:
            exp.clock.wait(SOA - stim.present())
            
        exp.screen.clear()
        exp.screen.update()

        io.Keyboard.process_control_keys()

exp.clock.wait(8000)
control.end()
