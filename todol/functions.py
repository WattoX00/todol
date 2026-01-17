import json

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import clear

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import print

from platformdirs import user_data_dir
from pathlib import Path

# app start

DATA_DIR = Path(user_data_dir('todol', 'todol'))
TODO_DIR = DATA_DIR / 'todoFiles'
TODO_JSON = TODO_DIR / 'main.json'
HISTORY_FILE = TODO_DIR / 'history'

TODO_DIR.mkdir(parents = True, exist_ok = True)

if not TODO_JSON.exists():
    TODO_JSON.write_text('{"tasks": {}}')

HISTORY_FILE.touch()
HISTORY_FILE.write_text('')

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

    def addTaskJson(task):
        data: dict = Functions.load_todos()

        if data['tasks']:
            new_id: str = str(max(map(int, data['tasks'].keys())) + 1)
        else:
            new_id: str = '1'

        data['tasks'][new_id] = task

        Functions.save_todos(data)
        print(f'\n[bold yellow]Task {new_id} Added![/bold yellow]\n')

    def addTask(full_cmd):
        title: str = " ".join(full_cmd)
        description: str = Prompts.desc_session.prompt(HTML('\n<ansiblue>[todol ~] description : </ansiblue>\n'+ Prompts.line_prefix(1))).strip()
        time: str = Prompts.session.prompt('\n[todol ~] time : ').strip()
        return {'name': title, 'desc': description, 'time': time, 'completed': False}

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

    # edit task

    def editTask(editIndex):
        
        data: dict = Functions.load_todos()    
        
        try:
            title: str = data['tasks'][editIndex]['name']
            desc: str = data['tasks'][editIndex]['desc']
            time: str = data['tasks'][editIndex]['time']

            editTittle = Prompts.session.prompt('[todol ~] title (edit) : ', default=title)
            editDesc = Prompts.desc_session.prompt(HTML('\n<ansiblue>[todol ~] description (edit) : </ansiblue>\n'+Prompts.line_prefix(1)), default=desc)
            editTime = Prompts.session.prompt('\n[todol ~] time (edit) : ', default=time)   

            data['tasks'][editIndex] = {'name': editTittle, 'desc': editDesc, 'time': editTime, 'completed': False}

            Functions.save_todos(data)

            print(f'\n[bold yellow]Task {editIndex} Edited![/bold yellow]\n')

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

    # load json file

    def load_todos():
        with open(TODO_JSON, 'r') as f:
            return json.load(f)

    # save to the json file

    def save_todos(data):
        with open(TODO_JSON, 'w') as f:
            json.dump(data, f, indent=4)

class Commands():
    def cmd_add(args):
        data = Functions.addTask(args)
        Functions.addTaskJson(data)

    def cmd_done(args):
        Functions.doneTaskJson(args)

    def cmd_remove(args):
        Functions.removeTaskJson(args)

    def cmd_edit(args):
        Functions.editTask(args[0])

    def cmd_help(args):
        Functions.helpText()

    def cmd_list(args):
        Functions.openJson()

    def cmd_clear(args):
        Functions.clearTaskJson()

    def cmd_reload(args):
        Functions.greetingAppStart()

    def cmd_exit(args):
        raise SystemExit

    def aliases(func, *names):
        return {name: func for name in names}

    COMMANDS = {
        **aliases(cmd_add, "add", "a"),
        **aliases(cmd_done, "done", "d"),
        **aliases(cmd_remove, "remove", "rm"),
        **aliases(cmd_edit, "edit", "e"),
        **aliases(cmd_help, "help", "h"),
        **aliases(cmd_list, "list", "l"),
        **aliases(cmd_clear, "clear", "c"),
        **aliases(cmd_reload, "reload", "reset"),
        **aliases(cmd_exit, "exit", "0"),
    }

class ShellCompleter(Completer):
    def get_completions(self, document, complete_event):
        if not complete_event.completion_requested:
            return

        text = document.text_before_cursor
        words = text.split()

        if not words:
            for cmd in Commands.COMMANDS:
                yield Completion(cmd, start_position=0)
            return

        if len(words) == 1 and not text.endswith(" "):
            current = words[0]
            for cmd in Commands.COMMANDS:
                if cmd.startswith(current):
                    yield Completion(cmd, start_position=-len(current))
            return

        cmd = words[0]
        args = Commands.COMMANDS.get(cmd, [])

        if args:
            current = words[-1] if not text.endswith(" ") else ""
            for arg in args:
                if arg.startswith(current):
                    yield Completion(arg, start_position=-len(current))

class Prompts():
    def line_prefix(n: int) -> str:
        return f"{n:>3} | "

    def prompt_continuation(width, line_number, is_soft_wrap):
        return Prompts.line_prefix(line_number +1)

    def bottom_toolbar():
        return HTML(
            "<style fg='ansiblack' bg='ansiwhite'>"
            "  Esc+Enter: Save   Enter: New line   "
            "↑/↓: Move   Ctrl+U: Clear line  "
            "</style>"
        )

    session = PromptSession(
        completer=ShellCompleter(),
        complete_while_typing=False,
        history=FileHistory(HISTORY_FILE)
    )

    desc_session = PromptSession(
        completer=ShellCompleter(),
        complete_while_typing=False,
        multiline=True,
        prompt_continuation=prompt_continuation,
        bottom_toolbar=bottom_toolbar,
    )