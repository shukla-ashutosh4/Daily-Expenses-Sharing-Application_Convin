# expenses.py

class Expense:
    def __init__(self, description, total_amount, split_type, participants):
        self.description = description
        self.total_amount = total_amount
        self.split_type = split_type
        self.participants = participants

expenses = []

def add_expense(description, total_amount, split_type, participants):
    expense = Expense(description, total_amount, split_type, participants)
    expenses.append(expense)
    return expense

def split_equal(total_amount, participants):
    split_amount = total_amount / len(participants)
    return {p['email']: split_amount for p in participants}

def split_exact(participants):
    return {p['email']: p['amount'] for p in participants}

def split_percentage(total_amount, participants):
    splits = {}
    for p in participants:
        splits[p['email']] = (p['percentage'] / 100) * total_amount
    return splits

def get_user_expenses(email):
    user_expenses = []
    for expense in expenses:
        for participant in expense.participants:
            if participant['email'] == email:
                user_expenses.append(expense)
    return user_expenses
