from platformdirs import user_data_dir
from pathlib import Path
from rich import print

DATA_DIR = Path(user_data_dir('todol', 'todol'))
TODO_DIR = DATA_DIR / 'todoFiles'
TODO_JSON = TODO_DIR / 'main.json'
HISTORY_FILE = TODO_DIR / 'history'

TODO_DIR.mkdir(parents = True, exist_ok = True)

if not TODO_JSON.exists():
    TODO_JSON.write_text('{"tasks": {}}')

HISTORY_FILE.touch()
HISTORY_FILE.write_text('')

def todoJsonListPath():
    return TODO_JSON

def todoHistoryFilePath():
    return HISTORY_FILE

def reset_todolist():
    print(
        '[bold red]!!! DANGER: THIS WILL ERASE ALL TODO DATA !!![/bold red]\n'
        'Make sure you have a backup first. You can run "todol --backup" or save a copy manually.\n'
    )

    choice = input('Do you really want to delete all tasks? [y/N] ').strip().lower()
    if choice in ('y', 'yes'):
        TODO_JSON.write_text('{"tasks": {}}')
        print('[bold green]All tasks have been cleared.[/bold green]')

    elif choice in ('', 'no', 'n'):
        print('[bold red]Operation cancelled. No data was lost.[/bold red]')
