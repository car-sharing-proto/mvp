import psycopg2
import os

from app.models.car import Car

class CarRepository():
    def __init__(self) -> None:
        self.connection_params = {
            'dbname'    :   os.environ['DB_NAME'],
            'user'      :   os.environ['DB_USER'],
            'password'  :   os.environ['DB_PASS'],
            'host'      :   os.environ['SERVER_HOST'],
            'port'      :   os.environ['DB_PORT'] 
        }

    # returns car by id if exists
    def get_car(self, id : int) -> Car:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'SELECT * FROM TCar WHERE _id = {id};')
            data = cur.fetchone()

            if(data is None):
                return None

            car = Car(
                id=int(data[0]),
                number=str(data[1]),
                mark_id=int(data[2]),
                rent_state=str(data[3]),
                rent_mode=str(data[4])
            )

            return car
    
    # add car to db
    def add_car(self, car : Car) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''
                INSERT INTO TCar (_id, _number, _markId, _rentState, _rentMode)
                VALUES ({car.id}, '{car.number}', {car.mark_id}, 
                '{car.rent_state}', '{car.rent_mode}');''')
            
    # update car        
    def update_car(self, car : Car) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()         
            cur.execute(f'''
                UPDATE TCar SET _number = {car.number}, _markId = {car.mark_id},
                _rentState = {car.rent_state}, _rentMode = {car.rent_mode}
                WHERE _id = {car.id};''')
            
    # remove car        
    def remove_car(self, id : int) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''DELETE FROM TCar WHERE _id = {id};''')