from applications import *
from application import Application, UnsafeApplicationProxy


class ApplicationFactory:
    def __init__(self) -> None:
        pass

    def create_application(
        self, application_name: str, unsafe: bool = False
    ) -> Application:
        return self.__get_application(application_name, unsafe)

    def __get_application(self, application_name, unsafe):
        applications = {
            "pwd": pwd.Pwd,
            "cd": cd.Cd,
            "echo": echo.Echo,
            "ls": ls.Ls,
            "cat": cat.Cat,
            "head": head.Head,
            "tail": tail.Tail,
            "grep": grep.Grep,
            "cut": cut.Cut,
            "find": find.Find,
            "uniq": uniq.Uniq,
            "sort": sort.Sort,
            "exit": exit.Exit,
            "cls": cls.Cls,
        }
        if application_name not in applications.keys():
            raise ValueError(f"unsupported application {application_name}")
        application = applications[application_name]()
        if unsafe:
            return UnsafeApplicationProxy(application)
        else:
            return application
