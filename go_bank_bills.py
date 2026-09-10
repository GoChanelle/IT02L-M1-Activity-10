from abc import ABC, abstractmethod
 
 
class Bill(ABC):
 
    def __init__(
        self,
        name,
        amount
    ):
        # Encapsulation
        self._name = name
        self._amount = amount
        self._paid = False
 
    # Encapsulation
    def get_name(self):
 
        return self._name
 
    # Encapsulation
    def get_amount(self):
 
        return self._amount
 
    # Encapsulation
    def is_paid(self):
 
        return self._paid
 
    # Encapsulation
    # The only way outside code can flip a bill to "paid" — nothing
    # outside this class ever writes to _paid directly.
    def mark_as_paid(self):
 
        self._paid = True
 
    # Abstraction
    @abstractmethod
    def get_bill_type(self):
        pass
 
    # Abstraction
    # Default policy: no processing fee. Subclasses that charge one
    # (like SubscriptionBill) override this.
    def get_processing_fee(self):
 
        return 0.0
 
    # Abstraction
    def get_total_due(self):
 
        return (
            self._amount
            +
            self.get_processing_fee()
        )
 
 
# Inheritance
class UtilityBill(Bill):
 
    # Polymorphism
    def get_bill_type(self):
 
        return "Utility Bill"
 
 
# Inheritance
class SubscriptionBill(Bill):
 
    PROCESSING_FEE_RATE = 0.02
 
    # Polymorphism
    def get_bill_type(self):
 
        return "Subscription Bill"
 
    # Polymorphism
    def get_processing_fee(self):
 
        return round(
            self._amount
            *
            SubscriptionBill.PROCESSING_FEE_RATE,
            2
        )
 