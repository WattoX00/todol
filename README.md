# Todol - Simple cli ToDo app

[![Version](https://img.shields.io/badge/version-0.3.1-blue?style=for-the-badge)](https://github.com/WattoX00/todol/releases/tag/v0.3.1)
![Python](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge)
[![PyPI](https://img.shields.io/pypi/v/todol?style=for-the-badge)](https://pypi.org/project/todol/)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)
![Build](https://img.shields.io/github/actions/workflow/status/wattox00/todol/publish.yml?style=for-the-badge)
[![License](https://img.shields.io/github/license/wattox00/todol?style=for-the-badge)](https://github.com/WattoX00/todol/blob/main/LICENSE)

![Demo](assets/demo.png)

<details>
<summary>📚 Contents</summary>
 
- [Installation](#installation)
- [Usage](#usage)
- [Command Guide](#command-guide)
- [FAQ](#faq)
- [Hotkeys](#hotkeys)
- [Support](#support)
- [License](#license)

</details>


## Installation

```
pip install todol
```

> [!IMPORTANT]
> `todol` is a terminal application. I recommend installing it with `pipx`.

More Info

- Check out the project page on PyPi: [https://pypi.org/project/todol/](https://pypi.org/project/todol/)
- and on Github: [https://github.com/WattoX00/todol](https://github.com/WattoX00/todol)

## Usage

### Run from anywhere in your terminal

```
todol
```

### Additional flags

View all flags (for more options):

```
todol-help
```

Check the current version:

```
todol-version
```

See where todo files are saved:

```
todol-path
```

Update todol with a single command


> [!CAUTION]
> This runs `pipx upgrade todol` under the hood.

```
todol-upgrade
```

## COMMAND GUIDE

```
 Command     Alias      Action          Usage 

 add         a       Add new task       add [task]
 done        d       Mark task done     done [id]
 list        l       Show todo list     list
 remove      rm      Remove task        rm [id]
 edit        e       Edit task          edit [id]
 clear       c       Clear done tasks   clear
 help        h       Show help          help
 reload    reset     Reload the app     reload
 exit        0       Exit app           exit
```
> [!TIP]
> ### Pro Tips: 
- You can use Tab for autocomplete.
- Navigate the terminal efficiently: arrow keys, backspace, and delete all work.
- You can execute multiple commands at once:
    - all - apply the command to all items

    - id-id – apply the command to a range of IDs

    - id1 id2 id3 – apply the command to specific IDs

### examples:

```
done all       # marks all tasks as done
remove 4-7     # removes tasks with IDs 4 through 7
rm 3 5 8       # removes tasks 3, 5, and 8
```

## FAQ

### Where are the saved todo files stored?

#### You can simply check it by running `todol-path`

`todol` stores its data using `platformdirs.user_data_dir`, which means files are written to the standard user data directory for each operating system.

#### Default locations

- **Linux**
`~/.local/share/todol/todoFiles/`

- **macOS**
`~/Library/Application Support/todol/todoFiles/`

- **Windows**
`%APPDATA%\todol\todoFiles\`

## Hotkeys

<details>
<summary>Click to expand</summary>

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

</details>

## Support

If you find this project helpful and would like to support its development, you can make a donation via the following method:

- [PayPal](https://www.paypal.com/paypalme/wattox)

Your contribution helps in maintaining and improving the app. Thank you for your support!

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
