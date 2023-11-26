class UserService():
    def __init__(self, repository):
        self.repository = repository

    def register_user(self, user):
        self.repository.add_user(user)