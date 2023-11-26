test_users = []

def user_register(user):
    test_users.append(user)
    print(f"{user.name} is registred with password: {user.password}")

def get_user(user_name):
    for user in test_users:
        if user.name == user_name:
            return user
        
    return False

def get_user_by_id(id):
    for user in test_users:
        if user.id == id:
            return user
        
    return None