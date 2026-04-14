from datetime import datetime
from utils import FinReview

app = FinReview()

while True:
    print("\n1. Add transaction")
    print("2. View balance")
    print("3. View total income")
    print("4. View total expenses")
    print("5. View transactions")
    print("6. View monthly summary")
    print("7. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        app.add_transaction()
    elif choice in ["2", "3", "4"]:
        app.view_option(choice=choice)
    elif choice == "5":
        app.view_trans_by_date()
    elif choice == "6":
        app.monthly_summary()
    elif choice == "7":
        break
    else:
        print("Invalid choice.")
        break



