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
        # A user-set personal limit, separate from the account
        # type's built-in rule. None means "no personal limit set".
        self._custom_withdrawal_limit = None

    # Encapsulation
    def check_balance(self):
        return self._balance

    # Encapsulation
    # This is the ONLY way outside code (like the storage module)
    # is allowed to change the balance directly. Before this method
    # existed, go_bank_storage.py reached into `_balance` directly,
    # which broke encapsulation because it let another module edit
    # a "private" attribute without going through any checks.
    def set_balance(self, balance):

        if balance < 0:
            return False

        self._balance = balance

        return True

    # Encapsulation
    # Lets the account holder set their own, stricter withdrawal
    # cap. Passing None clears it. Rejects zero/negative limits so
    # someone can't accidentally lock themselves out completely.
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
    # Combines the account type's built-in rule (polymorphic, via
    # get_withdrawal_limit()) with the holder's own personal limit,
    # and returns whichever is stricter. withdraw() only ever calls
    # this — it never has to know both limits exist separately.
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
        # The base class doesn't know or care WHICH account type
        # has a withdrawal limit or a minimum balance rule. It just
        # asks the account for its own rules through these two
        # methods and enforces whatever comes back. Each subclass
        # fills in the details on its own (see get_minimum_balance
        # and get_withdrawal_limit below).
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
    # Default policy: no required minimum balance. Subclasses that
    # need one (like SavingsAccount) override this.
    def get_minimum_balance(self):

        return 0

    # Abstraction
    # Default policy: no cap on a single withdrawal. Subclasses
    # that need one (like StudentAccount) override this.
    def get_withdrawal_limit(self):

        return None


# Inheritance
class SavingsAccount(BankAccount):

    MINIMUM_BALANCE = 500.00

    # Polymorphism
    def get_account_type(self):

        return "Savings Account"

    # Polymorphism
    # Overrides the base class's "no minimum" policy. A savings
    # account can never be withdrawn from below ₱500.
    def get_minimum_balance(self):

        return SavingsAccount.MINIMUM_BALANCE


# Inheritance
class StudentAccount(BankAccount):

    WITHDRAWAL_LIMIT = 3000.00

    # Polymorphism
    def get_account_type(self):

        return "Student Account"

    # Polymorphism
    # Overrides the base class's "no limit" policy. A student
    # account can withdraw at most ₱3,000 in a single transaction.
    def get_withdrawal_limit(self):

        return StudentAccount.WITHDRAWAL_LIMIT