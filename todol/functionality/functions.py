from .paths import todoJsonListPath

import json
import re
from prompt_toolkit.shortcuts import clear

from rich.console import Console
from rich.table import Table
from rich import print

from collections import defaultdict

class Functions():

    # greeting
    # reload view

    def greetingAppStart():

        clear()

        print(r"""
   ▄▄▄█████▓ ▒█████   ▓█████▄  ▒█████   ██▓    
   ▓  ██▒ ▓▒▒██▒  ██▒ ▒██▀ ██▌▒██▒  ██▒▓██▒    
   ▒ ▓██░ ▒░▒██░  ██▒ ░██   █▌▒██░  ██▒▒██░    
   ░ ▓██▓ ░ ▒██   ██░ ░▓█▄   ▌▒██   ██░▒██░    
     ▒██▒ ░ ░ ████▓▒░ ░▒████▓ ░ ████▓▒░░██████▒
     ▒ ░░   ░ ▒░▒░▒░   ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░▓  ░
       ░      ░ ▒ ▒░   ░ ▒  ▒   ░ ▒ ▒░ ░ ░ ▒  ░
     ░      ░ ░ ░ ▒    ░ ░  ░ ░ ░ ░ ▒    ░ ░   
                ░ ░      ░        ░ ░      ░  ░
"""
)
        print("[dim]      Type [bold]h[/bold] or [bold]help[/bold] to see available commands[/dim]\n")
        Functions.openJson()

    def getAllTasks() -> dict:
        data = Functions.load_todos()
        return data['tasks']

    def update_task(task_id: str, task: str):

            data = Functions.load_todos()
            data['tasks'][task_id] = {
                "task": task,
                "completed": False,
            }
            Functions.save_todos(data)

    # open Json (write on start)

    def openJson() -> None:
        TAG_RE = re.compile(r'@(\w+)')
        console = Console()
        tasks = Functions.getAllTasks()

        grouped = defaultdict(lambda: {"pending": [], "completed": []})

        for task_id, task in tasks.items():
            raw_text = task.get("task", "")

            # Extract tags from task text
            tags = TAG_RE.findall(raw_text)
            tags = tags if tags else ["untagged"]

            # Clean task text (remove tags)
            clean_text = TAG_RE.sub("", raw_text).strip()
            task["task"] = clean_text

            status = "completed" if task.get("completed") else "pending"

            for tag in tags:
                grouped[tag][status].append((task_id, task))

        for tag, buckets in grouped.items():
            pending = buckets["pending"]
            completed = buckets["completed"]

            console.print(
                f"\n[bold cyan]@{tag}[/bold cyan] "
                f"[dim]({len(pending)} pending • {len(completed)} done)[/dim]"
            )

            def render_task(task_id, task, done=False):
                icon = "[green]✔[/green]" if done else "[yellow]☐[/yellow]"
                text = task.get("task", "")
                if done:
                    text = f"[dim strike]{text}[/dim strike]"

                console.print(f"  {icon} {text} [dim]{task_id}[/dim]")

            for task_id, task in pending:
                render_task(task_id, task)

            for task_id, task in completed:
                render_task(task_id, task, done=True)
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


    def build_task(task: str):
        task_data = {
            "task": task,
            "completed": False,
        }

        Functions.addTaskJson(task_data)


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
        table.add_row("list", "ls", "Show todo list", "list")
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
