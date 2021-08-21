import time
import os
import argparse
import threading
from pathlib import Path

from pypyr import pipelinerunner
from pypyr import context
from pypyr.pypeloaders import fileloader

from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.progress import Progress
from rich import inspect

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
    'anotherkey':'song'
}) 
pipeline_thread = threading.Thread(target=pipeline_thread_function, args=(shared_context,))
pipeline_thread.start()

# display progress
pipeline_definition = fileloader.get_pipeline_definition('pipelines/test-pipe', Path(os.getcwd()))
total_steps = len(pipeline_definition['steps'])
completed_tasks = shared_context['progress']
with Progress() as progress:
    t1 = progress.add_task("[cyan]Running...", total=total_steps)
    while not progress.finished: #and completed_tasks < len(pipeline_definition['steps']):
        if shared_context['progress'] > completed_tasks:
            progress.update(t1, advance=1)
        # update count of completed tasks
        completed_tasks = shared_context['progress']


print('done')
#pipeline_thread.join()

#table = Table(show_header=True, header_style="bold magenta")
#table.add_column("Date", style="dim", width=12)
#table.add_column("Title")
#table.add_column("Production Budget", justify="right")
#table.add_column("Box Office", justify="right")
#table.add_row(
#    "Dev 20, 2019", "Star Wars", "$275,000,000", "375,000,000"
#)
#table.add_row(
#    "May 25, 2018",
#    "[red]Solo[/red]: A Star Wars Story",
#    "$275,000,000",
#    "$393,151,347",
#)
#table.add_row(
#    "Dec 15 2017",
#    "Star Wars Ep. VIII: The Last Jedi",
#    "$262,000,000",
#    "[bold]$1,332,539,889[/bold]",
#)

#console.print(table)
