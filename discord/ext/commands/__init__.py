class Bot:
    def __init__(self, command_prefix="!", intents=None):
        self.command_prefix = command_prefix
        self.intents = intents
        self._commands = {}
    def command(self, name=None, help=None):
        def decorator(func):
            cmd_name = name or func.__name__
            async def wrapper(ctx, *args, **kwargs):
                return await func(ctx, *args, **kwargs)
            self._commands[cmd_name] = wrapper
            return wrapper
        return decorator
    def event(self, func):
        setattr(self, func.__name__, func)
        return func
    def get_command(self, name):
        return self._commands.get(name)
    def add_listener(self, *args, **kwargs):
        pass
    async def run(self, *args, **kwargs):
        pass

class Cog:
    @classmethod
    def listener(cls, *dargs, **dkwargs):
        def decorator(func):
            return func
        return decorator
