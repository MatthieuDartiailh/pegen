@d
def f():
    pass


@d()
def f():
    pass


@d(a)
def f():
    pass


@d
class A:
    pass
