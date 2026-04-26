from atm.account import Account
from atm.transactions import TransactionHistory

def start_atm():
    account = Account(1000)  # initial balance
    history = TransactionHistory()

    while True:
        print("\n====== 🏦 ATM MENU ======")
        print("1. Display Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. View Statement")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            account.display_balance()

        elif choice == "2":
            amount = float(input("Enter amount to deposit: "))
            account.deposit(amount)
            history.add_transaction(f"Deposited ₹{amount}")

        elif choice == "3":
            amount = float(input("Enter amount to withdraw: "))
            account.withdraw(amount)
            history.add_transaction(f"Withdrawn ₹{amount}")

        elif choice == "4":
            history.show_statement()

        elif choice == "5":
            print("👋 Thank you for using ATM")
            break

        else:
            print("❌ Invalid choice")