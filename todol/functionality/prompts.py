from .shellcompleter import ShellCompleter
from .paths import todoHistoryFilePath

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

class Prompts:
        session = PromptSession(
        completer=ShellCompleter(),
        complete_while_typing=False,
        history=FileHistory(todoHistoryFilePath()),
    )
