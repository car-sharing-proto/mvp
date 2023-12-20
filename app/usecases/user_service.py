from app.models.user_responses import UserResponse

class UserService():
    def __init__(self, repository):
        self.repository = repository

    def register_user(self, user) -> str:
        if self.repository.get_user(user.id):
            return UserResponse.AlreadyExists
        self.repository.add_user(user)
        return UserResponse.SuccessfullyAdded

    def get_user_by_id(self, id):
        return self.repository.get_user(id)
    
    def update_user(self, user) -> str:
        self.repository.update_user(user)
        return UserResponse.SuccessfullyUpdated

    def get_all_users(self):
        return self.repository.get_all_users()

    def remove_user_by_id(self, id):
        self.repository.remove_user(id)