from .functions import Functions
from .prompts import Prompts

from prompt_toolkit.formatted_text import HTML

class Commands():
    def cmd_add(args):

        title = " ".join(args)

        description: str = Prompts.session.prompt(HTML('\n<ansiblue>[todol ~] description : </ansiblue>\n'+ Prompts.line_prefix(1))).strip()
        time: str = Prompts.session.prompt('\n[todol ~] time : ').strip()
                

        task = Functions.build_task(title, description, time)
        Functions.addTaskJson(task)

    def cmd_done(args):
        Functions.doneTaskJson(args)

    def cmd_remove(args):
        Functions.removeTaskJson(args)

    def cmd_edit(args):

        try:
            taskId = args[0]
            task = Functions.getTask(taskId)

            title: str = task['name']
            desc: str = task['desc']
            time: str = task['time']

            editTittle = Prompts.session.prompt('[todol ~] title (edit) : ', default=title)
            
            editDesc = Prompts.session.prompt(HTML('\n<ansiblue>[todol ~] description (edit) : </ansiblue>\n'+Prompts.line_prefix(1)), default=desc)
            
            editTime = Prompts.session.prompt('\n[todol ~] time (edit) : ', default=time)   

            Functions.update_task(taskId, editTittle, editDesc, editTime)

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

    def aliases(func, *names):
        return {name: func for name in names}

    COMMANDS = {
        **aliases(cmd_add, "add", "a"),
        **aliases(cmd_done, "done", "d"),
        **aliases(cmd_remove, "remove", "rm"),
        **aliases(cmd_edit, "edit", "e"),
        **aliases(cmd_help, "help", "h"),
        **aliases(cmd_list, "list", "ll", "ls", "l"),
        **aliases(cmd_clear, "clear", "clean", "c"),
        **aliases(cmd_reload, "reload", "reset"),
        **aliases(cmd_exit, "exit", "0", "q"),
    }
