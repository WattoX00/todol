from todol.functions import Functions, session, COMMANDS

# fix numbere list
def main():
    
    Functions.openJson()

    # main loop

    while True:
        raw = session.prompt('> ').strip()
        if not raw:
            continue

        parts = raw.split()
        command, *args = parts

        func = COMMANDS.get(command)

        if not func:
            print(f"Unknown command: {command}")
            continue

        try:
            func(args)
        except IndexError:
            print("Missing argument(s)")
        except SystemExit:
            break
