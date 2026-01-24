from .files import todoJsonListPath
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import print
from prompt_toolkit.shortcuts import clear
import json

from prompt_toolkit.formatted_text import HTML

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

    # open Json (write on start)

    def openJson():
        console = Console()
        data = Functions.load_todos()
        tasks = data.get("tasks", {})

        pending = []
        completed = []

        for task_id, task in tasks.items():
            if task.get("completed"):
                completed.append((task_id, task))
            else:
                pending.append((task_id, task))

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title="Todo List",
            caption=f"Pending: {len(pending)} | Completed: {len(completed)}"
        )

        table.add_column("ID", style="cyan", width=3, no_wrap=True)
        table.add_column("Task", style="bold white", min_width=20)
        table.add_column("Description", style="dim", overflow="fold")
        table.add_column("Time", style="yellow", width=10)
        table.add_column("Status", justify="center", width=10)

        def render_row(task_id, task, completed=False):
            status = Text("DONE", style="bold green") if completed else Text("TODO", style="bold red")
            name = Text(task["name"])

            if completed:
                name.stylize("strike dim")

            return [
                task_id,
                name,
                task.get("desc", ""),
                task.get("time", "-"),
                status
            ]

        for task_id, task in pending:
            table.add_row(*render_row(task_id, task))

        if completed:
            table.add_section()
            for task_id, task in completed:
                table.add_row(*render_row(task_id, task, completed=True))

        console.print((table))

    # add task to json

    """
    Due: in 3h
    Due: in 2d 4h
    Due: tomorrow 9am
    Due: next monday 14:00
    """

    def addTaskJson(task):
        data: dict = Functions.load_todos()

        if data['tasks']:
            new_id: str = str(max(map(int, data['tasks'].keys())) + 1)
        else:
            new_id: str = '1'

        data['tasks'][new_id] = task

        Functions.save_todos(data)
        print(f'\n[bold yellow]Task {new_id} Added![/bold yellow]\n')


    def build_task(title, desc, time):
        return {
            "name": title,
            "desc": desc,
            "time": time,
            "completed": False,
        }

    # remove task from json

    def removeTaskJson(index):
        
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

    def doneTaskJson(doneIndex):
        
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

    def helpText():
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
            "You can apply commands to multiple tasks at once:\n"
            "  - Use 'all' to target all tasks\n"
            "  - Specify a range with 'start-end', e.g., 2-5\n"
            "  - List multiple IDs separated by spaces, e.g., 1 3 7\n"
            "Examples:\n"
            "  done all       # mark all tasks done\n"
            "  rm 2-4         # remove tasks 2, 3, 4\n"
            "  done 1 5 7     # mark tasks 1, 5, and 7 done"
        )

    # load json file

    def load_todos():
        with open(todoJsonListPath(), 'r') as f:
            return json.load(f)

    # save to the json file

    def save_todos(data):
        with open(todoJsonListPath(), 'w') as f:
            json.dump(data, f, indent=4)
