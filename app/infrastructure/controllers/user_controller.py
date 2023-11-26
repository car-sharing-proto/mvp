class UserController():
    def _init__(self, repository):
        self.reposiory = repository

    def get_user_by_id(self, id):
        return self.reposiory.get_user_by_id(id)