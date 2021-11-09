class A:
    def exec(self):
        raise Exception("A")

class Unsafe:  #decorator pattern
    def __init__(self, app):
        self.app = app
    def exec(self):
        try:
            self.app.exec()
        except Exception as e:
            print(e.args[0])

class B:
    def exec(self):
        raise Exception("B")

seq = [Unsafe(B()), Unsafe(A())]

try:
    for a in seq:
        a.exec()
except Exception as e:
    print(e.args[0])