from .commands import Commands

def aliases(func, *names):
    return {name: func for name in names}


COMMANDS = {
    "add": Commands.cmd_add,
    "done": Commands.cmd_done,
    "edit": Commands.cmd_edit,
    "help": Commands.cmd_help,
    "list": Commands.cmd_list,
    "clear": Commands.cmd_clear,
    "order": Commands.cmd_order,
    "reload": Commands.cmd_reload,
    "exit": Commands.cmd_exit,
}

ALIASES = {
    "a": "add",
    "d": "done",
    "e": "edit",
    "h": "help",
    "ls": "list",
    "c": "clear",
    "o": "order",
    "rld": "reload",
    "q": "exit",
}

