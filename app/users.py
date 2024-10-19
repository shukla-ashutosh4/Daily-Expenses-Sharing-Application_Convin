class User:
    def __init__(self, name, email, mobile_number):
        self.name = name
        self.email = email
        self.mobile_number = mobile_number

users = []

def create_user(name, email, mobile_number):
    user = User(name, email, mobile_number)
    users.append(user)
    return user

def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None
