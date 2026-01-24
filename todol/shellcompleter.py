
from prompt_toolkit.completion import Completer, Completion

class ShellCompleter(Completer):
    def get_completions(self, document, complete_event):
        
        from .commands_list import COMMANDS
        
        if not complete_event.completion_requested:
            return

        text = document.text_before_cursor
        words = text.split()

        if not words:
            for cmd in COMMANDS:
                yield Completion(cmd, start_position=0)
            return

        if len(words) == 1 and not text.endswith(" "):
            current = words[0]
            for cmd in COMMANDS:
                if cmd.startswith(current):
                    yield Completion(cmd, start_position=-len(current))
            return

        cmd = words[0]
        args = COMMANDS.get(cmd, [])

        if args:
            current = words[-1] if not text.endswith(" ") else ""
            for arg in args:
                if arg.startswith(current):
                    yield Completion(arg, start_position=-len(current))

