from .shellcompleter import ShellCompleter
from .files import todoHistoryFilePath

from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import Condition
from prompt_toolkit.application.current import get_app

class Prompts:
    kb = KeyBindings()

    @staticmethod
    def line_prefix(n: int) -> str:
        return f"{n:>3} | "

    @staticmethod
    def prompt_continuation(width, line_number, is_soft_wrap):
        return Prompts.line_prefix(line_number + 1)

    @staticmethod
    def editing_bottom_toolbar():
            text = (
                "[MULTILINE MODE]  "
                "Switch mode: Ctrl+D  |  "
                "Save: Esc+Enter  |  "
                "New line: Enter  |  "
                "Move: ↑/↓  |  "
                "Clear line: Ctrl+U"
            )
            app = get_app()
            width = app.output.get_size().columns
            padded = text.ljust(width)
            return HTML(f"<style fg='ansiblack' bg='ansiwhite'>{padded}</style>")

    @staticmethod
    def normal_bottom_toolbar():
            text = (
                "[NORMAL MODE]  "
                "Switch mode: Ctrl+D  |  "
                "Execute: Enter"
            )
            app = get_app()
            width = app.output.get_size().columns
            padded = text.ljust(width)
            return HTML(f"<style fg='ansiblack' bg='ansiwhite'>{padded}</style>")
    @Condition
    def desc_mode():
        return getattr(Prompts.session, "_desc_mode", False)

    @staticmethod
    def dynamic_multiline():
        return Prompts._desc_mode()

    def dynamic_prompt_continuation(width, line_number, is_soft_wrap):
        if Prompts.desc_mode():
            return Prompts.prompt_continuation(width, line_number, is_soft_wrap)
        return ""

    def dynamic_toolbar():
        if Prompts.desc_mode():
            return Prompts.editing_bottom_toolbar()
        return Prompts.normal_bottom_toolbar()

    @kb.add("c-d")
    def toggle_desc_mode(event):
        Prompts.session._desc_mode = not getattr(Prompts.session, "_desc_mode", False)
        event.app.invalidate()

    session = PromptSession(
        completer=ShellCompleter(),
        complete_while_typing=False,
        history=FileHistory(todoHistoryFilePath()),
        multiline=desc_mode,
        prompt_continuation=dynamic_prompt_continuation,
        bottom_toolbar=dynamic_toolbar,
        key_bindings=kb,
    )
