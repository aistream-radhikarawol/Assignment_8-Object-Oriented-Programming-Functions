import logging


# ==========================================================
# LOGGING CONFIGURATION
# ==========================================================

logging.basicConfig(
    filename="banking.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================================
# CUSTOM EXCEPTIONS
# ==========================================================

class BankingError(Exception):
    pass


class InsufficientFundsError(BankingError):
    pass


class InvalidAmountError(BankingError):
    pass


class AccountNotFoundError(BankingError):
    pass


# ==========================================================
# ACCOUNT BASE CLASS
# ==========================================================

class Account:

    def __init__(
        self,
        account_number,
        holder_name,
        balance=0
    ):

        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance

        self.transaction_history = []

        self.log_transaction(
            f"Account created with balance "
            f"₹{balance:.2f}"
        )

        logging.info(
            f"Account created: {account_number}"
        )

    # ------------------------------------------------------
    # Transaction logging
    # ------------------------------------------------------

    def log_transaction(self, message):

        self.transaction_history.append(message)

    # ------------------------------------------------------
    # Deposit
    # ------------------------------------------------------

    def deposit(self, amount):

        if amount <= 0:
            raise InvalidAmountError(
                "Deposit amount must be greater than 0."
            )

        self.balance += amount

        self.log_transaction(
            f"Deposited ₹{amount:.2f}"
        )

        logging.info(
            f"Deposit: {self.account_number} "
            f"₹{amount:.2f}"
        )

    # ------------------------------------------------------
    # Withdraw
    # ------------------------------------------------------

    def withdraw(self, amount):

        if amount <= 0:
            raise InvalidAmountError(
                "Withdrawal amount must be greater than 0."
            )

        if amount > self.balance:
            raise InsufficientFundsError(
                "Insufficient balance."
            )

        self.balance -= amount

        self.log_transaction(
            f"Withdrawn ₹{amount:.2f}"
        )

        logging.info(
            f"Withdrawal: {self.account_number} "
            f"₹{amount:.2f}"
        )

    # ------------------------------------------------------
    # Display balance
    # ------------------------------------------------------

    def display_balance(self):

        print(
            f"\nAccount Number: {self.account_number}"
        )

        print(
            f"Account Holder: {self.holder_name}"
        )

        print(
            f"Balance: ₹{self.balance:.2f}"
        )

    # ------------------------------------------------------
    # Transaction history
    # ------------------------------------------------------

    def show_transactions(self):

        print("\n--- Transaction History ---")

        if not self.transaction_history:
            print("No transactions found.")
            return

        for index, transaction in enumerate(
            self.transaction_history,
            start=1
        ):

            print(
                f"{index}. {transaction}"
            )


# ==========================================================
# SAVINGS ACCOUNT
# ==========================================================

class SavingsAccount(Account):

    def __init__(
        self,
        account_number,
        holder_name,
        balance=0,
        interest_rate=4.0
    ):

        super().__init__(
            account_number,
            holder_name,
            balance
        )

        self.interest_rate = interest_rate

    # ------------------------------------------------------
    # Calculate interest
    # ------------------------------------------------------

    def calculate_interest(self):

        interest = (
            self.balance
            * self.interest_rate
            / 100
        )

        self.log_transaction(
            f"Interest calculated: ₹{interest:.2f}"
        )

        return interest

    # ------------------------------------------------------
    # Add interest to balance
    # ------------------------------------------------------

    def add_interest(self):

        interest = self.calculate_interest()

        self.balance += interest

        self.log_transaction(
            f"Interest added: ₹{interest:.2f}"
        )

        logging.info(
            f"Interest added: {self.account_number} "
            f"₹{interest:.2f}"
        )

        return interest


# ==========================================================
# CHECKING ACCOUNT
# ==========================================================

class CheckingAccount(Account):

    def __init__(
        self,
        account_number,
        holder_name,
        balance=0,
        transaction_fee=10
    ):

        super().__init__(
            account_number,
            holder_name,
            balance
        )

        self.transaction_fee = transaction_fee

    # ------------------------------------------------------
    # Override withdraw method
    # ------------------------------------------------------

    def withdraw(self, amount):

        if amount <= 0:
            raise InvalidAmountError(
                "Withdrawal amount must be greater than 0."
            )

        total_amount = (
            amount + self.transaction_fee
        )

        if total_amount > self.balance:

            raise InsufficientFundsError(
                "Insufficient balance including "
                "transaction fee."
            )

        self.balance -= total_amount

        self.log_transaction(
            f"Withdrawn ₹{amount:.2f} "
            f"(Fee: ₹{self.transaction_fee:.2f})"
        )

        logging.info(
            f"Checking withdrawal: "
            f"{self.account_number} "
            f"₹{amount:.2f}"
        )


# ==========================================================
# BANK SYSTEM
# ==========================================================

class Bank:

    def __init__(self):

        self.accounts = {}

    # ------------------------------------------------------
    # Create account
    # ------------------------------------------------------

    def create_account(self):

        print("\n--- Create Account ---")

        account_number = input(
            "Enter account number: "
        ).strip()

        if not account_number:
            print("Account number cannot be empty.")
            return

        if account_number in self.accounts:

            print(
                "Account number already exists."
            )

            return

        holder_name = input(
            "Enter account holder name: "
        ).strip()

        if not holder_name:

            print(
                "Account holder name cannot be empty."
            )

            return

        print("\nAccount Type")
        print("1. Savings Account")
        print("2. Checking Account")

        account_type = input(
            "Enter choice: "
        )

        try:

            initial_balance = float(
                input("Enter initial balance: ")
            )

            if initial_balance < 0:

                print(
                    "Balance cannot be negative."
                )

                return

        except ValueError:

            print(
                "Please enter a valid amount."
            )

            return

        if account_type == "1":

            account = SavingsAccount(
                account_number,
                holder_name,
                initial_balance
            )

        elif account_type == "2":

            account = CheckingAccount(
                account_number,
                holder_name,
                initial_balance
            )

        else:

            print("Invalid account type.")
            return

        self.accounts[
            account_number
        ] = account

        print(
            "Account created successfully."
        )

    # ------------------------------------------------------
    # Find account
    # ------------------------------------------------------

    def get_account(self):

        account_number = input(
            "Enter account number: "
        ).strip()

        if account_number not in self.accounts:

            raise AccountNotFoundError(
                "Account not found."
            )

        return self.accounts[
            account_number
        ]

    # ------------------------------------------------------
    # Deposit
    # ------------------------------------------------------

    def deposit_money(self):

        try:

            account = self.get_account()

            amount = float(
                input("Enter deposit amount: ")
            )

            account.deposit(amount)

            print(
                "Money deposited successfully."
            )

            account.display_balance()

        except (
            BankingError,
            ValueError
        ) as error:

            print(
                f"Error: {error}"
            )

    # ------------------------------------------------------
    # Withdraw
    # ------------------------------------------------------

    def withdraw_money(self):

        try:

            account = self.get_account()

            amount = float(
                input("Enter withdrawal amount: ")
            )

            account.withdraw(amount)

            print(
                "Money withdrawn successfully."
            )

            account.display_balance()

        except (
            BankingError,
            ValueError
        ) as error:

            print(
                f"Error: {error}"
            )

    # ------------------------------------------------------
    # Balance
    # ------------------------------------------------------

    def show_balance(self):

        try:

            account = self.get_account()

            account.display_balance()

        except BankingError as error:

            print(
                f"Error: {error}"
            )

    # ------------------------------------------------------
    # Transactions
    # ------------------------------------------------------

    def show_transactions(self):

        try:

            account = self.get_account()

            account.show_transactions()

        except BankingError as error:

            print(
                f"Error: {error}"
            )

    # ------------------------------------------------------
    # Interest
    # ------------------------------------------------------

    def add_interest(self):

        try:

            account = self.get_account()

            if not isinstance(
                account,
                SavingsAccount
            ):

                print(
                    "Interest is available "
                    "only for Savings Accounts."
                )

                return

            interest = account.add_interest()

            print(
                f"Interest added: ₹{interest:.2f}"
            )

            account.display_balance()

        except BankingError as error:

            print(
                f"Error: {error}"
            )

    # ------------------------------------------------------
    # Run application
    # ------------------------------------------------------

    def run(self):

        while True:

            print("\n==============================")
            print("       BANKING SYSTEM")
            print("==============================")

            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check Balance")
            print("5. Transaction History")
            print("6. Add Savings Interest")
            print("7. Exit")

            choice = input(
                "Enter your choice: "
            )

            if choice == "1":

                self.create_account()

            elif choice == "2":

                self.deposit_money()

            elif choice == "3":

                self.withdraw_money()

            elif choice == "4":

                self.show_balance()

            elif choice == "5":

                self.show_transactions()

            elif choice == "6":

                self.add_interest()

            elif choice == "7":

                print(
                    "Thank you for using "
                    "the Banking System."
                )

                break

            else:

                print(
                    "Invalid choice."
                )


# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    bank = Bank()

    bank.run()