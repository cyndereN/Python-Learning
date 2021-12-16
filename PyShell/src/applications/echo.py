from typing import Deque

from application import Application


class Echo(Application):
    """Prints its arguments separated by spaces
    and followed by a newline to stdout"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        args = self.glob(args)
        out.append(" ".join(args) + "\n")
