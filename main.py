import os
import sys
from typing import List

class Shell:
    COMMANDS = {
        "echo": "shell builtin",
        "exit": "shell builtin",
        "type": "shell builtin",
        "pwd": "shell builtin",
        "cd": "shell builtin"
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
            "echo": self.process_echo,
            "type": self.process_type,
            "pwd": self.process_pwd,
            "cd": self.process_cd
        }

        handler = handlers.get(cmd)
        if handler:
            handler(args)
            return
        print(f"{command}: command not found")

    def process_echo(self, args: List[str]) -> None:
        print(" ".join(args))

    def process_type(self, args: List[str]) -> None:
        if not args:
            print("type: missing command name")
            return
        command = args[0]
        if command in self.COMMANDS:
            print(f"{command} is a {self.COMMANDS[command]}")
            return

        print(f"{command}: command not found")

    def process_pwd(self, args: List[str]) -> None:
        print(os.getcwd())

    def process_cd(self, args: List[str]) -> None:
        if not args:
            return

        path = args[0]
        if not path.startswith('/'):
            path = os.path.normpath(os.path.join(os.getcwd(),path))
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")
        except NotADirectoryError:
            print(f"cd: {path}: Not a directory")


if __name__ == "__main__":
    shell = Shell()
    shell.run()
    sys.exit()