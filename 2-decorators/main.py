""" Декоратор ф-ции """
from functools import wraps


def limit_args(max_value, mode):
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if arg > max_value:
                    if mode == "error":
                        raise ValueError(
                            f"Аргумент {arg} превышает максимальное значение {max_value}")
                    elif mode == "clip":
                        list_args = list(args)
                        index_list_args = list_args.index(arg)
                        list_args[index_list_args] = max_value
                        return func(*list_args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return dec


@limit_args(max_value=10, mode="clip")
def multiply(a, b):
    return a * b


multiply(2, 3)
multiply(100, 3)
