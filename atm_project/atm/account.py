from .storage import load_data

def get_balance(account_number):
    """Returns the current balance for an account."""
    data = load_data()
    if account_number in data:
        return data[account_number]["balance"]
    return None

def get_history(account_number):
    """Returns the transaction history for an account."""
    data = load_data()
    if account_number in data:
        return data[account_number]["history"]
    return None
