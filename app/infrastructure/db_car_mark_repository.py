import psycopg2
import os

from app.models.car_mark import CarMark

class CarMarkRepository():
    def __init__(self) -> None:
        self.connection_params = {
            'dbname'    :   os.environ['DB_NAME'],
            'user'      :   os.environ['DB_USER'],
            'password'  :   os.environ['DB_PASS'],
            'host'      :   os.environ['SERVER_HOST'],
            'port'      :   os.environ['DB_PORT'] 
        }

    # returns car mark by id if exists
    def get_car_mark(self, id : int) -> CarMark:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'SELECT * FROM TCarMark WHERE _id = {id};')
            data = cur.fetchone()

            if(data is None):
                return None

            car_mark = CarMark(
                id=int(data[0]),
                model=str(data[1]),
                mark=str(data[2]),
                color=str(data[3])
            )

            return car_mark
    
    # add car mark to db
    def add_car_mark(self, car_mark : CarMark) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''
                INSERT INTO TCarMark (_id, _model, _mark, _color)
                VALUES ({car_mark.id}, '{car_mark.model}', {car_mark.mark}, 
                '{car_mark.color}');''')
            
    # update car mark  
    def update_car_mark(self, car_mark : CarMark) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()         
            cur.execute(f'''
                UPDATE TCarMark SET _model = {car_mark.model}, 
                _mark = {car_mark.mark},
                _color = {car_mark.color}
                WHERE _id = {car_mark.id};''')
            
    # remove car mark        
    def remove_car_mark(self, id : int) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''DELETE FROM TCarMark WHERE _id = {id};''')