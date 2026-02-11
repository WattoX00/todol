from prompt_toolkit.completion import Completer, Completion

from prompt_toolkit.completion import Completer, Completion

class ShellCompleter(Completer):
    def get_completions(self, document, complete_event):

        from .commands_list import COMMANDS
        from .functions import Functions
        # tags.py
        TAGS = Functions.load_tags()

        if not complete_event.completion_requested:
            return

        text = document.text_before_cursor
        words = text.split()

        if not words:
            for cmd in COMMANDS:
                yield Completion(cmd, start_position=0)
            return

        last = words[-1]

        if last.startswith("@"):
            current = last
            for tag in TAGS:
                if tag.startswith(current):
                    yield Completion(tag, start_position=-len(current))
            return

        if len(words) == 1 and not text.endswith(" "):
            current = words[0]
            for cmd in COMMANDS:
                if cmd.startswith(current):
                    yield Completion(cmd, start_position=-len(current))
            return
        return
