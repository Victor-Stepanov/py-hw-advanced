from dataclasses import dataclass
from collections import defaultdict
from typing import Protocol


@dataclass(frozen=True)
class Student:
    """
    Представляет ученика.
    """

    id: int
    name: str


@dataclass(frozen=True)
class Subject:
    """
    Представляет учебный предмет.
    """

    id: int
    title: str


@dataclass(frozen=True)
class Grade:
    """
    Представляет оценку ученика по предмету.
    """

    student_id: int
    subject_id: int
    value: float


class Notifier(Protocol):
    """
    Интерфейс сервиса уведомлений.
    """

    def notify(self, message: str) -> None:
        """
        Отправляет уведомление.

        Args:
            message: Текст уведомления.
        """
        ...


class ConsoleNotifier:
    """
    Реализация уведомителя через консольный вывод.
    """

    def notify(self, message: str) -> None:
        """
        Выводит сообщение в консоль.

        Args:
            message: Текст уведомления.
        """
        print(message)


class JournalRepository(Protocol):
    """
    Абстракция хранилища данных журнала.
    """

    def get_students(self) -> list[Student]:
        """
        Возвращает список учеников.
        """
        ...

    def get_subjects(self) -> list[Subject]:
        """
        Возвращает список предметов.
        """
        ...

    def get_grades(self) -> list[Grade]:
        """
        Возвращает список оценок.
        """
        ...

    def add_student(self, student: Student) -> None:
        """
        Добавляет ученика.

        Args:
            student: Добавляемый ученик.
        """
        ...

    def add_subject(self, subject: Subject) -> None:
        """
        Добавляет предмет.

        Args:
            subject: Добавляемый предмет.
        """
        ...

    def add_grade(self, grade: Grade) -> None:
        """
        Добавляет оценку.

        Args:
            grade: Добавляемая оценка.
        """
        ...


class Journal(JournalRepository):
    """
    Хранилище учеников, предметов и оценок.
    """

    def __init__(self) -> None:
        """
        Инициализирует пустой журнал.
        """
        self._students: dict[int, Student] = {}
        self._subjects: dict[int, Subject] = {}
        self._grades: list[Grade] = []

    def add_student(self, student: Student) -> None:
        """
        Добавляет ученика в журнал.

        Args:
            student: Объект ученика.
        """
        self._students[student.id] = student

    def add_subject(self, subject: Subject) -> None:
        """
        Добавляет предмет в журнал.

        Args:
            subject: Объект предмета.
        """
        self._subjects[subject.id] = subject

    def add_grade(self, grade: Grade) -> None:
        """
        Добавляет оценку в журнал.

        Args:
            grade: Объект оценки.
        """
        self._grades.append(grade)

    def get_students(self) -> list[Student]:
        """
        Возвращает список учеников.

        Returns:
            Список объектов Student.
        """
        return list(self._students.values())

    def get_subjects(self) -> list[Subject]:
        """
        Возвращает список предметов.

        Returns:
            Список объектов Subject.
        """
        return list(self._subjects.values())

    def get_grades(self) -> list[Grade]:
        """
        Возвращает список оценок.

        Returns:
            Список объектов Grade.
        """
        return self._grades.copy()


class StatisticsService:
    """
    Сервис расчёта статистики по оценкам.
    """

    def __init__(self, repository: JournalRepository) -> None:
        """
        Инициализирует сервис статистики.

        Args:
            repository: Репозиторий данных журнала.
        """
        self.repository = repository

    @staticmethod
    def _calculate_average(
        groups: dict[int, list[float]]
    ) -> dict[int, float]:
        """
        Вычисляет среднее значение для каждой группы.

        Args:
            groups: Словарь групп оценок.

        Returns:
            Словарь средних значений.
        """
        return {
            key: sum(values) / len(values)
            for key, values in groups.items()
        }

    def average_by_student(self) -> dict[str, float]:
        """
        Вычисляет средний балл каждого ученика.

        Returns:
            Словарь вида {имя_ученика: средний_балл}.
        """
        grouped: dict[int, list[float]] = defaultdict(list)

        for grade in self.repository.get_grades():
            grouped[grade.student_id].append(grade.value)

        averages = self._calculate_average(grouped)

        return {
            student.name: averages.get(student.id, 0.0)
            for student in self.repository.get_students()
        }

    def average_by_subject(self) -> dict[str, float]:
        """
        Вычисляет средний балл по каждому предмету.

        Returns:
            Словарь вида {название_предмета: средний_балл}.
        """
        grouped: dict[int, list[float]] = defaultdict(list)

        for grade in self.repository.get_grades():
            grouped[grade.subject_id].append(grade.value)

        averages = self._calculate_average(grouped)

        return {
            subject.title: averages.get(subject.id, 0.0)
            for subject in self.repository.get_subjects()
        }


class GradeMonitor:
    """
    Контролирует успеваемость учеников и отправляет уведомления.
    """

    def __init__(
        self,
        statistics: StatisticsService,
        notifier: Notifier,
        threshold: float = 3.5,
    ) -> None:
        """
        Инициализирует монитор успеваемости.

        Args:
            statistics: Сервис статистики.
            notifier: Сервис уведомлений.
            threshold: Порог среднего балла.
        """
        self.statistics = statistics
        self.notifier = notifier
        self.threshold = threshold

    def check_students(self) -> None:
        """
        Проверяет средний балл учеников и отправляет уведомления
        при значении ниже установленного порога.
        """
        for name, average in self.statistics.average_by_student().items():
            if average < self.threshold:
                self.notifier.notify(
                    f"Ученик {name}: "
                    f"средний балл {average:.2f} "
                    f"ниже {self.threshold}"
                )


class SchoolService:
    """
    Фасад для работы со школьным журналом.
    """

    def __init__(
        self,
        repository: JournalRepository,
        monitor: GradeMonitor,
    ) -> None:
        """
        Инициализирует сервис школы.

        Args:
            repository: Репозиторий журнала.
            monitor: Монитор успеваемости.
        """
        self.repository = repository
        self.monitor = monitor

    def add_grade(self, grade: Grade) -> None:
        """
        Добавляет оценку и запускает проверку успеваемости.

        Args:
            grade: Добавляемая оценка.
        """
        self.repository.add_grade(grade)
        self.monitor.check_students()
