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
                is_free=bool(data[3]),
                rent_mode=str(data[4])
            )

            return car
        

    # returns all cars
    def get_all_cars(self) -> []:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'SELECT * FROM TCar ORDER BY _id;')
            data = cur.fetchall()

            if(data is None):
                return None
            
            cars = []
            
            for item in data:
                cars.append(Car(
                    id=int(item[0]),
                    number=str(item[1]),
                    mark_id=int(item[2]),
                    is_free=bool(item[3]),
                    rent_mode=str(item[4])
                ))

            return cars
        
    # add car to db
    def add_car(self, car : Car) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''
                INSERT INTO TCar (_id, _number, _markId, _isFree, _rentMode)
                VALUES ({car.id}, '{car.number}', {car.mark_id}, 
                '{car.is_free}', '{car.rent_mode}');''')
            
    # update car        
    def update_car(self, car : Car) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()         
            cur.execute(f'''
                UPDATE TCar SET _number = '{car.number}', _markId = {car.mark_id},
                _isFree = {car.is_free}, _rentMode = '{car.rent_mode}'
                WHERE _id = {car.id};''')
            
    # remove car        
    def remove_car(self, id : int) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''DELETE FROM TCar WHERE _id = {id};''')