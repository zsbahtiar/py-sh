import os
import sys
from typing import List

class Shell:
    COMMANDS = {
        "echo": "shell builtin"
    }

    def __init__(self):
        self.running = True
        self.path = os.getenv("PATH", "").split(":")

    def run(self) -> None:
        while self.running:
            try:
                sys.stdout.write("$ ")
                sys.stdout.flush()
                command = input()
                self.process_cmd(command)
            except KeyboardInterrupt:
                print("\nuse 'exit 0' to exit the shell")
            except EOFError:
                break
    def process_cmd(self, command: str) -> None:
        if not command.strip():
            return

        parts = command.split()
        cmd, args = parts[0], parts[1:]

        if cmd == "exit" and args == ["0"]:
            self.running = False
            return

        if not args and cmd not in self.COMMANDS:
            print(f"{command}: command not found")
            return

        handlers = {
            "echo": self.process_echo
        }

        handler = handlers.get(cmd)
        if handler:
            handler(args)
            return
        print(f"{command}: command not found")

    def process_echo(self, args: List[str]) -> None:
        print(" ".join(args))

if __name__ == "__main__":
    shell = Shell()
    shell.run()
    sys.exit()