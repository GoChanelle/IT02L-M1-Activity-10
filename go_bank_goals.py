from abc import ABC, abstractmethod
 
 
class SavingsGoal(ABC):
 
    def __init__(
        self,
        name,
        target_amount
    ):
        # Encapsulation
        self._name = name
        self._target_amount = target_amount
 
    # Encapsulation
    def get_name(self):
 
        return self._name
 
    # Encapsulation
    def get_target_amount(self):
 
        return self._target_amount
 
    # Encapsulation
    def set_target_amount(self, target_amount):
 
        if target_amount <= 0:
            return False
 
        self._target_amount = target_amount
 
        return True
 
    # Abstraction
    def get_progress_percentage(self, current_balance):
 
        if self._target_amount <= 0:
            return 0.0
 
        percentage = (
            current_balance
            /
            self._target_amount
        ) * 100
 
        return min(percentage, 100.0)
 
    # Abstraction
    def is_reached(self, current_balance):
 
        return current_balance >= self._target_amount
 
    # Abstraction
    @abstractmethod
    def get_goal_type(self):
        pass
 
    # Abstraction
    @abstractmethod
    def get_congratulation_message(self):
        pass
 
 
# Inheritance
class GeneralSavingsGoal(SavingsGoal):
 
    # Polymorphism
    def get_goal_type(self):
 
        return "General Savings Goal"
 
    # Polymorphism
    def get_congratulation_message(self):
 
        return (
            f"Congratulations .ᐟ You've reached your "
            f"\"{self._name}\" savings goal .ᐟ"
        )
 
 
# Inheritance
class EmergencyFundGoal(SavingsGoal):
 
    # Polymorphism
    def get_goal_type(self):
 
        return "Emergency Fund Goal"
 
    # Polymorphism
    def get_congratulation_message(self):
 
        return (
            f"Well done .ᐟ Your emergency fund "
            f"\"{self._name}\" is now fully funded."
        )