#! /usr/bin/env python
# Time-stamp: <2024-06-03 09:45:08 christophe@pallier.org>

""" Generation the instructions files for each subject for mm-meg-distraction tasks
"""

import sys
import random
import pandas as pd
from pathlib import Path
import argparse

DEST_DIR = Path('instructions')
N_RUNS = 28
N_INSTRUCTIONS_PER_TYPE = 5
INSTRUCTION_FILES = ['list.txt', 'math.txt', 'memory.txt']

def merge_tasks_file_into_df(task_files):
    """ merges text files into a dataframe with the name of each file in the first column. 
    """ 
    tasks = pd.DataFrame(columns=['type', 'instruction'])
    for taskf in task_files:
        with open(taskf) as f:
            for instruction in f.readlines():
                tasks.loc[len(tasks.index)] = [taskf, instruction.strip()]
    return tasks


def pick_instructions(tasks_df, n_instructions_per_type):
    """ tasks_df is a data frame with columns ['type' 'instruction'] 
        Returns a random selection of n_tasks_per_type for each type of tasks (type indicated in the first column. 
    """
    l = []
    for typ in tasks_df['type'].unique():
        ts = tasks_df[tasks_df['type'] == typ].sample(n_instructions_per_type)
        l.append(ts)

    random.shuffle(l)
    tasks = pd.DataFrame(columns=['type', 'instruction'])
    for i in range(n_instructions_per_type):
        for x in l:
            tasks.loc[len(tasks.index)] = x.iloc[i]
         
    return tasks


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate instructions for each run for a given participant')
    parser.add_argument('--subject', type=int, required=True)  
    args = parser.parse_args()

    if args.subject is None:
        parser.print_help()
        sys.exit(1)

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    sub_file = DEST_DIR / f"sub-{args.subject}_instructions.tsv"

    if sub_file.is_file():
        resp = input(f'{sub_file} exists. Do you want to overwrite it? (y/n)')
        if resp == 'n':
            sys.exit(1)
            
    
    tasks = merge_tasks_file_into_df(INSTRUCTION_FILES)

    x = pick_instructions(tasks, N_INSTRUCTIONS_PER_TYPE)

    # insert no task runs
    for i in range(len(x.index)):
        x.loc[args.subject % 2 + i - 0.5] = 'NoTask', 'NA'
    x = x.sort_index().reset_index(drop=True)
    x["run"] = x.index + 1
    
    x[:N_RUNS].to_csv(sub_file, sep='\t')
