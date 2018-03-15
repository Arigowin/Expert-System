class ReturnValue(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value


def enable_ret(func):
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ReturnValue as exc:
            return exc.value
    return decorated_func


def ret(value):
    raise ReturnValue(value)
