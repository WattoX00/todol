import argparse

from .flags.todol_help import TodolHelp
from .flags.todol_path import TodolPath
from .flags.todol_list import TodolList
from .flags.todol_upgrade import TodolUpgrade
from .flags.todol_version import TodolVersion

from .functionality.functions import Functions
from .functionality.prompts import Prompts
from .functionality.commands_list import COMMANDS

def parse_args():
    parser = argparse.ArgumentParser(prog="todol")

    parser.add_argument("-c", "--commands", action="store_true", help="Show interactive commands")
    parser.add_argument("-p", "--path", action="store_true", help="Show todol data directory")
    parser.add_argument("-l", "--list", action="store_true", help="Upgrade todol")
    parser.add_argument("-u", "--upgrade", action="store_true", help="Upgrade todol")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    return parser.parse_args()

def main():
    args = parse_args()

    if args.commands:
        TodolHelp.help()
        return

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