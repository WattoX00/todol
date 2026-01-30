import argparse

# Flags
from .flags.todol_help import TodolHelp
from .flags.todol_path import TodolPath
from .flags.todol_list import TodolList
from .flags.todol_upgrade import TodolUpgrade
from .flags.todol_version import TodolVersion

# Functions for the main loop
from .functionality.functions import Functions
from .functionality.prompts import Prompts
from .functionality.commands_list import COMMANDS
from .functionality.commands import Commands

def parse_args():
    parser = argparse.ArgumentParser(
        prog="todol",
        description="Simple cli todo app",
        formatter_class=argparse.RawTextHelpFormatter
    )

    actions = parser.add_argument_group("Task actions")
    actions.add_argument("-a", "--add", nargs="+", metavar="TASK", help="Add a new task")
    actions.add_argument("-rm", "--remove", nargs="+", metavar="ID", help="Remove task by ID")
    actions.add_argument("-d", "--done", nargs="+", metavar="ID", help="Mark task as done")
    actions.add_argument("-c", "--clear", action="store_true", help="Remove completed tasks")

    info = parser.add_argument_group("Information")
    info.add_argument("-ls", "--list", action="store_true", help="List all tasks")
    info.add_argument("-p", "--path", action="store_true", help="Show data directory")
    info.add_argument("-u", "--upgrade", action="store_true", help="Upgrade todol")
    info.add_argument("-v", "--version", action="store_true", help="Show version")

    return parser.parse_args()

def main():
    args = parse_args()

    # commands (reused)

    if args.add:
        Commands.cmd_add(args.add)
        return
    
    if args.remove:
        Commands.cmd_remove(args.remove)
        return
    
    if args.done:
        Commands.cmd_done(args.done)
        return
    
    if args.clear:
        Commands.cmd_clear()
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
