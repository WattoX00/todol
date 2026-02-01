from .functions import Functions
from .prompts import Prompts

from rich import print

from prompt_toolkit.formatted_text import HTML

class Commands():
    def cmd_add(args):
        if not args:
            print("Add something bruhh")
            return

        words = []
        tags = []

        for arg in args:
            if arg.startswith("@") and len(arg) > 1:
                tags.append(arg[1:])  # remove '@'
            else:
                words.append(arg)

        task_text = " ".join(words)

        if not task_text:
            print("Task text missing")
            return

        Functions.build_task(task_text, tags)


    def cmd_done(args):
        Functions.doneTaskJson(args)

    def cmd_remove(args):
        Functions.removeTaskJson(args)

    def cmd_edit(args):
        try:
            taskId = args[0]
            task = Functions.getAllTasks()

            defTask: str = task[taskId]['task']

            editTask = Prompts.session.prompt(HTML('\n<ansiblue>todol ~ task (edit) : </ansiblue>'), default=defTask)

            Functions.update_task(taskId, editTask)

            print(f'\n[bold yellow]Task {taskId} Edited![/bold yellow]\n')

        except ValueError:
            print('Invalid input. Please enter a valid number.')
        except KeyError:
            print('Invalid input. Please enter a valid number.')

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
