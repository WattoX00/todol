from platformdirs import user_data_dir
from pathlib import Path

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
