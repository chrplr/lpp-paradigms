# Experiment LPP distraction 

This version of the LPP paradigm is an auditory version. In this study, participants will either:
- Listen to the Little Prince, as in the listen experiment
- Have to think / run some mental tasks while having the audio of the Little Prince in their ears.

## Before the experiment

- Check triggers by running: ```python check_parport.py``` in your terminal. You should observe LED of the trigger box turning on/off alternatively.
- Generate a new list of mental tasks for the subject by running: ```python create-instructions-list.py --subject x```
- Set MEG to 68° position
- Switch on video projector and run the projector script: ```./ ProPixxxsetup.sh```

## Running the experiment

In order to run this experiment, you will simply have to run:

```. run-lpp-meg.sh```

You will get a menu with 9 sections. Each section represents one recording (i.e. 2 to 4 runs in a single MEG recording). 

NB: If there is a crash during the experiment, you can run manually the desired run with:

```python lpp-meg-distraction.py --subject {subject_number} --run {run_number}```

with run_number from 1 to 28. 

## TODO:

Problems:

- trigger not saved: harder to crop and to realign

### Prio 1

- Check with Theo to make the triggers STI working in MEG
- For the current acq: make a simple algo for automatically crop (pauses longer than X sec)
- Have a full pipeline to:
    - put into BIDS format when new data comes in
    - check the trigger timings / the total length and assert it's ok
    - (bonus) run some simple wordfreq decoding / word emb

### Prio 2

- Add again the syntactic info / POS etc..
- Remove empty word events
