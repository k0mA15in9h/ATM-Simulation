from atm.gui import ATMApp

if __name__ == "__main__":
    try:
        app = ATMApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n\nATM shutdown requested. Goodbye!")
