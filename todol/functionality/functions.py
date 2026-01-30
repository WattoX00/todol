from .paths import todoJsonListPath

import json

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.text import Text
from rich.table import Table
from rich import print

from prompt_toolkit.shortcuts import clear

class Functions():

    # greeting
    # reload view

    def greetingAppStart():

        clear()

        print(r"""
████████  ██████   █████     ██████   ██      
   ██    ██    ██  ██   ██  ██    ██  ██      
   ██    ██    ██  ██   ██  ██    ██  ██      
   ██    ██    ██  ██   ██  ██    ██  ██      
   ██     ██████   █████     ██████   ███████
        """)

        print('[bold yellow]Type h or help to see the available commands and what they do![/bold yellow]\n')
        
        Functions.openJson()

    def getAllTasks() -> dict:
        data = Functions.load_todos()
        return data['tasks']

    def update_task(task_id: str, desc: str):

            data = Functions.load_todos()
            data['tasks'][task_id] = {
                "desc": desc,
                "completed": False,
            }
            Functions.save_todos(data)

    # open Json (write on start)

    def openJson() -> list:
        console = Console()
        tasks = Functions.getAllTasks()

        pending = []
        completed = []

        for task_id, task in tasks.items():
            (completed if task.get("completed") else pending).append((task_id, task))

        table = Table(
            title="Todo",
            show_header=False,
            box=None,
            pad_edge=False,
            show_lines=False,
            padding=(0, 1),
            caption=f"[dim]{len(pending)} pending • {len(completed)} completed[/dim]",
        )

        table.add_column(justify="right", width=5)
        table.add_column("Task", style="white")
        table.add_column(justify="right", style="dim", width=4)

        def add_task(task_id, task, done=False):
            icon = "[green]✔[/green]" if done else "[bold yellow]☐[/bold yellow]"
            desc = task.get("desc", "")
            desc = f"[dim strike]{desc}[/dim strike]" if done else desc

            table.add_row(icon, desc, f"[dim]{task_id}[/dim]")
            table.add_row("", "", "")

        for task_id, task in pending:
            add_task(task_id, task)

        if completed:
            table.add_section()
            for task_id, task in completed:
                add_task(task_id, task, done=True)

        console.print(table)


    # add task to json

    def addTaskJson(task: dict):
        data: dict = Functions.load_todos()

        if data['tasks']:
            new_id: str = str(max(map(int, data['tasks'].keys())) + 1)
        else:
            new_id: str = '1'

        data['tasks'][new_id] = task

        Functions.save_todos(data)
        print(f'\n[bold yellow]Task {new_id} Added![/bold yellow]\n')


    def build_task(desc: str):
        task = {
            "desc": desc,
            "completed": False,
        }
        
        Functions.addTaskJson(task)

    # remove task from json

    def removeTaskJson(index: list) -> str:

        data: dict = Functions.load_todos()

        try:
            if index[0] == "all":
                data['tasks'].clear()

                print(f'\n[bold yellow]All Tasks been removed![/bold yellow]\n')
            else:
                for arg in index:

                    if "-" in arg:
                        min_i, max_i = arg.split("-")

                        for task in range(int(min_i), int(max_i) + 1):
                            task = str(task)
                            if task in data['tasks']:
                                del data['tasks'][task]

                        print(f'\n[bold yellow]Tasks {index[0]} been removed![/bold yellow]\n')

                    else:
                        del data['tasks'][str(arg)]

                        print(f'\n[bold yellow]Task(s) {index} been removed![/bold yellow]\n')
            Functions.save_todos(data)

        except ValueError:
            print('Invalid input. Please enter a valid number.')
        except KeyError:
            print('Invalid input. Please enter a valid number.')

    # mark task as done in json

    def doneTaskJson(doneIndex: list) -> str:

        data: dict = Functions.load_todos()

        try:
            if doneIndex[0] == "all":
                for key in data['tasks']:
                    data['tasks'][key]['completed'] = True

            else:
                for arg in doneIndex:
                
                    if "-" in arg:
                        min_i, max_i = arg.split("-")

                        for task in range(int(min_i), int(max_i) + 1):
                            task = str(task)
                            if task in data['tasks']:
                                data['tasks'][task]['completed'] = True

                    else:
                        data['tasks'][str(arg)]['completed'] = True

            Functions.save_todos(data)

            print(f'\n[bold yellow]Task(s) {doneIndex} marked Done![/bold yellow]\n')

        except ValueError:
            print('Invalid input. Please enter a valid number.')
        except KeyError:
            print('Invalid input. Please enter a valid number.')

    # remove tasks that are completed

    def clearTaskJson():

        data: dict = Functions.load_todos()
        
        for count in list(data['tasks']):
            if data['tasks'][count]['completed']:
                del data['tasks'][count]

        Functions.save_todos(data)

        print('\n[bold yellow]TODO list CLEARED![/bold yellow]\n')

    # print help commands

    def helpText() -> str:
        console = Console()

        table = Table(show_header=True, header_style="bold")

        table.add_column("Command", style="cyan", width=10)
        table.add_column("Alias", style="green", width=6)
        table.add_column("Action", style="bold")
        table.add_column("Usage", style="dim")

        table.add_row("add", "a", "Add new task", "add [task]")
        table.add_row("done", "d", "Mark task done", "done [id]")
        table.add_row("list", "l", "Show todo list", "list")
        table.add_row("remove", "rm", "Remove task", "rm [id]")
        table.add_row("edit", "e", "Edit task", "edit [id]")
        table.add_row("clear", "c", "Clear done tasks", "clear")
        table.add_row("help", "h", "Show help", "help")
        table.add_row("reload", "reset", "Reload the app", "reload")
        table.add_row("exit", "0", "Exit app", "exit")

        console.print(table)
        print(
            "\nBatch Operations:\n"
            "  done all       # mark all tasks done\n"
            "  rm 2-4         # remove tasks 2, 3, 4\n"
            "  done 1 5 7     # mark tasks 1, 5, and 7 done"
        )

    # load json file

    def load_todos() -> dict:
        with open(todoJsonListPath(), 'r') as f:
            return json.load(f)

    # save to the json file

    def save_todos(data: dict):
        with open(todoJsonListPath(), 'w') as f:
            json.dump(data, f, indent=4)
