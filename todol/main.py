import argparse

from .flags.todol_path import TodolPath
from .flags.todol_help import TodolHelp
from .flags.todol_show import TodolShow
from .flags.todol_upgrade import TodolUpgrade
from .flags.todol_version import TodolVersion

from .functionality.functions import Functions
from .functionality.prompts import Prompts
from .functionality.commands_list import COMMANDS

def parse_args():
    parser = argparse.ArgumentParser(prog="todol")

    parser.add_argument("--upgrade", action="store_true", help="Upgrade todol")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    return parser.parse_args()

def main():
    args = parse_args()

    # ---- FLAG MODE (non-interactive) ----
    if args.version:
        TodolVersion.version()
        return

    if args.upgrade:
        TodolUpgrade.upgrade()
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