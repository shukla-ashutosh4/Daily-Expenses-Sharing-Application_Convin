# utils.py

def validate_percentage(participants):
    total_percentage = sum(p['percentage'] for p in participants)
    return total_percentage == 100

def validate_exact(total_amount, participants):
    total = sum(p['amount'] for p in participants)
    return total == total_amount
