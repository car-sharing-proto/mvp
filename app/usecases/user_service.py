from app.models.user_responses import UserResponse

class UserService():
    def __init__(self, repository):
        self.repository = repository

    def register_user(self, user) -> UserResponse:
        if self.repository.get_user(user.id):
            return UserResponse.AlreadyExists
        self.repository.add_user(user)
        return UserResponse.SuccessfullyAdded

    def get_user_by_id(self, id):
        return self.repository.get_user(id)
    
    def update_user(self, user) -> UserResponse:
        self.repository.update_user(user)
        return UserResponse.SuccessfullyUpdated

    def get_all_users(self):
        return self.repository.get_all_users()

    def remove_user_by_id(self, id) -> UserResponse:
        if not self.repository.get_user(id):
            return UserResponse.NotFound
        self.repository.remove_user(id)
        return UserResponse.SuccessfullyRemoved