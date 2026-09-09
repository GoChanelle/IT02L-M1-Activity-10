import streamlit as st

import balaman_bank_auth
import balaman_bank_storage
import balaman_bank_transactions
import balaman_bank_analysis
import balaman_bank_utils


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="balaman Bank",
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

st.title("balaman BANK")

st.caption(
    "Secure Digital Banking System"
)


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
                balaman_bank_auth
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
            "Create Your balaman Bank Account"
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
                balaman_bank_auth
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
        "balaman BANK"
    )

    st.sidebar.write(
        f"**{account.account_name}**"
    )

    st.sidebar.caption(
        account.get_account_type()
    )

    st.sidebar.write(
        f"Account: "
        f"{account.account_number}"
    )

    st.sidebar.divider()


    menu = st.sidebar.radio(
        "BANKING MENU",
        [
            "Dashboard",
            "Deposit",
            "Withdraw",
            "Transaction History",
            "Transaction Analysis"
        ]
    )


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

        st.header(
            f"Welcome, {account.account_name}"
        )

        st.subheader(
            "Account Overview"
        )

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Current Balance",
            balaman_bank_utils
            .format_currency(
                account.check_balance()
            )
        )


        col2.metric(
            "Account Type",
            account.get_account_type()
        )


        col3.metric(
            "Account Number",
            account.account_number
        )


        st.divider()


        st.info(
            "Select a banking service from "
            "the menu on the left."
        )


    # ======================================
    # DEPOSIT
    # ======================================

    elif menu == "Deposit":

        st.header(
            "Deposit Money"
        )

        st.write(
            f"Current Balance: "
            f"**{balaman_bank_utils.format_currency(account.check_balance())}**"
        )

        amount = st.number_input(
            "Deposit Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )


        if st.button(
            "Confirm Deposit",
            use_container_width=True
        ):

            if not balaman_bank_utils.is_valid_amount(
                amount
            ):

                st.error(
                    "Invalid deposit amount."
                )

            else:

                success = account.deposit(
                    amount
                )

                if success:

                    balaman_bank_storage.update_account(
                        account
                    )

                    balaman_bank_transactions.record_transaction(
                        account,
                        "Deposit",
                        amount
                    )

                    st.success(
                        "Deposit successful."
                    )

                    st.metric(
                        "New Balance",
                        balaman_bank_utils
                        .format_currency(
                            account.check_balance()
                        )
                    )


    # ======================================
    # WITHDRAW
    # ======================================

    elif menu == "Withdraw":

        st.header(
            "Withdraw Money"
        )

        st.write(
            f"Available Balance: "
            f"**{balaman_bank_utils.format_currency(account.check_balance())}**"
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

            if not balaman_bank_utils.is_valid_amount(
                amount
            ):

                st.error(
                    "Invalid withdrawal amount."
                )

            elif amount > account.check_balance():

                st.error(
                    "Insufficient balance."
                )

            else:

                success = account.withdraw(
                    amount
                )

                if success:

                    balaman_bank_storage.update_account(
                        account
                    )

                    balaman_bank_transactions.record_transaction(
                        account,
                        "Withdraw",
                        amount
                    )

                    st.success(
                        "Withdrawal successful."
                    )

                    st.metric(
                        "New Balance",
                        balaman_bank_utils
                        .format_currency(
                            account.check_balance()
                        )
                    )


    # ======================================
    # TRANSACTION HISTORY
    # ======================================

    elif menu == "Transaction History":

        st.header(
            "Transaction History"
        )

        transactions = (
            balaman_bank_transactions
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
                        balaman_bank_utils
                        .format_currency(
                            transaction.get(
                                "amount",
                                0
                            )
                        ),

                    "Balance After":
                        balaman_bank_utils
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
            "Transaction Analysis"
        )

        result = (
            balaman_bank_analysis
            .analyze_transactions(
                account.account_number
            )
        )


        # ==================================
        # ANALYSIS 1
        # TRANSACTION SUMMARY
        # ==================================

        st.subheader(
            "1. Transaction Summary"
        )

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Total Transactions",
            result[
                "total_transactions"
            ]
        )


        col2.metric(
            "Deposits",
            result[
                "deposits"
            ]
        )


        col3.metric(
            "Withdrawals",
            result[
                "withdrawals"
            ]
        )


        st.divider()


        # ==================================
        # ANALYSIS 2
        # MONEY FLOW
        # ==================================

        st.subheader(
            "2. Money Flow Analysis"
        )

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Total Deposited",
            balaman_bank_utils
            .format_currency(
                result[
                    "total_deposited"
                ]
            )
        )


        col2.metric(
            "Total Withdrawn",
            balaman_bank_utils
            .format_currency(
                result[
                    "total_withdrawn"
                ]
            )
        )


        col3.metric(
            "Net Cash Flow",
            balaman_bank_utils
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

        st.subheader(
            "3. Account Activity Analysis"
        )

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Largest Transaction",
            balaman_bank_utils
            .format_currency(
                result[
                    "largest_transaction"
                ]
            )
        )


        col2.metric(
            "Average Transaction",
            balaman_bank_utils
            .format_currency(
                result[
                    "average_transaction"
                ]
            )
        )


        col3.metric(
            "Latest Transaction",
            result[
                "latest_transaction"
            ]
        )


        st.caption(
            f"Latest Activity: "
            f"{result['latest_timestamp']}"
        )