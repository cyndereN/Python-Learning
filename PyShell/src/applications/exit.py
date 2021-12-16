from typing import Deque

from application import Application


class Exit(Application):
    """Exit shell with argument"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        print("=== Thank you for using COMP0010 Shell ===")
        out.append("")
        if len(args) == 0 or args[0] == "":
            exit(0)
        try:
            exit(int(args[0]))
        except Exception as e:
            print(e)
