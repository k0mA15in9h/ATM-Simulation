from .storage import load_data, save_data

def authenticate(account_number, pin):
    """Validates an account number and pin against the stored data."""
    data = load_data()
    if account_number in data:
        return data[account_number]["pin"] == pin
    return False

def create_account(account_number, pin, initial_balance=0.0):
    """Creates a new account in the system."""
    data = load_data()
    
    if account_number in data:
        return False, "Account number already exists."
        
    data[account_number] = {
        "pin": pin,
        "balance": initial_balance,
        "history": []
    }
    
    if initial_balance > 0:
        data[account_number]["history"].append(f"Account created with initial balance: ${initial_balance:.2f}")
    else:
        data[account_number]["history"].append("Account created.")
        
    save_data(data)
    return True, "Account created successfully."
