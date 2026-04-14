from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

class FinReview:
    def __init__(self):
        self.categories = {
            "1" : "Entertainment",
            "2" : "Food",
            "3" : "Transport",
            "4" : "Household Bills",
            "5" : "Salary",
            "6" : "Medical"
            }
    
    def load_data(self):
        df = pd.read_csv("data/data.csv")
        df["Amount"] = df["Amount"].astype(float)
        df["Type"] = df["Type"].str.strip().str.lower()
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
        df["Category"] = df["Category"].str.strip()
        return df

    def add_transaction(self):
        date = input("Date (dd/mm/yyyy): ")
        while True:
            try:
                amount = float(input("Enter amount: "))
                break
            except ValueError:
                print("Invalid amount.")
                continue
        category = input("Enter category:\n" \
                         "1. Entertainment\n" \
                         "2. Food\n" \
                         "3. Transport\n" \
                         "4. Household Bills\n" \
                         "5. Salary\n" \
                         "6. Medical\n" \
        )
        category = self.categories.get(category, "Unknown")
        t_type = input("Income/Expense/Bonus: ").lower()

        with open("data/data.csv", "a", newline = '') as file:
            file.write(f"{date},{amount},{category},{t_type}\n")

    def view_option(self, choice):
        df = self.load_data()

        income = df[df["Type"].isin(["income", "bonus"])]["Amount"].sum()
        expenses = df[df["Type"] == "expense"]["Amount"].sum()
        balance = income - expenses

        if choice == "2":
            print(f"Balance: {balance}")
        elif choice == "3":
            print(f"Income: {income}")
        elif choice == "4":
            print(f"Expenses: {expenses}")
    
    def get_valid_date(self, prompt):
        while True:
            user_input = input(prompt)
            try:
                return datetime.strptime(user_input, "%d/%m/%Y")
            except ValueError:
                print("Invalid date format. Use dd/mm/yyyy.")       

    def get_trans_by_date(self, start_date, end_date):
        df = self.load_data()
        
        # Filter by date range
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        
        # Sort
        return filtered_df.sort_values(by="Date")

    def view_trans_by_date(self):
        start_date = self.get_valid_date("Enter start date: ")
        end_date = self.get_valid_date("Enter end date:" )

        df = self.get_trans_by_date(start_date, end_date)
        
        for _, row in df.iterrows():
            print(f"{row['Date'].strftime('%d/%m/%Y')} | {row['Category']} | {row['Type']} | ${row['Amount']:.2f}")
    
    def monthly_summary(self):
        '''
        This function is designed to:
        1) Show the financial balance by month
        2) Show the monthly financial movement by category
        3) Visualise the monthly earnings and spendings 
        4) Visualise the monthly financial movement by category
        '''
        df = self.load_data()

        df["month"] = df["Date"].dt.to_period("M")
        monthly_bal = df.groupby("month")["Amount"].sum()
        monthly_cat_bal = df.groupby(["Category", "month"])["Amount"].sum()

        print(f"Monthly balance summary: {monthly_bal}")
        print(f"Monthly summary by category: {monthly_cat_bal}")
        
        # create new pivot table for monthly category visual chart
        cat_bal = df.pivot_table(
            index="month",
            columns="Category",
            values="Amount",
            aggfunc="sum",
            fill_value=0
        )
        
        '''
        #-----------------------------------
        create mini dashboard UI for:
        1) monthly cashflow trend line chart
        2) monthly category breakdown chart
        '''

        plt.figure(figsize=(10, 8))
        # create new pivot table for monthly category visual chart
        cat_bal = df.pivot_table(
            index="month",
            columns="Category",
            values="Amount",
            aggfunc="sum",
            fill_value=0
        )

        # Prepare data for plotting
        cat_bal.index = cat_bal.index.astype(str)
        income = df[df["Type"].isin(["income", "bonus"])]\
                 .groupby("month")["Amount"].sum()
        expense = df[df["Type"] == "expense"]\
                  .groupby("month")["Amount"].sum()
        
        all_months = income.index.union(expense.index)

        income = income.reindex(all_months, fill_value=0)
        expense = expense.reindex(all_months, fill_value=0)
        net = income - expense
        months = all_months.astype(str)

        #------ Chart 1: Cashflow ------
        plt.subplot(1, 2, 1)
        plt.plot(months, income.values, label="Income", marker="+")
        plt.plot(months, expense.values, label="Expense", marker="x")
        plt.plot(months, net.values, label="Net Cashflow", marker="o")
        plt.title("Monthly Financial Overview")
        plt.xlabel("Month")
        plt.ylabel("Amount ($)")
        plt.xticks(rotation=45)
        plt.axhline(0)
        plt.legend()

        #------ Chart 2: Category ------
        plt.subplot(1, 2, 2)
        cat_bal.plot(kind="bar", ax=plt.gca())
        plt.title("Category Breakdown")
        plt.xlabel("Month")
        plt.ylabel("Amount ($)")
        plt.xticks(rotation=45)

        #------ Final Layout ------
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.suptitle("Personal Finance Dashboard")

        plt.show()
        







        