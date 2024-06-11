# Experiment LPP distraction 

This version of the LPP paradigm is an auditory version. In this study, participants will either:
- Listen to the Little Prince, as in the listen experiment
- Have to think / run some mental tasks while having the audio of the Little Prince in their ears.

## Before the experiment

- Check triggers by running: ```./ check_partport.py``` in your terminal. You should observe LED of the trigger box turning on/off alternatively.
- Generate a new list of mental tasks for the subject by running: ```python create-instructions-list.py --subject x```
- Switch on MEG room 
- Set MEG to 68° position
- Switch on video projector and run projector script: ```./ ProPixxxsetup.sh```

## Running the experiment

In order to run this experiment, you will simply have to run:

```. run-lpp-meg.sh```

You will get a menu with 9 sections. Each section represents a recording (2 to 4 runs in a single MEG recording). 

NB: If there is a crash during the experiment, you can run manually the desired run with:

```python lpp-meg-distraction.py --subject {subject_number} --run {run_number}```

with run_number from 1 to 28. 
