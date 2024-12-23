
import json
import os


def add_expense(expenses, description, amount):
    expenses.append({"description": description, "amount": amount})
    print(f"Added expense: {description}, Amount: {amount}")

def get_total_expenses(expenses):
    sum = 0
    for expense in expenses:
        sum += expense["amount"]
    return sum

def get_balance(budget, expenses):
    return budget - get_total_expenses(expenses)

def show_budget_details(budget, expenses):
    print("\n------------------------------")
    print(f"\nTotal Budget: {budget}")
    print("Expenses:")
    for expense in expenses:
        print(f"- {expense['description']}: {expense['amount']}")
    print(f"Total spent: {get_total_expenses(expenses)}")
    print(f"Remaining Budget: {get_balance(budget, expenses)}")
    print("\n------------------------------")



def load_budget_data(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data["initial_budget"], data["expenses"]
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error loading file: {filepath}. Returning defaults.")
        return 0, []
    
    

def save_budget_details(filepath, initial_budget, expenses):
    data = {
        'initial_budget': initial_budget,
        'expenses': expenses
    }
    
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


def create_new_budget_file(filepath):
    # Ask the user for a new budget
    new_budget = float(input("Enter the new initial budget: "))
    new_expenses = []  # Start with an empty list of expenses
    
    # Confirm if the user really wants to create the new file
    confirm = input(f"Are you sure you want to create a new file with a budget of {new_budget}? (y/n): ").lower()
    
    if confirm == 'y':
        # Save the new file
        save_budget_details(filepath, new_budget, new_expenses)
        print(f"Created a new budget file with a budget of {new_budget}.")
        return new_budget, new_expenses
    else:
        print("Operation cancelled. Returning to the main menu.")
        return None, None  # Return None to indicate the process was cancelled

def delete_budget_data(filepath):
    try:
        os.remove(filepath)
        print(f"Deleted file: {filepath}")
    except FileNotFoundError:
        print(f"The file {filepath} does not exist.")


def main():
    print("Welcome to the Budget app")
    filepath = 'budget_data.json'
    initial_budget, expenses = load_budget_data(filepath)
    if initial_budget == 0:
        initial_budget = float(input("Please enter your initial budget: "))
    budget = initial_budget

    while True:
        print("\nWhat would you like to do?")
        print("1. Add an expense")
        print("2. Show budget details")
        print("3. Create a new budget file (keep old file intact)")
        print("4. Delete saved data (Delete JSON file)")
        print("5. View old budget file")
        print("6. Exit")
        print("0. Go back to the main menu or exit")  # Add an option to go back or exit
        
        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            description = input("Enter expense description: ")
            amount = float(input("Enter expense amount: "))
            add_expense(expenses, description, amount)
        elif choice == "2":
            show_budget_details(budget, expenses)
        elif choice == "3":
            # Create a new budget file with a new budget and reset expenses
            new_filepath = input("Enter the new file name (e.g., new_budget.json): ")
            create_new_budget_file(new_filepath)
            # After creating a new file, reset current budget and expenses
            initial_budget, expenses = 0, []
            budget = initial_budget
        elif choice == "4":
            delete_budget_data(filepath)
            # Optionally, reset the app after file deletion (reloads the app from scratch)
            initial_budget, expenses = 0, []
            budget = initial_budget
        elif choice =="5":
            # Option to load and view the old file's information
            old_filepath = input("Enter the file name to view (e.g., budget_data.json): ")
            # Check if the file exists
            if os.path.exists(old_filepath):
                initial_budget, expenses = load_budget_data(old_filepath)
                budget = initial_budget
                print(f"Loaded old file: {old_filepath}")
                show_budget_details(budget, expenses)
            else:
                print(f"Error: The file '{old_filepath}' does not exist. Please check the file name and try again.")
        elif choice == "6":
            save_budget_details(filepath, initial_budget, expenses)
            print("Exiting Budget App. Goodbye!")
            break
        elif choice == "0":
            print("Going back to the main menu or exiting the app.")
            break  # Exit the current loop (or break back to a previous state)
        else:
            print("Invalid choice, please choose again.")

if __name__ == "__main__":
    main()