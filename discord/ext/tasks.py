class Loop:
    def __init__(self, func, *args, **kwargs):
        self.func = func
    def start(self, *args, **kwargs):
        pass
    def before_loop(self, func):
        return func

def loop(*args, **kwargs):
    def decorator(func):
        return Loop(func)
    return decorator
