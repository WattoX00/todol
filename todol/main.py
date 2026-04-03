import argparse

# Flags
from .flags.todol_version import TodolVersion

def parse_args():
    parser = argparse.ArgumentParser(
        prog="todol",
        description=f"{TodolVersion.version()}\nSimple cli todo app",
        formatter_class=argparse.RawTextHelpFormatter
    )

    actions = parser.add_argument_group("Task actions")
    actions.add_argument("-a", "--add", nargs="+", metavar="TASK", help="Add new task")
    actions.add_argument("-d", "--done", nargs="+", metavar="ID", help="Mark task as done")
    actions.add_argument("-c", "--clear", action="store_true", help="Remove completed tasks")
    actions.add_argument("-o", "--order", action="store_true", help="Order Todos by ids")

    info = parser.add_argument_group("Information")
    info.add_argument("-ls", "--list", action="store_true", help="List tasks to the terminal")
    info.add_argument("-p", "--path", action="store_true", help="Show todo files in local directory")
    info.add_argument("-u", "--update", action="store_true", help="Update todol with pipx")
    info.add_argument("-up", "--upgrades", action="store_true", help="There's only one way to find out :)")
    info.add_argument("-v", "--version", action="store_true", help="Show version")

    file_action = parser.add_argument_group("File actions")
    file_action.add_argument("-rst", "--reset", action="store_true", help="Reset Todo list")
    file_action.add_argument("-bk", "--backup", action="store_true", help="Create backup")
    file_action.add_argument("-lbk", "--load", action="store_true", help="Load backup")

    return parser.parse_args()

def main():
    args = parse_args()

    # file actions

    if args.reset:
        from .functionality.paths import reset_todolist
        reset_todolist()
        return

    if args.backup:
        from .functionality.paths import backup_todolist
        backup_todolist()
        return

    if args.load:
        from .functionality.paths import load_backup
        load_backup()
        return

    # Flag flags

    if args.path:
        from .flags.todol_path import TodolPath
        TodolPath.path()
        return

    if args.list:
        from .flags.todol_list import TodolList
        TodolList.list()
        return

    if args.update:
        from .flags.todol_upgrade import TodolUpgrade
        TodolUpgrade.upgrade()
        return

    if args.upgrades:
        from .flags.todol_upgrades import main
        main()
        return

    if args.version:
        print(TodolVersion.version())
        return

    # commands

    if args.add:
        from .functionality.commands import Commands
        Commands.cmd_add(args.add)
        return

    if args.done:
        from .functionality.commands import Commands
        Commands.cmd_done(args.done)
        return

    if args.clear:
        Functions.clearTaskJson()
        return

    if args.order:
        from .functionality.functions import Functions
        Functions.orderList()
        return

    # main loop

    from .functionality.prompts import Prompts
    from .functionality.commands_list import COMMANDS, ALIASES
    from .functionality.functions import Functions

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
        command = command.lower()

        command = ALIASES.get(command, command)

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

