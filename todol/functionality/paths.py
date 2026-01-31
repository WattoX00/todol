from datetime import datetime
from platformdirs import user_data_dir
from pathlib import Path
from rich import print

# Todo files dir based on OS

DATA_DIR = Path(user_data_dir('todol', 'todol'))
TODO_DIR = DATA_DIR / 'todoFiles'

# Basic files for todol

TODO_JSON = TODO_DIR / 'main.json'
HISTORY_FILE = TODO_DIR / 'history'

# Backup dir

BACKUP_DIR = TODO_DIR / 'backups'

# Creating dictionaries

BACKUP_DIR.mkdir(parents=True, exist_ok=True)
TODO_DIR.mkdir(parents = True, exist_ok = True)

# Creating "blank" json

if not TODO_JSON.exists():
    TODO_JSON.write_text('{"tasks": {}}')

# Creating/Reseting history

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


def backup_todolist():
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        default_backup = BACKUP_DIR / f'backup-{timestamp}.json'

        print(
            f'[bold yellow]Save backup somewhere else (Leave blank for default)[/bold yellow]\n'
            f'{default_backup}\n'
            )
        user_path = input('> ').strip()

        if user_path:
            backup_path = Path(user_path).expanduser()
            if backup_path.is_dir():
                backup_path = backup_path / default_backup.name
        else:
            backup_path = default_backup

        backup_path.parent.mkdir(parents=True, exist_ok=True)

        backup_path.write_text(TODO_JSON.read_text(), encoding='utf-8')

        print(f'[bold green]Todo list backed up to:[/bold green] {backup_path}')

    except KeyboardInterrupt:
        print('\n[bold red]No backup were made[/bold red]')