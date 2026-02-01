from .paths import todoJsonListPath

import json
import re
from prompt_toolkit.shortcuts import clear
from rich.text import Text

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

        grouped = defaultdict(list)

        for task_id, task in tasks.items():
            raw_text = task.get("task", "")
            completed = task.get("completed", False)

            tags = TAG_RE.findall(raw_text) or ["untagged"]
            clean_text = TAG_RE.sub("", raw_text).strip()

            for tag in tags:
                grouped[tag].append({
                    "id": task_id,
                    "text": clean_text,
                    "completed": completed,
                })

        for tag, items in grouped.items():
            items.sort(key=lambda t: t["completed"])
            console.print()
            console.print(
                Text(f"@{tag}", style="bold magenta")
            )

            for task in items:
                if task["completed"]:
                    line = Text("  • ", style="dim")
                    line.append(f"{task['id']} ", style="dim cyan")
                    line.append("✔ ", style="green")
                    line.append(task["text"], style="dim strike")
                else:
                    line = Text("  • ", style="bold yellow")
                    line.append(f"{task['id']} ", style="bold cyan")
                    line.append(task["text"], style="white")

                console.print(line)

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
        table.add_row("edit", "e", "Edit task", "edit [id]")
        table.add_row("clear", "c", "Clear done tasks", "clear")
        table.add_row("help", "h", "Show help", "help")
        table.add_row("reload", "rld" "Reload the app", "reload")
        table.add_row("exit", "0", "Exit app", "exit")

        console.print(table)
        print(
            "\nBatch Operations:\n"
            "  done all       # mark all tasks done\n"
            "  done 2-4         # remove tasks 2, 3, 4\n"
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
