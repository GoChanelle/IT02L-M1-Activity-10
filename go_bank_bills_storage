from go_bank_bills import (
    UtilityBill,
    SubscriptionBill
)
 
 
BILLS_FILE = "bills.txt"
 
 
def _build_bill(bill_type, name, amount, paid):
 
    if bill_type == "Subscription Bill":
 
        bill = SubscriptionBill(name, amount)
 
    else:
 
        bill = UtilityBill(name, amount)
 
    if paid:
 
        # Encapsulation
        # Uses the account's own method to flip the flag instead
        # of touching bill._paid directly.
        bill.mark_as_paid()
 
    return bill
 
 
def add_bill(
    account_number,
    bill
):
 
    with open(
        BILLS_FILE,
        "a"
    ) as file:
 
        file.write(
            f"Account Number: {account_number}\n"
        )
 
        file.write(
            f"Bill Name: {bill.get_name()}\n"
        )
 
        file.write(
            f"Bill Type: {bill.get_bill_type()}\n"
        )
 
        file.write(
            f"Amount: {bill.get_amount():.2f}\n"
        )
 
        file.write(
            f"Paid: {bill.is_paid()}\n\n"
        )
 
 
def get_bills(account_number):
 
    bills = []
 
    try:
 
        with open(
            BILLS_FILE,
            "r"
        ) as file:
 
            lines = file.readlines()
 
    except FileNotFoundError:
 
        return bills
 
    current = {}
 
    for line in lines:
 
        line = line.strip()
 
        if not line:
            continue
 
        if line.startswith("Account Number:"):
 
            current["account_number"] = (
                line
                .replace("Account Number:", "")
                .strip()
            )
 
        elif line.startswith("Bill Name:"):
 
            current["name"] = (
                line
                .replace("Bill Name:", "")
                .strip()
            )
 
        elif line.startswith("Bill Type:"):
 
            current["bill_type"] = (
                line
                .replace("Bill Type:", "")
                .strip()
            )
 
        elif line.startswith("Amount:"):
 
            current["amount"] = float(
                line
                .replace("Amount:", "")
                .strip()
            )
 
        elif line.startswith("Paid:"):
 
            paid_text = (
                line
                .replace("Paid:", "")
                .strip()
            )
 
            current["paid"] = (
                paid_text == "True"
            )
 
            if current.get(
                "account_number"
            ) == account_number:
 
                bills.append(
                    _build_bill(
                        current["bill_type"],
                        current["name"],
                        current["amount"],
                        current["paid"]
                    )
                )
 
            current = {}
 
    return bills
 
 
def mark_bill_paid(
    account_number,
    bill_name
):
 
    all_bills_raw = []
 
    try:
 
        with open(
            BILLS_FILE,
            "r"
        ) as file:
 
            lines = file.readlines()
 
    except FileNotFoundError:
 
        return
 
    current = {}
 
    for line in lines:
 
        stripped = line.strip()
 
        if not stripped:
            continue
 
        if stripped.startswith("Account Number:"):
 
            current["account_number"] = (
                stripped
                .replace("Account Number:", "")
                .strip()
            )
 
        elif stripped.startswith("Bill Name:"):
 
            current["name"] = (
                stripped
                .replace("Bill Name:", "")
                .strip()
            )
 
        elif stripped.startswith("Bill Type:"):
 
            current["bill_type"] = (
                stripped
                .replace("Bill Type:", "")
                .strip()
            )
 
        elif stripped.startswith("Amount:"):
 
            current["amount"] = float(
                stripped
                .replace("Amount:", "")
                .strip()
            )
 
        elif stripped.startswith("Paid:"):
 
            paid_text = (
                stripped
                .replace("Paid:", "")
                .strip()
            )
 
            current["paid"] = (
                paid_text == "True"
            )
 
            if (
                current.get("account_number")
                == account_number
                and
                current.get("name")
                == bill_name
            ):
 
                current["paid"] = True
 
            all_bills_raw.append(
                current.copy()
            )
 
            current = {}
 
    with open(
        BILLS_FILE,
        "w"
    ) as file:
 
        for record in all_bills_raw:
 
            file.write(
                f"Account Number: "
                f"{record['account_number']}\n"
            )
 
            file.write(
                f"Bill Name: {record['name']}\n"
            )
 
            file.write(
                f"Bill Type: {record['bill_type']}\n"
            )
 
            file.write(
                f"Amount: {record['amount']:.2f}\n"
            )
 
            file.write(
                f"Paid: {record['paid']}\n\n"
            )