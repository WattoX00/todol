from platformdirs import user_data_dir
from pathlib import Path

def main():
    DATA_DIR = Path(user_data_dir('todol', 'todol'))
    TODO_DIR = DATA_DIR / 'todoFiles'

    if TODO_DIR.exists():
        print(f"Todol files:\n{TODO_DIR}")
    else:
        print("No data directory found. Run the app first: todol")