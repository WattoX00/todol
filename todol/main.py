from .functions import Functions, session, COMMANDS

def main():
    Functions.greetingAppStart()
    Functions.openJson()

    # main loop

    while True:
        try:
            raw = session.prompt('[todol ~]$ ').strip()

        except KeyboardInterrupt:
            break

        if not raw:
            continue

        parts = raw.split()
        command, *args = parts

        func = COMMANDS.get(command)

        if not func:
            print(f'{command}: command not found')
            continue

        try:
            func(args)
        except IndexError:
            print('Missing argument')
        except SystemExit:
            break
        except KeyboardInterrupt:
            break