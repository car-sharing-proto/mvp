import psycopg2
import os

from app.models.telemetry import Telemetry

class TelemetryRepository():
    def __init__(self) -> None:
        self.connection_params = {
            'dbname'    :   os.environ['DB_NAME'],
            'user'      :   os.environ['DB_USER'],
            'password'  :   os.environ['DB_PASS'],
            'host'      :   os.environ['SERVER_HOST'],
            'port'      :   os.environ['DB_PORT'] 
        }

    # returns telemetry by id if exists
    def get_telemetry(self, id : int) -> Telemetry:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'SELECT * FROM TTelematics WHERE _id = {id};')
            data = cur.fetchone()

            if(data is None):
                return None

            telemetry = Telemetry(
                id=int(data[0]),
                timedate=str(data[1]),
                car_id=int(data[2]),
                data=str(data[3])
            )

            return telemetry
        

     # returns telemetries by car id
    def get_all_telemetries_by_car_id(self, car_id : int) -> []:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'''
                        SELECT * FROM TTelematics WHERE _carId = {car_id} 
                        ORDER BY _timedate DESC;''')
            data = cur.fetchall()

            if(data is None):
                return None
            
            telemetries = []
            
            for item in data:
                telemetries.append(Telemetry(
                    id=int(item[0]),
                    timedate=str(item[1]),
                    car_id=int(item[2]),
                    data=str(item[3])
                ))

            return telemetries
        
    # add telemetry to db
    def add_telemetry(self, telemetry) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''
                INSERT INTO TTelematics (
                    _timedate, _carId, _data
                ) VALUES (%s, %s, %s);
            ''', (
                    telemetry.timedate, 
                    telemetry.car_id, 
                    telemetry.data
                )
            )
            
    def update_telemetry(self, telemetry) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()         
            cur.execute(f'''
                UPDATE TTelematics SET
                _timedate = '{telemetry.timedate}',
                _carId = {telemetry.car_id},
                _data = '{telemetry.data}'
                WHERE _id = {telemetry.id};
            ''')

    def remove_telemetry(self, id) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''DELETE FROM TTelematics WHERE _id = {id};''')

    def get_telemetry_by_time_range(self, car_id, start_time, end_time) -> []:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'''
                SELECT * FROM TTelematics
                WHERE _carId = {car_id} AND _timedate BETWEEN '{start_time}' AND '{end_time}';
            ''')

            telemetry_data = cur.fetchall()

            telemetry_list = []
            for data in telemetry_data:
                telemetry = Telemetry(
                    id=int(data[0]),
                    timedate=str(data[1]),
                    car_id=int(data[2]),
                    data=str(data[3])
                )
                telemetry_list.append(telemetry)

            return telemetry_list


    def get_latest_telemetry_for_car(self, car_id):
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()

            cur.execute(f'''
                SELECT * FROM TTelematics
                WHERE _carId = {car_id}
                ORDER BY _timedate DESC
                LIMIT 1
            ''')

            data = cur.fetchone()

            if data:
                telemetry = Telemetry(
                    id=int(data[0]),
                    timedate=str(data[1]),
                    car_id=int(data[2]),
                    data=str(data[3])
                )
                return telemetry
            else:
                return None