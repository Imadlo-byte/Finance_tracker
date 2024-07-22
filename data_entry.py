from datetime import datetime

# Date format
date_format = "%d-%m-%Y"
# Categories - used to translate the input from the user
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    """Function used to get the date from the user

    Args:
        prompt (string): The message shown to the user when asking for a date
        allow_default (bool, optional): If set to True empty input (Enter) causes return Today's date. Defaults to False.

    Returns:
        str: Date in the format dd-mm-yyyy
    """

    # Asking for a date, while showing the argument "prompt"
    date_str = input(prompt)

    # If allow_default set to True and no input given -> Today's date
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    # Try to make a datetime object out of the given string
    # -> if it succeeds, it means that the date was given in the correct format
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)

    # If unable to make a datetime object
    # -> informing the user about incorrect format and asking again about the date
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm--yyyy format")
        return get_date(prompt, allow_default)


def get_amount():
    """Function used to get the amount from the user

    Returns:
        float: Amount of money in the transaction. Must be more than 0.
    """

    # Asking for an amount and trying to make it a float
    # -> If unable to make a float, or the amount <= 0 -> value error
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be non negative, non zero value.")
        return amount

    #
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input(
        "Enter the category ('I' for income or 'E' for expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid category. Please enter 'I' for Income or 'E' for Expense. ")
    return get_category()


def get_description():
    return input("Enter the description (optional): ")
