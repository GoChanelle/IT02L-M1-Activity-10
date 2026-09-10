from go_bank_goals import (
    GeneralSavingsGoal,
    EmergencyFundGoal
)
 
 
GOALS_FILE = "goals.txt"
 
 
def _build_goal(
    goal_type,
    name,
    target_amount
):
 
    if goal_type == "Emergency Fund Goal":
 
        return EmergencyFundGoal(
            name,
            target_amount
        )
 
    return GeneralSavingsGoal(
        name,
        target_amount
    )
 
 
def _load_all_records():
 
    records = {}
 
    try:
 
        with open(
            GOALS_FILE,
            "r"
        ) as file:
 
            lines = file.readlines()
 
    except FileNotFoundError:
 
        return records
 
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
 
        elif stripped.startswith("Goal Name:"):
 
            current["name"] = (
                stripped
                .replace("Goal Name:", "")
                .strip()
            )
 
        elif stripped.startswith("Goal Type:"):
 
            current["goal_type"] = (
                stripped
                .replace("Goal Type:", "")
                .strip()
            )
 
        elif stripped.startswith("Target Amount:"):
 
            current["target_amount"] = float(
                stripped
                .replace("Target Amount:", "")
                .strip()
            )
 
            records[
                current["account_number"]
            ] = current.copy()
 
            current = {}
 
    return records
 
 
def _write_all_records(records):
 
    with open(
        GOALS_FILE,
        "w"
    ) as file:
 
        for account_number, record in records.items():
 
            file.write(
                f"Account Number: {account_number}\n"
            )
 
            file.write(
                f"Goal Name: {record['name']}\n"
            )
 
            file.write(
                f"Goal Type: {record['goal_type']}\n"
            )
 
            file.write(
                f"Target Amount: "
                f"{record['target_amount']:.2f}\n\n"
            )
 
 
def save_goal(
    account_number,
    goal
):
 
    records = _load_all_records()
 
    records[account_number] = {
        "account_number": account_number,
        "name": goal.get_name(),
        "goal_type": goal.get_goal_type(),
        "target_amount": goal.get_target_amount()
    }
 
    _write_all_records(records)
 
 
def get_goal(account_number):
 
    records = _load_all_records()
 
    record = records.get(account_number)
 
    if record is None:
        return None
 
    return _build_goal(
        record["goal_type"],
        record["name"],
        record["target_amount"]
    )
 
 
def clear_goal(account_number):
 
    records = _load_all_records()
 
    if account_number in records:
 
        del records[account_number]
 
        _write_all_records(records)