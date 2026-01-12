import json
import os

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory

from platformdirs import user_data_dir
from pathlib import Path

# app start

DATA_DIR = Path(user_data_dir('todol', 'todol'))
TODO_DIR = DATA_DIR / 'todoFilees'
TODO_JSON = TODO_DIR / 'main.json'
HISTORY_FILE = TODO_DIR / 'history'

TODO_DIR.mkdir(parents = True, exist_ok = True)

if not TODO_JSON.exists():
    TODO_JSON.write_text('{"tasks": {}}')

HISTORY_FILE.touch()
HISTORY_FILE.write_text('')

class Functions():

    # greeting

    def greetingAppStart():
        print(r"""
████████  ██████   █████     ██████   ██      
   ██    ██    ██  ██   ██  ██    ██  ██      
   ██    ██    ██  ██   ██  ██    ██  ██      
   ██    ██    ██  ██   ██  ██    ██  ██      
   ██     ██████   █████     ██████   ███████
        """)

        print(
            f'Type h or help to see the available commands and what they do!\n'
        )

    # open Json (write on start)

    def openJson():
        data: dict = Functions.load_todos()

        for key in data['tasks']:
            title: str = data['tasks'][key]['name']
            description: str = data['tasks'][key]['desc']
            time: str = data['tasks'][key]['time']
            completed: bool = data['tasks'][key]['completed']
            status: str = "✓" if completed else "✗"
            print(
                f'{key}. {title}\n'
                f'   desc: {description}\n'
                f'   time: {time}\n'
                f'   done: [{status}]\n'
            )

    # add task to json

    def addTaskJson(task):
        data: dict = Functions.load_todos()

        if data['tasks']:
            new_id: str = str(max(map(int, data['tasks'].keys())) + 1)
        else:
            new_id: str = '1'

        data['tasks'][new_id] = task

        Functions.save_todos(data)
        print(f'\nTask {new_id} Added!\n')

    def addTask(full_cmd):
        title: str = " ".join(full_cmd)
        description: str = session.prompt('[todol ~] description : ').strip()
        time: str = session.prompt('[todol ~] time : ').strip()
        return {'name': title, 'desc': description, 'time': time, 'completed': False}

    # remove task from json

    def removeTaskJson(index):
        
        data: dict = Functions.load_todos()
        
        try:
            del data['tasks'][index]

            Functions.save_todos(data)

            print(f'\nTask {index} is removed!\n')

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

            editTittle = session.prompt('[todol ~] title (edit) : ', default=title)
            editDesc = session.prompt('[todol ~] description (edit) : ', default=desc)
            editTime = session.prompt('[todol ~] time (edit) : ', default=time)

            data['tasks'][editIndex] = {'name': editTittle, 'desc': editDesc, 'time': editTime, 'completed': False}

            Functions.save_todos(data)

            print(f'\nTask {editIndex} Edited!\n')

        except ValueError:
            print('Invalid input. Please enter a valid number.')
        except KeyError:
            print('Invalid input. Please enter a valid number.')

    # mark task as done in json

    def doneTaskJson(doneIndex):
        
        data: dict = Functions.load_todos()
        
        try:
            data['tasks'][str(doneIndex)]['completed'] = True

            Functions.save_todos(data)

            print(f'\nTask {doneIndex} marked Done!\n')

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

        print('\nTODO list CLEARED!\n')

    # print help commands

    def helpText():
        BOLD = "\033[1m"
        RESET = "\033[0m"
        GREEN = "\033[92m"

        print(
            f"\n{BOLD}COMMAND GUIDE{RESET}\n"
            f"{'─' * 66}\n"
            f"{GREEN}add    | a{RESET}    → {BOLD}ADD{RESET} a new task          |  add/a [task]\n"
            f"{GREEN}done   | d{RESET}    → {BOLD}MARK{RESET} a task as {BOLD}DONE{RESET}     |  done/d [task_number]\n"
            f"{GREEN}list   | l{RESET}    → {BOLD}SHOW{RESET} your todo list     |  list/l \n"
            f"{GREEN}remove | rm {RESET}  → {BOLD}REMOVE{RESET} a task           |  remove/rm [task_number] \n"
            f"{GREEN}edit   | e {RESET}   → {BOLD}Edit{RESET} a task             |  edit/e [task_number] \n"
            f"{GREEN}clear  | c{RESET}    → {BOLD}REMOVE{RESET} completed tasks  |  clear/c \n"
            f"{GREEN}help   | h{RESET}    → {BOLD}SHOW{RESET} this help menu     |  help/h \n"
            f"{GREEN}exit   | 0{RESET}    → {BOLD}EXIT{RESET} the application    |  exit/0\n"
            f"{'─' * 66}\n"
            f"{BOLD}Tip:{RESET} You can use Tab for autocomplete.\n"
            f"{BOLD}Pro Tip:{RESET} Navigate the terminal efficiently: arrow keys, backspace, and delete all work.\n"
            f'Hotkeys are available! For full details, see the README: https://github.com/WattoX00/todol\n'
        )

    # load json file

    def load_todos():
        with open(TODO_JSON, 'r') as f:
            return json.load(f)

    # save to the json file

    def save_todos(data):
        with open(TODO_JSON, 'w') as f:
            json.dump(data, f, indent=4)


def cmd_add(args):
    data = Functions.addTask(args)
    Functions.addTaskJson(data)

def cmd_done(args):
    Functions.doneTaskJson(args[0])

def cmd_remove(args):
    Functions.removeTaskJson(args[0])

def cmd_edit(args):
    Functions.editTask(args[0])

def cmd_help(args):
    Functions.helpText()

def cmd_list(args):
    Functions.openJson()

def cmd_clear(args):
    Functions.clearTaskJson()

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
    **aliases(cmd_exit, "exit", "0"),
}

class ShellCompleter(Completer):
    def get_completions(self, document, complete_event):
        if not complete_event.completion_requested:
            return

        text = document.text_before_cursor
        words = text.split()

        if not words:
            for cmd in COMMANDS:
                yield Completion(cmd, start_position=0)
            return

        if len(words) == 1 and not text.endswith(" "):
            current = words[0]
            for cmd in COMMANDS:
                if cmd.startswith(current):
                    yield Completion(cmd, start_position=-len(current))
            return

        cmd = words[0]
        args = COMMANDS.get(cmd, [])

        if args:
            current = words[-1] if not text.endswith(" ") else ""
            for arg in args:
                if arg.startswith(current):
                    yield Completion(arg, start_position=-len(current))


session = PromptSession(
    completer=ShellCompleter(),
    complete_while_typing=False,
    history=FileHistory(HISTORY_FILE)
)