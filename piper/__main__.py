import time
import os
import argparse
import threading
import logging
from pathlib import Path

from pypyr import pipelinerunner
from pypyr import context
from pypyr.pypeloaders import fileloader
from pypyr.stepsrunner import StepsRunner
from pypyr.dsl import Step

from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.progress import Progress
from rich import inspect
from rich.logging import RichHandler
from rich import print

from tinydb import TinyDB, Query

import ast

# TODO: allow the user to specify / select a DB file to 
# use for a given pipeline
db = TinyDB('./db.json')

host = {
    'ip': '',
    'hostname': '',
    'steps': {},
    'services': {},
    'last_seen': ''
}

FORMAT = "%(message)s"
logging.basicConfig(
    level=25, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
console = Console()

def pipeline_thread_function(shared_context):
    pipelinerunner.prepare_and_run(
        pipeline_name='pipelines/test-pipe',
        working_dir=os.getcwd(),
        context=shared_context,
        parse_input=False
        )   

# Shared context object used by the main thread here (for reads)
# and by the pipeline itself in a separate thread (for reads and writes)
# no locking here because idgaf.
shared_context = context.Context({
    'finished': False,
    'progress': 0, 
    'arbkey':'pipe', 
    'anotherkey':'song',
    'logger': console.log,
    'db': db
}) 
#pipeline_thread = threading.Thread(target=pipeline_thread_function, args=(shared_context,))
#pipeline_thread.start()
pipeline_definition = fileloader.get_pipeline_definition('pipelines/test-pipe', Path(os.getcwd()))
stepsrunner = StepsRunner(pipeline_definition, shared_context) 
steps = stepsrunner.get_pipeline_steps('steps')
step_count = 0

with console.status('[bold green]Hacking stuff...', spinner='pong'):
    for step in steps:
        if step.get('comment', None):
            console.log(step.get('comment'))

        step_instance = Step(step, stepsrunner)
        step_instance.run_step(shared_context)
        
        if shared_context.get('cmdOut', None):
            cmd_out = shared_context.get('cmdOut')
            shared_context['cmdOut'] = ''
            console.log(cmd_out['stdout'])

            #if step.get('comment', None) and step['comment'] == 'rustscan':
            #    stdout_split = cmd_out['stdout'].split('\n')
            #    
            #    for h in stdout_split:
            #        db.table(step['comment']).insert({
            #            h.split()[0]: {
            #                'ports': ast.literal_eval(h.split()[2])
            #            }
            #        })

        console.log(f'{step["name"]} compelete')
        step_count += 1

console.print('')
console.log(':smiley: done')
#pipeline_thread.join()