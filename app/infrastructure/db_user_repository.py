import psycopg2
import os

from dotenv import load_dotenv
from app.models.user import User

class UserRepository():
    def __init__(self) -> None:
        load_dotenv()

    # returns user by id if exists
    def get_user(self, id):
        con = psycopg2.connect(
                dbname=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASS'],
                host=os.environ['SERVER_HOST'],
                port=os.environ['DB_PORT']
            )
        cur = con.cursor()
        cur.execute('SELECT * FROM TUser WHERE (_id = {0});'.format(id))
        data = cur.fetchone()

        if(data is None):
            return None
        
        user_id, user_role, user_name, user_pass = data
        user = User(
            int(user_id),
            str(user_role),
            str(user_name), 
            str(user_pass)
        )
        con.close()
        return user
    
    # add user to db
    def add_user(self, user):
        con = psycopg2.connect(
                dbname=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASS'],
                host=os.environ['SERVER_HOST'],
                port=os.environ['DB_PORT']
            )
        cur = con.cursor()
        cur.execute(
            "INSERT INTO TUser (_id, _role, _name, _pass) "+
            "VALUES ({0}, '{1}', '{2}', '{3}');".format(
                user.id,
                user.role, 
                user.name,
                user.password))
        con.commit()
        con.close()