from abc import ABC, abstractmethod


class BankAccount(ABC):

    def __init__(
        self,
        account_number,
        name,
        pin,
        starting_balance
    ):
        self.account_number = account_number
        self.account_name = name

        # Encapsulation
        self._pin = pin
        self._balance = starting_balance

        # Encapsulation
        self._custom_withdrawal_limit = None

    # Encapsulation
    def check_balance(self):
        return self._balance

    # Encapsulation
    def set_balance(self, balance):

        if balance < 0:
            return False

        self._balance = balance

        return True

    # Encapsulation
    def set_withdrawal_limit(self, limit):

        if limit is not None and limit <= 0:
            return False

        self._custom_withdrawal_limit = limit

        return True

    # Encapsulation
    def get_custom_withdrawal_limit(self):

        return self._custom_withdrawal_limit

    # Encapsulation
    def clear_withdrawal_limit(self):

        self._custom_withdrawal_limit = None

    # Abstraction
    def get_effective_withdrawal_limit(self):

        type_limit = self.get_withdrawal_limit()
        custom_limit = self._custom_withdrawal_limit

        if type_limit is None:
            return custom_limit

        if custom_limit is None:
            return type_limit

        return min(type_limit, custom_limit)

    def deposit(self, amount):

        if amount <= 0:
            return False

        self._balance += amount

        return True

    def withdraw(self, amount):

        if amount <= 0:
            return False

        # Abstraction
        withdrawal_limit = self.get_effective_withdrawal_limit()

        if (
            withdrawal_limit is not None
            and
            amount > withdrawal_limit
        ):
            return False

        if amount > self._balance:
            return False

        remaining_balance = self._balance - amount

        if remaining_balance < self.get_minimum_balance():
            return False

        self._balance = remaining_balance

        return True

    def verify_pin(self, pin):

        return self._pin == pin

    # Used by storage when the account
    # needs to be saved.
    def get_pin(self):

        return self._pin

    # Abstraction
    @abstractmethod
    def get_account_type(self):
        pass

    # Abstraction
    def get_minimum_balance(self):

        return 0

    # Abstraction
    def get_withdrawal_limit(self):

        return None


# Inheritance
class SavingsAccount(BankAccount):

    MINIMUM_BALANCE = 500.00

    # Polymorphism
    def get_account_type(self):

        return "Savings Account"

    # Polymorphism
    def get_minimum_balance(self):

        return SavingsAccount.MINIMUM_BALANCE


# Inheritance
class StudentAccount(BankAccount):

    WITHDRAWAL_LIMIT = 3000.00

    # Polymorphism
    def get_account_type(self):

        return "Student Account"

    # Polymorphism
    def get_withdrawal_limit(self):

        return StudentAccount.WITHDRAWAL_LIMIT