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
    def check_balance(self):
        return self._balance

    def deposit(self, amount):

        if amount <= 0:
            return False

        self._balance += amount

        return True

    def withdraw(self, amount):

        # Abstraction
        # Asks the account for its own rules through these two
        # methods and enforces whatever comes back. 
        withdrawal_limit = self.get_withdrawal_limit()
 
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

        if amount <= 0:
            return False

        if amount > self._balance:
            return False

        self._balance -= amount

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


# Inheritance
class SavingsAccount(BankAccount):

    # Polymorphism
    def get_account_type(self):

        return "Savings Account"


# Inheritance
class StudentAccount(BankAccount):

    # Polymorphism
    def get_account_type(self):

        return "Student Account"