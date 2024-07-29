import pandas as pd
import csv
from datetime import datetime

from data_entry import get_category, get_amount, get_date, get_description, get_attribute

import matplotlib.pyplot as plt


class CSV:
    """Class build to work with the csv file: initialize, add entry, get transactions

    """

    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """Check if the csv. file named CSV_FILE exists, and if not making one
        """

        # Try to open and read csv file, if it doesn't exists
        # -> FileNotFoundError -> saving new csv. file with the columns named cls.COLUMNS
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """Adds new information into the csv. file

        Args:
            date (str): Date in the format dd-mm-yyyy
            amount (float): Amount of money in the transaction. Must be more than 0.
            category (str): 'Income' or 'Expense'
            description (str): Description of the transaction
        """

        # Save given arguments in the form of dictionary,
        # which to every argument connects with the key from the COLUMNS
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        # Opens the csv. file to save the information inside the dictionary in the form of the new row
        with open(cls.CSV_FILE, "a", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def delete(cls):
        """Deletes the chosen entry from the file
        """

        # Read the file
        df = pd.read_csv(cls.CSV_FILE)

        # Shows the transactions
        print("Transactions saved in the file: \n")
        print(df)

        # Asks the user which row to delete
        try:
            choice = int(input("\nWhich transaction would you like to delete from the file?\nType the number (Enter if you want to get back to the menu): "))
                
            if not choice:
                return

            if choice not in range(df["date"].count()):
                raise ValueError
            
            # Delete the row
            df = df.drop([choice])

            # Save the file
            df.to_csv(cls.CSV_FILE, index= False)
                
        except ValueError:
            print("Invalid choice. Try again. ")
            return cls.delete()
    
    @classmethod
    def change(cls):
        # Read the file
        df = pd.read_csv(cls.CSV_FILE)

        # Shows the transactions
        print("Transactions saved in the file: \n")
        print(df)
        try:
            choice = int(input("\nWhich transaction would you like to modify?\nType the number (Enter if you want to get back to the menu): "))
                
            if not choice:
                return

            if choice not in range(df["date"].count()):
                raise ValueError
            
            print(f"\nYou are modifying the row:\n{df.iloc[[choice]]}")

            # Get the column to change
            attribute = get_attribute()

            print(f"\nCurrent {attribute}: {df.at[df.index[choice], attribute]}")

            # Get new value which will replace the old
            if attribute == "date":
                new_change = get_date("Enter the new date of the transaction (Enter for today's date): ")
            elif attribute == "amount":
                new_change = get_amount()
            elif attribute == "category":
                new_change = get_category()
            else:
                new_change = get_description()

            # Change the position in the dataFrame
            df.at[df.index[choice], attribute] = new_change

            # Save the file
            df.to_csv(cls.CSV_FILE, index= False)
        
        except ValueError:
            print("Invalid choice. Try again. ")
            return cls.change()
            


    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Shows the user the transactions from the chosen time range.
        Prints the transactions in the chosen time range.

        Args:
            start_date (str): Starting date of the time range
            end_date (_type_): Ending date of the time range 

        Returns:
            DataFrame: A Pandas DataFrame is a 2 dimensional data structure, like a 2 dimensional array, or a table with rows and columns.
        """

        # Saving the information from the csv. file in the form of DataFrame(Pandas)
        df = pd.read_csv(cls.CSV_FILE)

        # Changing the data type inside of the "date" column from string to DateTime(pandas).
        # Doing the same with the arguments
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Selecting the rows inside of the df based on the condition: start date <= ["date"] column <= end column
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        # Sorting the information based on the dates
        filtered_df = filtered_df.sort_values(by = ["date"])

        # Printing out the data
        if filtered_df.empty:
            print("No transaction found in the given date range. ")
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={
                  "date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"]
                                       == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"]
                                        == "Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total income: ${total_income:.2f}")
            print(f"Total expanse: ${total_expense:.2f}")
            print(f"Net savings: ${(total_income - total_expense):.2f}")

            # returning the filtered_df -> might be used in the creation of the plot, if the user wishes to see it
            return filtered_df


def add():
    """Get the information about the transaction from the user, and add it to the csv. file
    """

    # Checks if the csv. file exists, creates it if not. Gets the required information and saves it.
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry(date, amount, category, description)


def plot_transaction(df):
    """Creates the plot of the income and expenses

    Args:
        df (DataFrame): A Pandas DataFrame is a 2 dimensional data structure, like a 2 dimensional array, or a table with rows and columns.
    """

    # Assigning the ["date"] column as an index
    df.set_index('date', inplace=True)

    # Creating two more data frames based on the 'category'
    income_df = (df[df["category"] == "Income"]
                 .resample("D")
                 .sum()
                 .reindex(df.index, fill_value=0)
                 )

    expense_df = (df[df["category"] == "Expense"]
                  .resample("D")
                  .sum()
                  .reindex(df.index, fill_value=0)
                  )
    

    # Creating the plot using matplotlib
    # Creating the figure for a plot, setting its size
    plt.figure(figsize=(10, 5))

    # Plot the different lines
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")

    # Labels on the graph
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and expenses over time")

    # Enables the legend
    plt.legend()

    # Enables the grid
    plt.grid(True)

    # Shows the plot
    plt.show()


def main():
    # The while loop which can be exited only with the function break
    while True:

        # Prints out the possible choices
        print("\n1. Add a new transaction.")
        print("2. View transactions and summary within a date range.")
        print("3. Change the transaction's details")
        print("4. Delete the transaction from the file")
        print("5. Exit.")
        choice = input("Enter your choice (1-5): ")

        # Based on the user input right set of functions is applied
        if choice == "1":
            add()

        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            
            while True:
                choice = input("Would you like to see the plot? \nType: 'y' - yes or 'n' - no: ").lower()

                if choice == 'y':
                    plot_transaction(df)
                    break
                elif choice == 'n':
                    break
                else:
                    print("Invalid choice. Try again. ")
        
        elif choice == '3':
            CSV.change()

        elif choice == '4':
            CSV.delete()

        elif choice == '5':
            print("Exiting...")
            break

        # If the input is none of the proposed, print the message
        else:
            print("Invalid choice. Enter the number from 1 to 5.")
    

if __name__ == "__main__":
    main()
