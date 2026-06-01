from dataclasses import dataclass
from datetime import date


@dataclass
class Room:
    """Базовый класс комнаты"""
    room_id: int
    base_price: float

    def get_price(self) -> float:
        """Возвращает цену за ночь"""
        return self.base_price


@dataclass
class LuxuryRoom(Room):
    """Номер класса люкс с мультипликатором цены"""
    multiplier_price: float = 1.4

    def get_price(self) -> float:
        return super().get_price() * self.multiplier_price


@dataclass
class Guest:
    """Информация о госте"""
    guest_id: int
    name: str
    check_in_date: date


@dataclass
class Booking:
    """Бронирование номера"""
    booking_id: int
    guest: Guest
    room: Room
    check_in: date
    check_out: date
    is_active: bool = True

    def overlaps(self, other_check_in: date, other_check_out: date) -> bool:
        """Проверяет пересечение дат бронирования"""
        return self.check_in < other_check_out and other_check_in < self.check_out

    def cancel(self) -> None:
        """Отменяет бронирование"""
        self.is_active = False


@dataclass
class Hotel:
    """Отель с управлением номерами и бронированием"""
    rooms: list[Room]
    bookings: list[Booking]

    def add_room(self, room: Room) -> None:
        """Добавляет номер в отель"""
        self.rooms.append(room)

    def get_available_rooms(self, check_in: date, check_out: date) -> list[Room]:
        """Возвращает список доступных номеров на заданные даты"""
        available: list[Room] = []

        for room in self.rooms:
            is_available = True
            for booking in self.bookings:
                if booking.is_active and booking.room == room:
                    if booking.overlaps(check_in, check_out):
                        is_available = False
                        break
            if is_available:
                available.append(room)

        return available

    def booking_room(self, guest: Guest, room: Room, check_in: date, check_out: date) -> Booking | None:
        """Бронирует номер для гостя, если он свободен"""
        if room not in self.get_available_rooms(check_in, check_out):
            return None

        booking_id = len(self.bookings) + 1
        new_booking = Booking(
            booking_id=booking_id,
            guest=guest,
            room=room,
            check_in=check_in,
            check_out=check_out
        )
        self.bookings.append(new_booking)
        return new_booking

    def cancel_booking(self, booking_id: int) -> bool:
        """ Отменяет бронь гостя, если она существует """
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                booking.cancel()
                return True
        return False

    def get_booked_rooms(self) -> list[Booking]:
        """Возвращает список активных бронирований"""
        return [b for b in self.bookings if b.is_active]
