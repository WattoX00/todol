from .functions import Functions, Prompts, Commands

def main():
    Functions.greetingAppStart()

    # main loop

    while True:
        try:
            raw = Prompts.session.prompt('[todol ~]$ ').strip()

        except KeyboardInterrupt:
            break

        if not raw:
            continue

        parts = raw.split()
        command, *args = parts

        func = Commands.COMMANDS.get(command)
        
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
