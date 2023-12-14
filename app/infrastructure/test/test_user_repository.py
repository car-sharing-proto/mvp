class UserRepository():
    def __init__(self):
        self.data = []
    

    def get_user(self, id):
        for user in self.data:
            if user.id == id:
                return user
            
        return None
    
    
    def add_user(self, user):
        self.data.append(user)

    
    def update_user(self, user):
        for i in range(0, len(self.data)):
            if self.data[i].id == user.id:
                self.data[i] = user

    def remove_user(self, id):
        index = -1
        for i in range(0, len(self.data)):
            if self.data[i].id == id:
                index = i

        if index >= 0:
            del self.data[i]


def funny_test():
    class User():
        def __init__(self, id, name) -> None:
            self.id = id
            self.name = name

    user = User(0, "kek")
    repo = UserRepository()
    repo.add_user(user)
    print(repo.get_user(0).name)
    new_user = User(0, "kek2")
    repo.update_user(new_user)
    print(repo.get_user(0).name)
    print(len(repo.data))
    repo.remove_user(1)
    print(len(repo.data))
    repo.remove_user(0)
    print(len(repo.data))