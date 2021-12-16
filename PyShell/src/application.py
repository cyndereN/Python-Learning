import sys

from abc import ABCMeta, abstractmethod
from glob import glob
from typing import Deque


class Application(metaclass=ABCMeta):
    """Application Interface"""

    def __init__(self):
        pass

    @abstractmethod
    def exec(self, args: Deque[str], out: Deque) -> None:
        pass

    def glob(self, args: Deque[str] = []):
        globbed = []
        for arg in args:
            globbing = glob(arg)
            if globbing:
                globbed.extend(globbing)
            else:
                globbed.append(arg)
        return globbed


class UnsafeApplicationProxy(Application):
    """The proxy of Application, carry the unsafe mode"""

    def __init__(self, application: Application) -> None:
        self._application = application

    def exec(self, args: Deque[str], out: Deque) -> None:
        try:
            self._application.exec(args, out)
            self.log_access()
        except Exception as e:
            print(e, file=sys.stderr)

    def log_access(self) -> None:
        print("[Proxy: Logging unsafe mode.]", end="")
