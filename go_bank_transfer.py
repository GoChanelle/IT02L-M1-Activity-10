import go_bank_storage
import go_bank_transactions
import go_bank_utils
 
 
def transfer_funds(
    sender_account,
    recipient_account_number,
    amount
):
 
    recipient_account_number = (
        recipient_account_number.strip()
    )
 
    if recipient_account_number == "":
 
        return False, "Please enter a recipient account number."
 
    if (
        recipient_account_number
        == sender_account.account_number
    ):
 
        return False, "You can't transfer to your own account."
 
    if not go_bank_utils.is_valid_amount(amount):
 
        return False, "Please enter a valid amount."
 
    recipient_account = go_bank_storage.find_account(
        recipient_account_number
    )
 
    if recipient_account is None:
 
        return False, "Recipient account not found."
 
    # Encapsulation / Polymorphism
    withdrawn = sender_account.withdraw(amount)
 
    if not withdrawn:
 
        return False, (
            "Transfer failed: insufficient balance "
            "or account limit reached."
        )
 
    recipient_account.deposit(amount)
 
    go_bank_storage.update_account(
        sender_account
    )
 
    go_bank_storage.update_account(
        recipient_account
    )
 
    go_bank_transactions.record_transaction(
        sender_account,
        f"Transfer Sent to {recipient_account.account_number}",
        amount
    )
 
    go_bank_transactions.record_transaction(
        recipient_account,
        f"Transfer Received from {sender_account.account_number}",
        amount
    )
 
    return True, (
        f"{go_bank_utils.format_currency(amount)} sent to "
        f"{recipient_account.account_name}."
    )