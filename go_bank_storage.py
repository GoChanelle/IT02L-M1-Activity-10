from go_bank_account import (
    SavingsAccount,
    StudentAccount
)


USERS_FILE = "users.txt"


def account_exists(account_number):

    try:

        with open(
            USERS_FILE,
            "r"
        ) as file:

            for line in file:

                if line.startswith(
                    "Account Number:"
                ):

                    saved_number = (
                        line
                        .replace(
                            "Account Number:",
                            ""
                        )
                        .strip()
                    )

                    if saved_number == account_number:

                        return True

    except FileNotFoundError:

        return False

    return False


def save_account(account):

    with open(
        USERS_FILE,
        "a"
    ) as file:

        file.write(
            f"Account Number: "
            f"{account.account_number}\n"
        )

        file.write(
            f"Account Name: "
            f"{account.account_name}\n"
        )

        file.write(
            f"PIN: "
            f"{account.get_pin()}\n"
        )

        file.write(
            f"Account Type: "
            f"{account.get_account_type()}\n"
        )

        custom_limit = account.get_custom_withdrawal_limit()

        if custom_limit is None:

            limit_text = "None"

        else:

            limit_text = f"{custom_limit:.2f}"

        file.write(
            f"Withdrawal Limit: {limit_text}\n"
        )

        file.write(
            f"Balance: "
            f"{account.check_balance():.2f}\n\n"
        )


def load_accounts():

    accounts = []

    try:

        with open(
            USERS_FILE,
            "r"
        ) as file:

            lines = file.readlines()

    except FileNotFoundError:

        return accounts

    current = {}

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("Account Number:"):

            current["account_number"] = (
                line
                .replace(
                    "Account Number:",
                    ""
                )
                .strip()
            )

        elif line.startswith("Account Name:"):

            current["account_name"] = (
                line
                .replace(
                    "Account Name:",
                    ""
                )
                .strip()
            )

        elif line.startswith("PIN:"):

            current["pin"] = (
                line
                .replace(
                    "PIN:",
                    ""
                )
                .strip()
            )

        elif line.startswith("Account Type:"):

            current["account_type"] = (
                line
                .replace(
                    "Account Type:",
                    ""
                )
                .strip()
            )

        elif line.startswith("Withdrawal Limit:"):

            limit_text = (
                line
                .replace(
                    "Withdrawal Limit:",
                    ""
                )
                .strip()
            )

            if limit_text == "None":

                current["withdrawal_limit"] = None

            else:

                current["withdrawal_limit"] = float(
                    limit_text
                )

        elif line.startswith("Balance:"):

            balance_text = (
                line
                .replace(
                    "Balance:",
                    ""
                )
                .strip()
            )

            current["balance"] = float(
                balance_text
            )

            if (
                "account_number" in current
                and
                "account_name" in current
                and
                "pin" in current
                and
                "account_type" in current
            ):

                if (
                    current["account_type"]
                    == "Savings Account"
                ):

                    account = SavingsAccount(
                        current["account_number"],
                        current["account_name"],
                        current["pin"],
                        current["balance"]
                    )

                else:

                    account = StudentAccount(
                        current["account_number"],
                        current["account_name"],
                        current["pin"],
                        current["balance"]
                    )

                accounts.append(account)

                # Backward compatible: old users.txt records
                # without a "Withdrawal Limit:" line just leave
                # this as None, which is already the default.
                account.set_withdrawal_limit(
                    current.get(
                        "withdrawal_limit",
                        None
                    )
                )

            current = {}

    return accounts


def find_account(account_number):

    accounts = load_accounts()

    for account in accounts:

        if (
            account.account_number
            == account_number
        ):

            return account

    return None


def update_account(account):

    accounts = load_accounts()

    with open(
        USERS_FILE,
        "w"
    ) as file:

        for saved_account in accounts:

            if (
                saved_account.account_number
                == account.account_number
            ):

                # Encapsulation
                # Goes through the account's own setter instead of
                # writing to saved_account._balance directly, so the
                # account class stays in control of its own data.
                saved_account.set_balance(
                    account.check_balance()
                )

                saved_account.set_withdrawal_limit(
                    account.get_custom_withdrawal_limit()
                )

            file.write(
                f"Account Number: "
                f"{saved_account.account_number}\n"
            )

            file.write(
                f"Account Name: "
                f"{saved_account.account_name}\n"
            )

            file.write(
                f"PIN: "
                f"{saved_account.get_pin()}\n"
            )

            file.write(
                f"Account Type: "
                f"{saved_account.get_account_type()}\n"
            )

            custom_limit = (
                saved_account
                .get_custom_withdrawal_limit()
            )

            if custom_limit is None:

                limit_text = "None"

            else:

                limit_text = f"{custom_limit:.2f}"

            file.write(
                f"Withdrawal Limit: {limit_text}\n"
            )

            file.write(
                f"Balance: "
                f"{saved_account.check_balance():.2f}\n\n"
            )