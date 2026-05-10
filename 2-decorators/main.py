""" Декоратор ф-ции """
from functools import wraps


def limit_args(max_value, mode):
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            clipped_args = []
            for arg in args:
                if arg > max_value:
                    if mode == "error":
                        raise ValueError(
                            f"Аргумент {arg} превышает максимальное значение {max_value}")
                    elif mode == "clip":
                        clipped_args.append(max_value)
                else:
                    clipped_args.append(arg)

            if mode == "clip":
                return func(*clipped_args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return dec


@limit_args(max_value=10, mode="clip")
def multiply(a, b):
    return a * b


multiply(2, 3)
print(multiply(100, 200))
