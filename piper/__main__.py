import time
import os
import argparse

from pypyr import pipelinerunner

from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich import inspect

console = Console()

#out = pipelinerunner.main_with_context(pipeline_name='pipelines/test-pipe',
#        dict_in={'arbkey':'pipe', 'anotherkey':'song'})

context = {}
pipelinerunner.prepare_and_run(
        pipeline_name='pipelines/test-pipe',
        working_dir=os.getcwd(),
        context=context,
        parse_input=False
        )

inspect(out)
#while out['finished'] == False:
#    console.print(out['progress'])
    #track(range(out['progress']))
#inspect(pipelinerunner, methods=True)
#inspect(out, methods=True)

#for step in track(range(100)):
#   time.sleep(0.3)

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
