'''
1) To increase features to extract transactions on specific datetimes.
2) Maybe add new columns?
3) Add in test functions
'''

from datetime import datetime

date = datetime.now().strftime("%Y-%m-%d")
data = "data/data.csv"
def add_transaction():
    date = input("Date (dd/mm/yyyy): ")
    amount = float(input("Enter amount: "))
    category = input("Enter category:/n" \
                     "1. Entertainment/n" \
                     "2. Food/n" \
                     "3. Transport/n" \
                     "4. Household Bills/n" \
                     "5. Salary/n" \
                     "6. Medical/n" \
    )
    t_type = input("Income/Expense/Bonus: ")

    with open(data, "a", newline = '') as file:
        file.write(f"{date},{amount},{category},{t_type}\n")

def view_balance():
    balance = 0
    with open(data, "r") as file:
        next(file) # Skip header line in csv
        for line in file:
            date, amount, category, t_type = line.strip().split(",")
            amount = float(amount)
            if t_type == "Income" or t_type == "Bonus":
                balance += amount
            elif t_type == "Expense":
                balance -= amount
            else:
                print("Invalid option, please raise recommendation.")
    print(f"Current Balance: {balance}")

while True:
    print("\n1. Add transaction")
    print("2. View balance")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_transaction()
    elif choice == "2":
        view_balance()
    elif choice == "3":
        break
    else:
        print("Invalid choice.")
        break

