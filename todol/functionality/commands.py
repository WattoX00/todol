from .functions import Functions
from .prompts import Prompts

from rich import print

from prompt_toolkit.formatted_text import HTML

class Commands():
    def cmd_add(args):
            args = args or []

            try:
                task = " ".join(args)
            except IndexError:
                print("Add something bruhh")

            Functions.build_task(task)

    def cmd_done(args):
        Functions.doneTaskJson(args)

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

    def cmd_order(args):
        Functions.orderList()

    def cmd_exit(args):
        raise SystemExit
