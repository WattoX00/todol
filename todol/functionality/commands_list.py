from .commands import Commands

def aliases(func, *names):
    return {name: func for name in names}

COMMANDS = {
    **aliases(Commands.cmd_add, "add", "a"),
    **aliases(Commands.cmd_done, "done", "d"),
    **aliases(Commands.cmd_edit, "edit", "e"),
    **aliases(Commands.cmd_help, "help", "h"),
    **aliases(Commands.cmd_list, "list", "ls",),
    **aliases(Commands.cmd_clear, "clear", "c"),
    **aliases(Commands.cmd_order, "order", "o"),
    **aliases(Commands.cmd_reload, "reload", "rld"),
    **aliases(Commands.cmd_exit, "exit", "q"),
}
