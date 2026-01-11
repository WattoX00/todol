import json
import os

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory

# app start

todoPath: str = 'todoFiles'
todoJsonPath: str = './todoFiles/main.json'


if not os.path.exists(todoPath):
    os.makedirs(todoPath)
    with open(todoJsonPath, 'w') as f:
        f.write('{"tasks": {}}')

# reset history

open('./todoFiles/my_history', 'w').close()

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
        with open(todoJsonPath, 'r') as f:
            data: dict = json.load(f)

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
        with open(todoJsonPath, 'r') as f:
            data: dict = json.load(f)

        if data['tasks']:
            new_id: str = str(max(map(int, data['tasks'].keys())) + 1)
        else:
            new_id: str = '0'

        data['tasks'][new_id] = task

        with open(todoJsonPath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f'\nTask {new_id} Added!\n')

    def addTask(full_cmd):
        title: str = " ".join(full_cmd)
        description: str = session.prompt('[todol ~] description : ').strip()
        time: str = session.prompt('[todol ~] time : ').strip()
        return {'name': title, 'desc': description, 'time': time, 'completed': False}

    # remove task from json

    def removeTaskJson(index):
        try:
            with open(todoJsonPath, 'r') as f:
                data: dict = json.load(f)

            del data['tasks'][index]
            with open(todoJsonPath, 'w') as f:
                json.dump(data, f, indent=4)
            print(f'\nTask {index} is removed!\n')

        except ValueError:
            print('Invalid input. Please enter a valid number.')
        except KeyError:
            print('Invalid input. Please enter a valid number.')

    # edit task

    def editTask(editIndex):
        try:
            with open(todoJsonPath, 'r') as f:
                data: dict = json.load(f)
            title: str = data['tasks'][editIndex]['name']
            desc: str = data['tasks'][editIndex]['desc']
            time: str = data['tasks'][editIndex]['time']
            editTittle = session.prompt('[todol ~] title (edit) : ', default=title)
            editDesc = session.prompt('[todol ~] description (edit) : ', default=desc)
            editTime = session.prompt('[todol ~] time (edit) : ', default=time)

            data['tasks'][editIndex] = {'name': editTittle, 'desc': editDesc, 'time': editTime, 'completed': False}

            with open(todoJsonPath, 'w') as f:
                json.dump(data, f, indent=4)
            print(f'\nTask {editIndex} Edited!\n')

        except ValueError:
            print('Invalid input. Please enter a valid number.')
        except KeyError:
            print('Invalid input. Please enter a valid number.')

    # mark task as done in json

    def doneTaskJson(doneIndex):
        with open(todoJsonPath, 'r') as f:
            data = json.load(f)
        try:
            data['tasks'][str(doneIndex)]['completed'] = True
            with open(todoJsonPath, 'w') as f:
                json.dump(data, f, indent=4)
            print(f'\nTask {doneIndex} marked Done!\n')

        except ValueError:
            print('Invalid input. Please enter a valid number.')
        except KeyError:
            print('Invalid input. Please enter a valid number.')

    # remove tasks that are completed

    def clearTaskJson():
        with open(todoJsonPath, 'r') as f:
            data = json.load(f)
        
        for count in list(data['tasks']):
            if data['tasks'][count]['completed']:
                del data['tasks'][count]

        with open(todoJsonPath, 'w') as f:
            json.dump(data, f, indent=4)
        print('\nTODO list CLEARED!\n')

    # print help commands

    def helpText():
        BOLD = "\033[1m"
        RESET = "\033[0m"
        GREEN = "\033[92m"

        print(
            f"\n{BOLD}COMMAND GUIDE{RESET}\n"
            f"{'─' * 65}\n"
            f"{GREEN}add    | a{RESET}      → {BOLD}ADD{RESET} a new task | add/a [task]\n"
            f"{GREEN}done   | d{RESET}      → {BOLD}MARK{RESET} a task as {BOLD}DONE{RESET} | done/d [task_number]\n"
            f"{GREEN}list   | l{RESET}      → {BOLD}SHOW{RESET} your todo list | list/l \n"
            f"{GREEN}remove | rm | r{RESET} → {BOLD}REMOVE{RESET} a task | remove/rm/r [task_number] \n"
            f"{GREEN}clear  | c{RESET}      → {BOLD}REMOVE{RESET} all completed tasks | clear/c \n"
            f"{GREEN}help   | h{RESET}      → {BOLD}SHOW{RESET} this help menu | help/h \n"
            f"{GREEN}exit   | 0{RESET}      → {BOLD}EXIT{RESET} the application | exit/0\n"
            f"{'─' * 65}\n"
            f"{BOLD}Tip:{RESET} You can use Tab for autocomplete.\n"
            f"{BOLD}Pro Tip:{RESET} Navigate the terminal efficiently: arrow keys, backspace, and delete all work.\n"
            f'Hotkeys are available! For full details, see the README: https://github.com/WattoX00/todol\n'
        )

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
    **aliases(cmd_remove, "remove", "rm", "r"),
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
    history=FileHistory("./todoFiles/my_history"),
)
