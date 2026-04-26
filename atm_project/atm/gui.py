import tkinter as tk
from tkinter import messagebox, ttk
from .auth import authenticate, create_account
from .account import get_balance, get_history
from .transactions import deposit, withdraw

class ATMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATM System")
        self.geometry("500x650")
        self.configure(bg="#f0f2f5")
        self.current_user = None

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11), padding=5)
        style.configure("TLabel", font=("Helvetica", 11), background="#f0f2f5")
        
        self.container = tk.Frame(self, bg="#f0f2f5")
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, DashboardFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("LoginFrame")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff", padx=40, pady=40)
        self.controller = controller
        
        # Center the frame content using pack or grid weights
        content = tk.Frame(self, bg="#ffffff")
        content.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(content, text="Welcome to ATM", font=("Helvetica", 20, "bold"), bg="#ffffff")
        title.pack(pady=(0, 20))

        tk.Label(content, text="Account Number:", font=("Helvetica", 12), bg="#ffffff").pack(anchor="w")
        self.acc_entry = ttk.Entry(content, font=("Helvetica", 12), width=25)
        self.acc_entry.pack(pady=(5, 15))

        tk.Label(content, text="PIN:", font=("Helvetica", 12), bg="#ffffff").pack(anchor="w")
        self.pin_entry = ttk.Entry(content, show="*", font=("Helvetica", 12), width=25)
        self.pin_entry.pack(pady=(5, 25))

        login_btn = tk.Button(content, text="Login", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", 
                              width=23, command=self.login, cursor="hand2", borderwidth=0, pady=10)
        login_btn.pack(pady=5)

        reg_btn = tk.Button(content, text="Create New Account", font=("Helvetica", 11), fg="#2196F3", bg="#ffffff", 
                            borderwidth=0, cursor="hand2", command=lambda: controller.show_frame("RegisterFrame"))
        reg_btn.pack()
        
    def on_show(self):
        self.acc_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)
        self.controller.current_user = None

    def login(self):
        acc = self.acc_entry.get().strip()
        pin = self.pin_entry.get().strip()
        if not acc or not pin:
            messagebox.showerror("Error", "Please enter both Account Number and PIN.")
            return

        if authenticate(acc, pin):
            self.controller.current_user = acc
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid account number or PIN.")

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff", padx=40, pady=40)
        self.controller = controller

        content = tk.Frame(self, bg="#ffffff")
        content.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(content, text="Create Account", font=("Helvetica", 20, "bold"), bg="#ffffff")
        title.pack(pady=(0, 20))

        tk.Label(content, text="Choose Account Number:", font=("Helvetica", 12), bg="#ffffff").pack(anchor="w")
        self.acc_entry = ttk.Entry(content, font=("Helvetica", 12), width=25)
        self.acc_entry.pack(pady=(5, 10))

        tk.Label(content, text="Choose PIN:", font=("Helvetica", 12), bg="#ffffff").pack(anchor="w")
        self.pin_entry = ttk.Entry(content, font=("Helvetica", 12), width=25)
        self.pin_entry.pack(pady=(5, 10))

        tk.Label(content, text="Initial Deposit ($):", font=("Helvetica", 12), bg="#ffffff").pack(anchor="w")
        self.dep_entry = ttk.Entry(content, font=("Helvetica", 12), width=25)
        self.dep_entry.insert(0, "0")
        self.dep_entry.pack(pady=(5, 25))

        create_btn = tk.Button(content, text="Register", font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", 
                              width=23, command=self.register, cursor="hand2", borderwidth=0, pady=10)
        create_btn.pack(pady=5)

        back_btn = tk.Button(content, text="Back to Login", font=("Helvetica", 11), fg="#757575", bg="#ffffff", 
                            borderwidth=0, cursor="hand2", command=lambda: controller.show_frame("LoginFrame"))
        back_btn.pack()

    def on_show(self):
        self.acc_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)
        self.dep_entry.delete(0, tk.END)
        self.dep_entry.insert(0, "0")

    def register(self):
        acc = self.acc_entry.get().strip()
        pin = self.pin_entry.get().strip()
        dep = self.dep_entry.get().strip()

        if not acc or not pin:
            messagebox.showerror("Error", "Account Number and PIN are required.")
            return

        try:
            dep_amt = float(dep)
            if dep_amt < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Initial deposit must be a valid positive number.")
            return

        success, msg = create_account(acc, pin, dep_amt)
        if success:
            messagebox.showinfo("Success", "Account created successfully! You can now login.")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", msg)

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg="#2196F3", pady=15, padx=20)
        header.pack(fill="x")
        
        self.welcome_msg = tk.Label(header, text="Dashboard", font=("Helvetica", 16, "bold"), bg="#2196F3", fg="white")
        self.welcome_msg.pack(side="left")
        
        logout_btn = tk.Button(header, text="Logout", font=("Helvetica", 10, "bold"), bg="#f44336", fg="white", 
                              borderwidth=0, padx=10, pady=5, cursor="hand2", command=lambda: controller.show_frame("LoginFrame"))
        logout_btn.pack(side="right")

        content = tk.Frame(self, bg="#ffffff", padx=30, pady=20)
        content.pack(fill="both", expand=True)

        # Balance Card
        card = tk.Frame(content, bg="#f5f5f5", pady=20, borderwidth=1, relief="solid")
        card.pack(fill="x", pady=(0, 20))
        
        tk.Label(card, text="Current Balance", font=("Helvetica", 12), bg="#f5f5f5", fg="#616161").pack()
        self.balance_lbl = tk.Label(card, text="$0.00", font=("Helvetica", 28, "bold"), bg="#f5f5f5", fg="#4CAF50")
        self.balance_lbl.pack()

        # Action Area
        actions = tk.Frame(content, bg="#ffffff")
        actions.pack(fill="x", pady=10)

        self.amt_entry = ttk.Entry(actions, font=("Helvetica", 14), width=15)
        self.amt_entry.pack(side="left", padx=(0, 10), ipady=5)

        dep_btn = tk.Button(actions, text="Deposit", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", 
                              borderwidth=0, padx=15, pady=8, cursor="hand2", command=self.do_deposit)
        dep_btn.pack(side="left", padx=5)

        with_btn = tk.Button(actions, text="Withdraw", font=("Helvetica", 12, "bold"), bg="#FF9800", fg="white", 
                              borderwidth=0, padx=15, pady=8, cursor="hand2", command=self.do_withdraw)
        with_btn.pack(side="left", padx=5)

        # History Area
        tk.Label(content, text="Transaction History", font=("Helvetica", 14, "bold"), bg="#ffffff").pack(anchor="w", pady=(20, 5))
        
        history_frame = tk.Frame(content)
        history_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_txt = tk.Text(history_frame, yscrollcommand=scrollbar.set, font=("Consolas", 10), state="disabled", bg="#fafafa", relief="flat")
        self.history_txt.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_txt.yview)

    def on_show(self):
        self.amt_entry.delete(0, tk.END)
        self.refresh_data()

    def refresh_data(self):
        user = self.controller.current_user
        if not user: return
        
        self.welcome_msg.config(text=f"Account: {user}")
        
        balance = get_balance(user)
        self.balance_lbl.config(text=f"${balance:.2f}" if balance is not None else "$0.00")
        
        history = get_history(user) or []
        self.history_txt.config(state="normal")
        self.history_txt.delete("1.0", tk.END)
        for h in reversed(history): # show newest first
            self.history_txt.insert(tk.END, h + "\n")
        self.history_txt.config(state="disabled")

    def do_deposit(self):
        self.process_transaction(deposit)

    def do_withdraw(self):
        self.process_transaction(withdraw)

    def process_transaction(self, func):
        try:
            amt = float(self.amt_entry.get())
            if amt <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount.")
            return

        success, msg = func(self.controller.current_user, amt)
        if success:
            messagebox.showinfo("Success", msg)
            self.amt_entry.delete(0, tk.END)
            self.refresh_data()
        else:
            messagebox.showerror("Transaction Failed", msg)
