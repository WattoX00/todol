import argparse

# Flags
from .flags.todol_path import TodolPath
from .flags.todol_list import TodolList
from .flags.todol_upgrade import TodolUpgrade
from .flags.todol_version import TodolVersion

# Functions for the main loop
from .functionality.functions import Functions
from .functionality.prompts import Prompts
from .functionality.commands_list import COMMANDS
from .functionality.commands import Commands
from .functionality.paths import reset_todolist, backup_todolist

from .todol_viewer import GuiApp

def parse_args():
    parser = argparse.ArgumentParser(
        prog="todol",
        description="Simple cli todo app by me for u <3",
        formatter_class=argparse.RawTextHelpFormatter
    )

    actions = parser.add_argument_group("Task actions")

    actions.add_argument("-a", "--add", nargs="+", metavar="TASK", help="Add a new task")
    actions.add_argument("-d", "--done", nargs="+", metavar="ID", help="Mark task as done")
    actions.add_argument("-c", "--clear", action="store_true", help="Remove completed tasks")
    actions.add_argument("-rst", "--reset", action="store_true", help="Reset Todo List!!!")
    actions.add_argument("-bk", "--backup", action="store_true", help="Create a backup")

    info = parser.add_argument_group("Information")
    info.add_argument("-w", "--viewer", action="store_true", help="Open GUI window")
    info.add_argument("-ls", "--list", action="store_true", help="List tasks to the terminal")
    info.add_argument("-p", "--path", action="store_true", help="Show data directory")
    info.add_argument("-u", "--upgrade", action="store_true", help="Upgrade todol")
    info.add_argument("-v", "--version", action="store_true", help="Show version")

    return parser.parse_args()

def main():
    args = parse_args()

    if args.viewer:
        GuiApp.main()
        return
    
    if args.reset:
        reset_todolist()
        return
    
    if args.backup:
        backup_todolist()
        return

    # commands (reused)

    if args.add:
        Commands.cmd_add(args.add)
        return
      
    if args.done:
        Commands.cmd_done(args.done)
        return
    
    if args.clear:
        Functions.clearTaskJson()
        return

    # Flag flags (reused)

    if args.path:
        TodolPath.path()
        return

    if args.list:
        TodolList.list()
        return

    if args.upgrade:
        TodolUpgrade.upgrade()
        return

    if args.version:
        TodolVersion.version()
        return

    # main loop

    Functions.greetingAppStart()

    while True:
        try:
            raw = Prompts.session.prompt('todol ~ $ ').strip()
        except KeyboardInterrupt:
            break

        if not raw:
            continue

        parts = raw.split()
        command, *args = parts

        func = COMMANDS.get(command)

        if not func:
            print(f'{command}: command not found')
            continue

        try:
            func(args)
        except IndexError:
            print('Missing argument')
        except (SystemExit, KeyboardInterrupt):
            break
main()