""" Модуль Cache """
from typing import Generic, Optional, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Cache(Generic[T, R]):
    """ generic-класс кэша """
    cache: dict[T, R]

    def __init__(self) -> None:
        self.cache = {}

    def set(self, key: T, value: R):
        """ Добавляет новый элемент в словарь """
        self.cache[key] = value

    def get(self, key: T) -> Optional[R]:
        """ Возвращает значение по ключу или None """
        return self.cache.get(key)

    def keys(self) -> list[T]:
        """ Возвращает все ключи """
        return list(self.cache.keys())

    def values(self) -> list[R]:
        """ Возвращает все значения """
        return list(self.cache.values())


hits = Cache[str, int]()
hits.set("home", 10)
hits.set("about", 3)
x = hits.get("home")        # x: int | None
paths = hits.keys()         # list[str]
counts = hits.values()      # list[int]
