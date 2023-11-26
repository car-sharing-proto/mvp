class UserRepository():
    def __init__(self):
        self.data = []
    

    def get_user_by_id(self, id):
        for user in self.data:
            if user.id == id:
                return user
            
        return None
    

    def add_user(self, user):
        self.data.append(user)