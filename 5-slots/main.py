from dataclasses import dataclass
import sys


@dataclass
class User:
    name: str
    email: str
    password: str


@dataclass(slots=True)
class SlotsUser:
    name: str
    email: str
    password: str


N = 100_000
user_list = [User("A", "a@ex.ru", "AA") for _ in range(N)]
suser_list = [SlotsUser("A", "a@ex.ru", "AA") for _ in range(N)]

user_size = (
    sys.getsizeof(user_list[0])
    + sys.getsizeof(user_list[0].__dict__)
)

slots_size = sys.getsizeof(suser_list[0])

print(f"User (с учетом __dict__): {user_size} байт")
print(f"SlotsUser: {slots_size} байт")
print(f"Разница: {user_size - slots_size} байт")
print(f"Экономия: {(1 - slots_size / user_size) * 100:.1f}%")
