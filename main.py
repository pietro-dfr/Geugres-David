import random

class BankAccount:
    def __init__(self, holder: str, password: str) -> None:
        self.__holder: str = holder
        self.__account_number: int | None = None
        self.__password: str = password
        self.__balance: float = 0.0

    @property
    def holder(self) -> str:
        return self.__holder

    @holder.setter
    def holder(self, value: str) -> None:
        self.__holder = value

    @property
    def account_number(self) -> int | None:
        return self.__account_number

    @account_number.setter
    def account_number(self, value: int) -> None:
        self.__account_number = value

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str) -> None:
        self.__password = value

    @property
    def balance(self) -> float:
        return self.__balance

    @balance.setter
    def balance(self, value: float) -> None:
        self.__balance = value

    def __str__(self) -> str:
        return (
            f"Bank Account {{ holder = '{self.__holder}', "
            f"account number = {self.__account_number}, "
            f"password = '{self.__password}', "
            f"balance = R${self.__balance:,.2f} }}"
        )


class Bank:
    def __init__(self):
        self.__registered_accounts: list[BankAccount] = []
        self.__MIN_ACC_NUMBER: int = 1000
        self.__MAX_ACC_NUMBER: int = 9999

    def add_account(self, account: BankAccount) -> None:
        existing_account_numbers = {acc.account_number for acc in self.__registered_accounts}
        while True:
            acc_number = random.randint(self.__MIN_ACC_NUMBER, self.__MAX_ACC_NUMBER)
            if acc_number not in existing_account_numbers:
                account.account_number = acc_number
                self.__registered_accounts.append(account)
                break

    def remove_account(self, account_number: int) -> None:
        for acc in self.__registered_accounts:
            if acc.account_number == account_number:
                self.__registered_accounts.remove(acc)
                return
        print("App:Query -> Account not found!")

    def list_accounts(self) -> None:
        if not self.__registered_accounts:
            print("App:Query -> No accounts!")
            return
        print("Account List:")
        for acc in self.__registered_accounts:
            print(acc)

    def find_account(self, account_number: int) -> BankAccount | None:
        for acc in self.__registered_accounts:
            if acc.account_number == account_number:
                return acc
        return None

    def account_list_empty(self) -> bool:
        return len(self.__registered_accounts) == 0

    def withdraw(self, account: BankAccount, amount: float) -> bool:
        if amount <= 0:
            print("Invalid withdraw value!")
            return False
        if account.balance < amount:
            print("Insufficient balance for withdraw!")
            return False
        account.balance -= amount
        return True

    def deposit(self, account: BankAccount, amount: float) -> bool:
        if amount <= 0:
            print("Invalid deposit value!")
            return False
        account.balance += amount
        return True

    def transfer(self, account: BankAccount, other_account: BankAccount, amount: float) -> bool:
        if amount <= 0:
            print("Invalid transfer value!")
            return False
        if account.balance < amount:
            print("Insufficient balance for transfer!")
            return False
        account.balance -= amount
        other_account.balance += amount
        return True

    def accounts_list(self) -> list[BankAccount]:
        return self.__registered_accounts


def safe_float_input(msg: str, fail_msg: str) -> float:
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print(fail_msg)

def safe_int_input(msg: str, fail_msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print(fail_msg)


def create_account(bank: Bank) -> None:
    print("+======= Create Account =======+")
    holder = input("HOLDER: ")
    password = input("PASSWORD: ")
    
    while len(password) != 6:
        print("App:Login Error -> Password must be 6 digits!")
        password = input("PASSWORD: ")
        
    bank.add_account(BankAccount(holder, password))


def authenticate(holder: str, password: str, accounts_list: list[BankAccount]) -> BankAccount | None:
    for acc in accounts_list:
        if acc.holder == holder and acc.password == password:
            return acc
    print("App:Login Error -> Invalid password or user!")
    return None


def login_page(bank: Bank) -> None:
    accounts_list = bank.accounts_list()
    while True:
        holder = input("HOLDER NAME: ")
        password = input("PASSWORD: ")
        account_in_use = authenticate(holder, password, accounts_list)

        if account_in_use is None:
            break

        while True:
            print(
                "\n+=== Account Menu ===+\n"
                "| [1] Withdraw       |\n"
                "| [2] Deposit        |\n"
                "| [3] Transfer       |\n"
                "| [4] Log-off        |\n"
                "+====================+"
            )
            option = input("Choose: ")

            if option == "1":
                amount = safe_float_input("AMOUNT: ", "Invalid!")
                if bank.withdraw(account_in_use, amount):
                    print(f"New balance: R${account_in_use.balance:,.2f}")

            elif option == "2":
                amount = safe_float_input("AMOUNT: ", "Invalid!")
                if bank.deposit(account_in_use, amount):
                    print(f"New balance: R${account_in_use.balance:,.2f}")

            
            elif option == "3":
                try:
                    other_account_number = safe_int_input("RECIPIENT ACCOUNT NUMBER: ", "INVALID!")
                    other_account = bank.find_account(other_account_number)

                    if other_account is None:
                        print("App:Transfer Error -> Account not found!")
                        continue
                    if other_account.account_number == account_in_use.account_number:
                        print("App:Transfer Error -> Cannot transfer to same account!")
                        continue

                    amount = safe_float_input("AMOUNT: ", "Invalid!")
                    before_sender = str(account_in_use)
                    before_receiver = str(other_account)

                    if bank.transfer(account_in_use, other_account, amount):
                        print("Transfer successful!")
                        print("Sender before: " + before_sender)
                        print("Sender after: " + str(account_in_use))
                        print("Recipient before: " + before_receiver)
                        print("Recipient after: " + str(other_account))
                    else:
                        print("Transfer failed!")
                except ValueError:
                    print("App:Input Error -> Please enter a valid account number!")

            
            elif option == "4":
                print("Logoff successful. See you soon!")
                return

            else:
                print("Invalid option. Please try again.")


# Main Program
bank = Bank()
while True:
    print("+======= Menu =======+\n"
          "| [1] Login          |\n"
          "| [2] Create Account  |\n"
          "| [3] List Accounts   |\n"
          "| [4] Exit           |\n"
          "+====================+"
        )
    choice = input("Choose: ")
    if choice == "1":
        if bank.account_list_empty():
            print("App:Login Error -> No accounts registered!")
            continue
        login_page(bank)

    elif choice == "2":
        create_account(bank)

    elif choice == "3":
        bank.list_accounts()

    elif choice == "4":
        print("Goodbye.")
        break

    else:
        print("App:Option Error -> Choose a valid option!")
