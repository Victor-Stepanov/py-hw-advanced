class BankAccount:
    __number_of_accounts: int = 0

    def __init__(self, user_name: str,
                 account_number: str | int,
                 balance: int | float = 0) -> None:
        self._validate_user_data(user_name, account_number, balance)

        self.user_name = user_name
        self.account_number = str(account_number)
        self.balance = balance

        type(self).__number_of_accounts += 1

    @staticmethod
    def _validate_user_data(user_name: str,
                            account_number: str | int,
                            balance: int | float) -> None:
        """Комплексная валидация данных пользователя."""
        BankAccount._validate_user_name(user_name)
        BankAccount._validate_account_number(account_number)
        BankAccount._validate_initial_balance(balance)

    @staticmethod
    def _validate_user_name(user_name: str) -> None:
        if not user_name.strip():
            raise ValueError("Имя владельца не может быть пустым")

    @staticmethod
    def _validate_account_number(account_number: str | int) -> None:
        if isinstance(account_number, str) and not account_number.strip():
            raise ValueError("Номер счета не может быть пустой строкой")

    @staticmethod
    def _validate_initial_balance(balance: int | float) -> None:
        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")

    def _validate_amount(self, amount: int | float,
                         operation_name: str = "операции") -> None:
        """Валидация суммы для операций."""
        if amount <= 0:
            raise ValueError(
                f"Сумма для {operation_name} должна быть больше 0")

    def _check_sufficient_funds(self, amount: int | float,
                                operation: str = "операции") -> None:
        """Проверка достаточности средств."""
        if self.balance - amount < 0:
            raise ValueError(f"Недостаточно средств для {operation}. ")

    @classmethod
    def get_accounts_created(cls) -> int:
        return cls.__number_of_accounts

    def info(self) -> str:
        return (f"Владелец счета: {self.user_name}\n"
                f"Номер счета: {self.account_number}\n"
                f"Баланс: {self.balance:.2f}")

    def deposit(self, amount: int | float) -> float:
        self._validate_amount(amount, "пополнения")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: int | float) -> float:
        self._validate_amount(amount, "снятия")
        self._check_sufficient_funds(amount, "снятия")
        self.balance -= amount
        return self.balance

    def transfer_to(self, account: object, amount: int | float) -> float:
        if not isinstance(account, BankAccount):
            raise TypeError("Перевод возможен только на счета BankAccount")

        if self is account:
            raise ValueError("Нельзя переводить средства на свой же счет")

        self._validate_amount(amount, "перевода")
        self._check_sufficient_funds(amount, "перевода")

        self.balance -= amount
        account.balance += amount

        return self.balance


if __name__ == "__main__":
    try:
        acc1 = BankAccount("Иван Петров", "12345", 1000)
        acc2 = BankAccount("Мария Иванова", 67890, 500)

        print(acc1.info())
        print()

        new_balance = acc1.deposit(500)
        print(f"После пополнения: {new_balance}")

        new_balance = acc1.withdraw(200)
        print(f"После снятия: {new_balance}")

        new_balance = acc1.transfer_to(acc1, 300)
        print(f"После перевода: {new_balance}")

    except (TypeError, ValueError) as e:
        print(f"Ошибка: {e}")

    print(f"\nВсего создано счетов: {BankAccount.get_accounts_created()}")
