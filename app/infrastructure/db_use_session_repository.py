import psycopg2
import os

from app.models.use_session import UseSession

class UseSessionRepository():
    def __init__(self) -> None:
        self.connection_params = {
            'dbname'    :   os.environ['DB_NAME'],
            'user'      :   os.environ['DB_USER'],
            'password'  :   os.environ['DB_PASS'],
            'host'      :   os.environ['SERVER_HOST'],
            'port'      :   os.environ['DB_PORT'] 
        }

    # returns use session by id if exists
    def get_session(self, id : int) -> UseSession:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'SELECT * FROM TUseSession WHERE _id = {id};')
            data = cur.fetchone()

            if(data is None):
                return None

            session = UseSession(
                id=int(data[0]),
                start_time=str(data[1]),
                end_time=str(data[2]),
                car_id=int(data[3]),
                user_id=int(data[4]),
                state=str(data[5])
            )

            return session
        
    # returns all use sessions by user id if exists
    def get_sessions_by_user_id(self, id : int) -> []:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'SELECT * FROM TUseSession WHERE _userId = {id};')
            data = cur.fetchall()

            if(data is None):
                return None

            sessions = []

            for item in data:
                sessions.append(UseSession(
                    id=int(item[0]),
                    start_time=str(item[1]),
                    end_time=str(item[2]),
                    car_id=int(item[3]),
                    user_id=int(item[4]),
                    state=str(item[5])
                ))

            return sessions
        
    # returns all use sessions by user id if exists
    def get_sessions_by_car_id(self, id : int) -> []:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'SELECT * FROM TUseSession WHERE _carId = {id} ORDER BY _id;')
            data = cur.fetchall()

            if(data is None):
                return None

            sessions = []

            for item in data:
                sessions.append(UseSession(
                    id=int(item[0]),
                    start_time=str(item[1]),
                    end_time=str(item[2]),
                    car_id=int(item[3]),
                    user_id=int(item[4]),
                    state=str(item[5])
                ))

            return sessions
        
    def get_last_session_by_car_id(self, id: int) -> UseSession | None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'''
                SELECT * FROM TUseSession 
                WHERE _carId = {id} 
                ORDER BY _startTime DESC 
                LIMIT 1;
            ''')
            data = cur.fetchone()

            if not data:
                return None

            session = UseSession(
                id=int(data[0]),
                start_time=str(data[1]),
                end_time=str(data[2]),
                car_id=int(data[3]),
                user_id=int(data[4]),
                state=str(data[5])
            )

            return session
    
    # add use session to db
    def add_session(self, session : UseSession) -> int:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''
                INSERT INTO TUseSession (_startTime, _endTime, _carId, _userId, _state)
                VALUES ('{session.start_time}', '{session.end_time}',
                {session.car_id}, {session.user_id}, '{session.state.value}') RETURNING _id;''')
            return int(cur.fetchone()[0])
            
    # update use session        
    def update_session(self, session : UseSession) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()         
            cur.execute(f'''
                UPDATE TUseSession SET _startTime = '{session.start_time}',
                _endTime = '{session.end_time}', _carId = {session.car_id},
                _userId = {session.user_id}, _state = '{session.state.value}'
                WHERE _id = {session.id};''')