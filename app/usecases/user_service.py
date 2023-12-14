class UserService():
    def __init__(self, repository):
        self.repository = repository

    def register_user(self, user):
        self.repository.add_user(user)

    def get_user_by_id(self, id):
        return self.repository.get_user(id)
    
    def update_user(self, user):
        self.repository.update_user(user)

    def remove_user_by_id(self, id):
        self.repository.remove_user(id)