from .functions import Functions
from .prompts import Prompts

from rich import print

from prompt_toolkit.formatted_text import HTML

class Commands():
    def cmd_add(args):
            args = args or []

            try:
                description = " ".join(args)
            except IndexError:
                description = Prompts.session.prompt(
                    HTML('\n<ansiblue>todol ~ description : </ansiblue>\n' + Prompts.line_prefix(1))
                ).strip()

            Functions.build_task(description)


    def cmd_done(args):
        Functions.doneTaskJson(args)

    def cmd_remove(args):
        Functions.removeTaskJson(args)

    def cmd_edit(args):
        try:
            taskId = args[0]
            task = Functions.getAllTasks()

            desc: str = task[taskId]['desc']

            
            editDesc = Prompts.session.prompt(HTML('\n<ansiblue>todol ~ description (edit) : </ansiblue>\n'+Prompts.line_prefix(1)), default=desc)

            Functions.update_task(taskId, editDesc)

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
