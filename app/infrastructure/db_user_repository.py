from app.models.user import User

class UserRepository():
    def __init__(self, cursor) -> None:
        self.cursor = cursor

    # returns user by id if exists
    def get_user(self, id):
        self.cursor.execute(
            'SELECT * FROM TUser WHERE (id = {0})'.format(id))
        
        data = self.cursor.fetchone()

        if(data is None):
            return None
        
        user_id, user_role, user_name, user_pass = data
        user = User(user_id, user_role, user_name, user_pass)
        
        return user
    
    # add user to db
    def add_user(self, user):
        self.cursor.execute(
            'INSERT INTO TUser (_id, _role, _name, _pass) ' +
            'VALUES ({0}, {1}, {2}, {3}});'.format(
                user.id,
                user.role, 
                user.name,
                user.password))