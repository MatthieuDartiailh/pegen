def f():
    pass

def f() -> None:
    pass

def f(a):
    pass

def f(a: int) -> Tuple[int, ...]:
    pass

def f(a: int = 1) -> Tuple[int, ...]:
    pass

def f(a, b: int):
    pass

def f(a, /, b):
    pass

def f(a, *, b):
    pass

def f(*, b):
    pass

def f(*args):
    pass

def f(**kwargs):
    pass

def f(a, **kwargs):
    pass
