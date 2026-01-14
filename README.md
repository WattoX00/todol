# Todol - Python TUI ToDo app

## Installation

```
pip install todol
```
More Info

- Check out the project page on PyPi: [https://pypi.org/project/todol/](https://pypi.org/project/todol/)
- and on Github: [https://github.com/WattoX00/todol](https://github.com/WattoX00/todol)

`todol` is a terminal application. I recommend installing it with `pipx`.

![Demo](assets/demo.png)

## Running

### Run from anywhere in you terminal with the command `todol`

## COMMAND GUIDE

```
┏━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Command    ┃ Alias  ┃ Action           ┃ Usage ┃
┡━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ add        │ a      │ Add new task     │ add   │
│ done       │ d      │ Mark task done   │ done  │
│ list       │ l      │ Show todo list   │ list  │
│ remove     │ rm     │ Remove task      │ rm    │
│ edit       │ e      │ Edit task        │ edit  │
│ clear      │ c      │ Clear done tasks │ clear │
│ help       │ h      │ Show help        │ help  │
│ exit       │ 0      │ Exit app         │ exit  │
└────────────┴────────┴──────────────────┴───────┘
Tip: You can use Tab for autocomplete.
Pro Tip: Navigate the terminal efficiently: arrow keys, backspace, and delete all work.
```

## FAQ

### Where are the saved todo files stored?

`todol` stores its data using `platformdirs.user_data_dir`, which means files are written to the standard user data directory for each operating system.

#### Default locations

- **Linux**
`~/.local/share/todol/todoFiles/`

- **macOS**
`~/Library/Application Support/todol/todoFiles/`

- **Windows**
`%APPDATA%\todol\todoFiles\`

## Hotkeys are available!

### Cursor navigation

| Key      | Action                           |
| -------- | -------------------------------- |
| `Ctrl‑a` | Move cursor to beginning of line |
| `Ctrl‑e` | Move cursor to end of line       |
| `Ctrl‑f` | Move cursor forward (right)      |
| `Ctrl‑b` | Move cursor backward (left)      |
| `Alt‑f`  | Move forward one word            |
| `Alt‑b`  | Move backward one word           |
| `Home`   | Go to start of line              |
| `End`    | Go to end of line                |

### Editing

| Key                    | Action                         |
| ---------------------- | ------------------------------ |
| `Ctrl‑d`               | Delete character under cursor  |
| `Ctrl‑h` / `Backspace` | Delete character before cursor |
| `Alt‑d`                | Delete word forward            |
| `Ctrl‑k`               | Kill (cut) text to end of line |
| `Ctrl‑y`               | Yank (paste) killed text       |
| `Ctrl‑t`               | Transpose characters           |

### History

| Key      | Action                |
| -------- | --------------------- |
| `Ctrl‑p` | Previous history item |
| `Ctrl‑n` | Next history item     |

### Searching

| Key      | Action                                                                 |
| -------- | ---------------------------------------------------------------------- |
| `Ctrl‑r` | Reverse search history                                                 |
| `Ctrl‑s` | Forward search history *(may be intercepted by terminal flow control)* |

### Completion & Accept

| Key          | Action                   |
| ------------ | ------------------------ |
| `Tab`        | Trigger completion       |
| `Ctrl‑Space` | Start/advance completion |
| `Enter`      | Accept input             |

### Misc

| Key        | Action                               |
| ---------- | ------------------------------------ |
| `Ctrl‑c`   | Cancel / raise KeyboardInterrupt     |
| `Ctrl‑z`   | Suspend (depends on shell)           |
| `Escape`   | Escape/Meta prefix for `Alt‑` combos |
| Arrow keys | Move cursor up/down/left/right       |

For the full official key binding documentation, check the prompt_toolkit docs: [prompt_toolkit GITHUB](https://github.com/prompt-toolkit/python-prompt-toolkit)

## Support

If you find this project helpful and would like to support its development, you can make a donation via the following method:

- [PayPal](https://www.paypal.com/paypalme/wattox)

Your contribution helps in maintaining and improving the app. Thank you for your support!

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
