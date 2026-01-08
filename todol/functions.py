import json
import os

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory

# app start

todoPath = 'todoFiles'
todoJsonPath = './todoFiles/main.json'

if not os.path.exists(todoPath):
    os.makedirs(todoPath)
    with open(todoJsonPath, 'w') as f:
        f.write('{"tasks": {}}')

class Functions():

    # open Json (write on start)

    def openJson():
        with open(todoJsonPath, 'r') as f:
            data = json.load(f)
        
        for key in data['tasks']:
            title = data['tasks'][key]['name']
            description = data['tasks'][key]['desc']
            time = data['tasks'][key]['time']
            completed = data['tasks'][key]['completed']
            status = "✓" if completed else "✗"
            print(
                f"{key}. {title}\n"
                f"   desc: {description}\n"
                f"   time: {time}\n"
                f"   done: [{status}]\n"
            )

    # add task to json

    def addTaskJson(task):
        with open(todoJsonPath, 'r') as f:
            data = json.load(f)

        if data['tasks']:
            new_id = str(max(map(int, data['tasks'].keys())) + 1)
        else:
            new_id = "0"

        data['tasks'][new_id] = task

        with open(todoJsonPath, 'w') as f:
            json.dump(data, f, indent=4)
        print("Task Added")
        print()

    def addTask(full_cmd):
        title = " ".join(full_cmd)
        description = session.prompt('description > ').strip()
        time = session.prompt('when > ').strip()
        return {"name": title, "desc": description, "time": time, "completed": False}

    # remove task from json

    def removeTaskJson(index):
        with open(todoJsonPath, 'r') as f:
            data = json.load(f)
        del data['tasks'][index]
        with open(todoJsonPath, 'w') as f:
            json.dump(data, f, indent=4)
        print('Task is removed')
        print()

    # mark task as done in json

    def doneTaskJson(doneIndex):
        with open(todoJsonPath, 'r') as f:
            data = json.load(f)

        data['tasks'][str(doneIndex)]['completed'] = True

        with open(todoJsonPath, 'w') as f:
            json.dump(data, f, indent=4)
        print('Task is marked')
        print()

    # remove tasks that are completed

    def clearTaskJson():
        with open(todoJsonPath, 'r') as f:
            data = json.load(f)
        
        for count in list(data['tasks']):
            if data['tasks'][count]['completed']:
                del data['tasks'][count]

        with open(todoJsonPath, 'w') as f:
            json.dump(data, f, indent=4)
        print('Completed task are cleared out of the TODO list')
        print()

def cmd_add(args):
    data = Functions.addTask(args)
    Functions.addTaskJson(data)

def cmd_done(args):
    Functions.doneTaskJson(args[0])

def cmd_remove(args):
    Functions.removeTaskJson(args[0])

def cmd_help(args):
    print('help been given')

def cmd_list(args):
    Functions.openJson()

def cmd_clean(args):
    Functions.clearTaskJson()

def cmd_exit(args):
    raise SystemExit
        

def aliases(func, *names):
    return {name: func for name in names}

COMMANDS = {
    **aliases(cmd_add, "add", "a"),
    **aliases(cmd_done, "done", "d"),
    **aliases(cmd_remove, "remove", "rm", "r"),
    **aliases(cmd_help, "help", "h"),
    **aliases(cmd_list, "list", "l"),
    **aliases(cmd_clean, "clean", "c"),
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