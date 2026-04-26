from .storage import load_data, save_data
from datetime import datetime

def _get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def deposit(account_number, amount):
    """Deposits a given amount into the specified account."""
    if amount <= 0:
        return False, "Deposit amount must be positive."
        
    data = load_data()
    if account_number not in data:
        return False, "Account not found."
        
    data[account_number]["balance"] += amount
    timestamp = _get_timestamp()
    data[account_number]["history"].append(f"[{timestamp}] Deposited: ${amount:.2f}")
    
    save_data(data)
    return True, f"Successfully deposited ${amount:.2f}."

def withdraw(account_number, amount):
    """Withdraws a given amount from the specified account."""
    if amount <= 0:
        return False, "Withdrawal amount must be positive."
        
    data = load_data()
    if account_number not in data:
        return False, "Account not found."
        
    if data[account_number]["balance"] < amount:
        return False, "Insufficient funds."
        
    data[account_number]["balance"] -= amount
    timestamp = _get_timestamp()
    data[account_number]["history"].append(f"[{timestamp}] Withdrew: ${amount:.2f}")
    
    save_data(data)
    return True, f"Successfully withdrew ${amount:.2f}."
