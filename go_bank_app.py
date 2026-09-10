import streamlit as st

import go_bank_auth
import go_bank_storage
import go_bank_transactions
import go_bank_analysis
import go_bank_utils
import go_bank_bills_storage

from go_bank_bills import (
    UtilityBill,
    SubscriptionBill
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CHANCE'S Bank",
    page_icon="🏦",
    layout="wide"
)


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "account" not in st.session_state:

    st.session_state.account = None


# ==========================================
# BANK HEADER
# ==========================================

st.markdown("""
<style>
div[data-testid="stImage"] img {
    height: 180px;
    width: 100%;
    object-fit: cover;
    object-position: center;
}
</style>
""", unsafe_allow_html=True)

st.image("https://i.pinimg.com/1200x/16/cc/5b/16cc5b65e4c313181101844c746d8532.jpg")

st.title("𖥻 ׁ ׅ  CHANCE BANK ᯓ★")

st.caption(
    "Secure Digital Banking System ⸝⸝"
)

st.divider()


# ==========================================
# LOGIN / REGISTRATION
# ==========================================

if not st.session_state.logged_in:

    login_tab, register_tab = st.tabs(
        [
            "Login",
            "Register"
        ]
    )


    # ======================================
    # LOGIN
    # ======================================

    with login_tab:

        st.subheader(
            "Welcome Back"
        )

        account_number = st.text_input(
            "Account Number",
            key="login_account"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            key="login_pin"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            account, message = (
                go_bank_auth
                .login_account(
                    account_number,
                    pin
                )
            )

            if account is not None:

                st.session_state.logged_in = True

                st.session_state.account = (
                    account
                )

                st.success(message)

                st.rerun()

            else:

                st.error(message)


    # ======================================
    # REGISTRATION
    # ======================================

    with register_tab:

        st.subheader(
            "Create Your Chance Bank Account"
        )

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        account_number = st.text_input(
            "Account Number",
            key="register_account"
        )

        pin = st.text_input(
            "Create 4-Digit PIN",
            type="password",
            key="register_pin"
        )

        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password",
            key="register_confirm_pin"
        )

        account_type = st.selectbox(
            "Account Type",
            [
                "Savings Account",
                "Student Account"
            ]
        )

        starting_balance = st.number_input(
            "Starting Balance",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            account, message = (
                go_bank_auth
                .register_account(
                    name,
                    account_number,
                    pin,
                    confirm_pin,
                    account_type,
                    starting_balance
                )
            )

            if account is not None:

                st.success(message)

                st.info(
                    "Your account has been created. "
                    "Please use the Login tab."
                )

            else:

                st.error(message)


# ==========================================
# LOGGED-IN BANKING APPLICATION
# ==========================================

else:

    account = (
        st.session_state.account
    )


    # ======================================
    # SIDEBAR
    # ======================================

    st.sidebar.title(
        "𖥻 ׁ ׅ CHANCE BANK"
    )

    st.sidebar.write(
        f"**{account.account_name}**"
    )

    st.sidebar.write(
        f"Account: "
        f"{account.account_number}"
    )

    st.sidebar.badge(
        account.get_account_type(), color="red"
    )

    st.sidebar.divider()


    if "menu" not in st.session_state:
        st.session_state.menu = "Dashboard"

    st.sidebar.title("BANKING MENU")

    options = ["Dashboard", "Deposit", "Withdraw", "Bills to Pay", "Transaction History", "Transaction Analysis"]

    for option in options:
        button_type = "primary" if st.session_state.menu == option else "secondary"
        if st.sidebar.button(option, use_container_width=True, type=button_type):
            st.session_state.menu = option

    menu = st.session_state.menu


    st.sidebar.divider()


    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.account = None

        st.rerun()


    # ======================================
    # DASHBOARD
    # ======================================

    if menu == "Dashboard":

        st.subheader(
            f"𓄲 Welcome, {account.account_name} !"
        )

        st.header(
            ":red[Account Overview]"
        )

        col1, col2, col3 = st.columns(3, border=True)


        col1.badge("Current Balance", color="red")
        col1.metric(
            "・・・・・",
            go_bank_utils
            .format_currency(
                account.check_balance()
            )
        )

        col2.badge("Account", color="red")
        col2.metric(
            "・・・・・",
            account.get_account_type()
        )

        col3.badge("Account Number", color="red")
        col3.metric(
            "・・・・・",
            account.account_number
        )


        st.divider()


        st.caption(
            "Select a banking service from the menu on the left."
        )


    # ======================================
    # DEPOSIT
    # ======================================

    elif menu == "Deposit":

        st.header(
            ":red[Deposit Money]"
        )

        st.divider()

        st.badge(
            f"Current Balance: "
            f"**{go_bank_utils.format_currency(account.check_balance())}**", color="red"
        )

        amount = st.number_input(
            "Deposit Amount:",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )


        if st.button(
            "Confirm Deposit",
            use_container_width=True
        ):

            if not go_bank_utils.is_valid_amount(
                amount
            ):

                st.error(
                    "Invalid deposit amount .ᐟ"
                )

            else:

                success = account.deposit(
                    amount
                )

                if success:
                    with st.spinner(text="Transferring amount...", show_time=False, width="content"):

                        go_bank_storage.update_account(
                            account
                        )

                        go_bank_transactions.record_transaction(
                            account,
                            "Deposit",
                            amount
                        )

                    st.success(
                        "Deposit successful .ᐟ"
                    )

                    st.metric(
                        "New Balance",
                        go_bank_utils
                        .format_currency(
                            account.check_balance()
                        )
                    )


    # ======================================
    # WITHDRAW
    # ======================================

    elif menu == "Withdraw":

        st.header(
            ":red[Withdraw Money]"
        )

        st.divider()

        st.badge(
            f"Available Balance: "
            f"**{go_bank_utils.format_currency(account.check_balance())}**", color="red"
        )

        amount = st.number_input(
            "Withdrawal Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )


        if st.button(
            "Confirm Withdrawal",
            use_container_width=True
        ):

            if not go_bank_utils.is_valid_amount(
                amount
            ):

                st.error(
                    "Invalid withdrawal amount .ᐟ"
                )

            elif amount > account.check_balance():

                st.error(
                    "Insufficient balance .ᐟ"
                )

            else:

                success = account.withdraw(
                    amount
                )

                if success:

                    with st.spinner(text="Transferring amount...", show_time=False, width="content"):
                        go_bank_storage.update_account(
                            account
                        )

                        go_bank_transactions.record_transaction(
                            account,
                            "Withdraw",
                            amount
                        )

                    st.success(
                        "Withdrawal successful .ᐟ"
                    )

                    st.metric(
                        "New Balance",
                        go_bank_utils
                        .format_currency(
                            account.check_balance()
                        )
                    )
    # ======================================
    # BILLS TO PAY
    # ======================================
 
    elif menu == "Bills to Pay":
 
        st.header(
            ":red[Bills to Pay]"
        )
 
        st.divider()
 
        st.badge(
            f"Available Balance: "
            f"**{go_bank_utils.format_currency(account.check_balance())}**", color="red"
        )
 
 
        # ==================================
        # ADD A NEW BILL
        # ==================================
 
        st.subheader(
            "Add a Bill"
        )
 
        bill_name = st.text_input(
            "What are you paying for?",
            key="bill_name"
        )
 
        bill_amount = st.number_input(
            "Amount Due",
            min_value=0.0,
            step=50.0,
            format="%.2f",
            key="bill_amount"
        )
 
        bill_type = st.selectbox(
            "Bill Type",
            [
                "Utility Bill",
                "Subscription Bill"
            ],
            key="bill_type"
        )
 
        if st.button(
            "Add to List",
            use_container_width=True
        ):
 
            if bill_name.strip() == "":
 
                st.error(
                    "Please enter what this bill is for."
                )
 
            elif not go_bank_utils.is_valid_amount(
                bill_amount
            ):
 
                st.error(
                    "Please enter a valid amount."
                )
 
            else:
 
                if bill_type == "Subscription Bill":
 
                    new_bill = SubscriptionBill(
                        bill_name.strip(),
                        bill_amount
                    )
 
                else:
 
                    new_bill = UtilityBill(
                        bill_name.strip(),
                        bill_amount
                    )
 
                go_bank_bills_storage.add_bill(
                    account.account_number,
                    new_bill
                )
 
                st.success(
                    f"Added \"{bill_name.strip()}\" to your bills."
                )
 
                st.rerun()
 
 
        st.divider()
 
 
        # ==================================
        # LIST OF UNPAID BILLS
        # ==================================
 
        st.subheader(
            "Pending Bills"
        )
 
        bills = go_bank_bills_storage.get_bills(
            account.account_number
        )
 
        unpaid_bills = [
            bill
            for bill in bills
            if not bill.is_paid()
        ]
 
        if not unpaid_bills:
 
            st.caption(
                "You have no pending bills."
            )
 
        else:
 
            for bill in unpaid_bills:
 
                col1, col2, col3, col4 = st.columns(
                    [3, 2, 2, 2],
                    border=True
                )
 
                col1.write(
                    f"**{bill.get_name()}**"
                )
 
                col1.caption(
                    bill.get_bill_type()
                )
 
                col2.metric(
                    "Amount",
                    go_bank_utils.format_currency(
                        bill.get_amount()
                    )
                )
 
                # Polymorphism
                # get_total_due() calls the bill's own
                # get_processing_fee() under the hood, so this
                # screen doesn't need an if/else for bill type.
                col3.metric(
                    "Total Due",
                    go_bank_utils.format_currency(
                        bill.get_total_due()
                    )
                )
 
                if col4.button(
                    "Pay",
                    key=f"pay_{bill.get_name()}",
                    use_container_width=True
                ):
 
                    total_due = bill.get_total_due()
 
                    if total_due > account.check_balance():
 
                        st.error(
                            "Insufficient balance to pay this bill."
                        )
 
                    else:
 
                        success = account.withdraw(
                            total_due
                        )
 
                        if success:
 
                            with st.spinner(text="Processing payment...", show_time=False, width="content"):
 
                                go_bank_storage.update_account(
                                    account
                                )
 
                                go_bank_bills_storage.mark_bill_paid(
                                    account.account_number,
                                    bill.get_name()
                                )
 
                                go_bank_transactions.record_transaction(
                                    account,
                                    f"Bill Payment: {bill.get_name()}",
                                    total_due
                                )
 
                            st.success(
                                f"Paid {bill.get_name()} successfully."
                            )
 
                            st.rerun()
 
                        else:
 
                            st.error(
                                "Payment failed. Check your account "
                                "limits or balance."
                            )

    # ======================================
    # TRANSACTION HISTORY
    # ======================================

    elif menu == "Transaction History":

        st.header(
            ":red[Transaction History]"
        )

        st.divider()

        transactions = (
            go_bank_transactions
            .get_transactions()
        )


        # Show only transactions
        # belonging to the logged-in user.

        transactions = [
            transaction
            for transaction in transactions
            if transaction.get(
                "account_number"
            ) == account.account_number
        ]


        if transactions:

            display_data = []

            for transaction in transactions:

                display_data.append({

                    "Timestamp":
                        transaction.get(
                            "timestamp",
                            "N/A"
                        ),

                    "Transaction":
                        transaction.get(
                            "transaction",
                            "N/A"
                        ),

                    "Amount":
                        go_bank_utils
                        .format_currency(
                            transaction.get(
                                "amount",
                                0
                            )
                        ),

                    "Balance After":
                        go_bank_utils
                        .format_currency(
                            transaction.get(
                                "balance_after",
                                0
                            )
                        )
                })


            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No transaction history available."
            )


    # ======================================
    # TRANSACTION ANALYSIS
    # ======================================

    elif menu == "Transaction Analysis":

        st.header(
            ":red[Transaction Analysis]"
        )

        st.divider()

        result = (
            go_bank_analysis
            .analyze_transactions(
                account.account_number
            )
        )


        # ==================================
        # ANALYSIS 1
        # TRANSACTION SUMMARY
        # ==================================

        st.header(
            "Transaction Summary"
        )

        col1, col2, col3 = st.columns(3, border=True)

        col1.badge("Total Transactions",color="red")
        col1.metric(
            "・・・・・",
            result[
                "total_transactions"
            ]
        )

        col2.badge("Deposits",color="red")
        col2.metric(
            "・・・・・",
            result[
                "deposits"
            ]
        )

        col3.badge("Withdrawals",color="red")
        col3.metric(
            "・・・・・",
            result[
                "withdrawals"
            ]
        )


        st.divider()


        # ==================================
        # ANALYSIS 2
        # MONEY FLOW
        # ==================================

        st.header(
            "Money Flow Analysis"
        )

        col1, col2, col3 = st.columns(3, border=True)

        col1.badge("Total Deposited",color="red")
        col1.metric(
            "・・・・・",
            go_bank_utils
            .format_currency(
                result[
                    "total_deposited"
                ]
            )
        )

        col2.badge("Total Withdrawn",color="red")
        col2.metric(
            "・・・・・",
            go_bank_utils
            .format_currency(
                result[
                    "total_withdrawn"
                ]
            )
        )

        col3.badge("Net Cash Flow",color="red")
        col3.metric(
            "・・・・・",
            go_bank_utils
            .format_currency(
                result[
                    "net_cash_flow"
                ]
            )
        )


        st.divider()


        # ==================================
        # ANALYSIS 3
        # ACCOUNT ACTIVITY
        # ==================================

        st.header(
            "Account Activity Analysis"
        )

        col1, col2, col3 = st.columns(3, border=True)


        col1.badge("Largest Transaction",color="red")
        col1.metric(
            "・・・・・",
            go_bank_utils
            .format_currency(
                result[
                    "largest_transaction"
                ]
            )
        )

        col2.badge("Average Transaction",color="red")
        col2.metric(
            "・・・・・",
            go_bank_utils
            .format_currency(
                result[
                    "average_transaction"
                ]
            )
        )

        col3.badge("Latest Transaction",color="red")
        col3.metric(
            "・・・・・",
            result[
                "latest_transaction"
            ]
        )

        st.divider()

        st.caption(
            f"Latest Activity: "
            f"{result['latest_timestamp']}"
        )