import psycopg2
import os

from app.models.user import User

class UserRepository():
    def __init__(self) -> None:
        self.connection_params = {
            'dbname'    :   os.environ['DB_NAME'],
            'user'      :   os.environ['DB_USER'],
            'password'  :   os.environ['DB_PASS'],
            'host'      :   os.environ['SERVER_HOST'],
            'port'      :   os.environ['DB_PORT'] 
        }

    # returns user by id if exists
    def get_user(self, id : int) -> User:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM TUser WHERE (_id = {0});'.format(id))
            data = cur.fetchone()

            if(data is None):
                return None

            user = User(
                int(data[0]),
                str(data[1]),
                str(data[2]), 
                str(data[3])
            )

            return user
        
    # returns all users
    def get_all_users(self) -> []:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM TUser ORDER BY _id;')
            data = cur.fetchall()

            if(data is None):
                return None
            
            users = []
            
            for item in data:
                users.append(User(
                    int(item[0]),
                    str(item[1]),
                    str(item[2]), 
                    str(item[3])
                 ))

            return users
    
    # add user to db
    def add_user(self, user : User) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO TUser (_id, _role, _name, _pass) "+
                "VALUES ({0}, '{1}', '{2}', '{3}');".format(
                    user.id,
                    user.role, 
                    user.name,
                    user.password))
            
    # update user        
    def update_user(self, user : User) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE TUser SET _role = '{1}', _name = '{2}', _pass = '{3}'
                WHERE _id = {0};'''.format(
                    user.id,
                    user.role, 
                    user.name,
                    user.password))
            
    # remove user        
    def remove_user(self, id : int) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''DELETE FROM TUser WHERE _id = {id};''')