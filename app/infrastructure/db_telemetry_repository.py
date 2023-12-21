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
                left_front_door_status=str(data[3]),
                left_rear_door_status=str(data[4]),
                right_front_door_status=str(data[5]),
                right_rear_door_status=str(data[6]),
                trunk_status=str(data[7]),
                hood_status=str(data[8]),
                geoposition=str(data[9]),
                immobilizer_status=str(data[10]),
                central_locking_status=str(data[11]),
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
                    left_front_door_status=str(item[3]),
                    left_rear_door_status=str(item[4]),
                    right_front_door_status=str(item[5]),
                    right_rear_door_status=str(item[6]),
                    trunk_status=str(item[7]),
                    hood_status=str(item[8]),
                    geoposition=str(item[9]),
                    immobilizer_status=str(item[10]),
                    central_locking_status=str(item[11]),
                ))

            return telemetries
        
    # add telemetry to db
    def add_telemetry(self, telemetry) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()
            cur.execute(f'''
                INSERT INTO TTelematics (
                    _timedate, _carId,
                    _leftFrontDoorStatus, _rightFrontDoorStatus,
                    _leftRearDoorStatus, _rightRearDoorStatus,
                    _hood, _trunk, _geoposition,
                    _immobilizerStatus, _centralLockingStatus
                ) VALUES (
                    '{telemetry.timedate}', {telemetry.car_id},
                    '{telemetry.left_front_door_status}', '{telemetry.right_front_door_status}',
                    '{telemetry.left_rear_door_status}', '{telemetry.right_rear_door_status}',
                    '{telemetry.hood_status}', '{telemetry.trunk_status}', '{telemetry.geoposition}',
                    '{telemetry.immobilizer_status}', '{telemetry.central_locking_status}'
                );
            ''')
            
    def update_telemetry(self, telemetry) -> None:
        with psycopg2.connect(**self.connection_params) as con:
            cur = con.cursor()         
            cur.execute(f'''
                UPDATE TTelematics SET
                _timedate = '{telemetry.timedate}',
                _carId = {telemetry.car_id},
                _leftFrontDoorStatus = '{telemetry.left_front_door_status}',
                _rightFrontDoorStatus = '{telemetry.right_front_door_status}',
                _leftRearDoorStatus = '{telemetry.left_rear_door_status}',
                _rightRearDoorStatus = '{telemetry.right_rear_door_status}',
                _hood = '{telemetry.hood_status}',
                _trunk = '{telemetry.trunk_status}',
                _geoposition = '{telemetry.geoposition}',
                _immobilizerStatus = '{telemetry.immobilizer_status}',
                _centralLockingStatus = '{telemetry.central_locking_status}'
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
                    left_front_door_status=str(data[3]),
                    right_front_door_status=str(data[4]),
                    left_rear_door_status=str(data[5]),
                    right_rear_door_status=str(data[6]),
                    trunk_status=str(data[7]),
                    hood_status=str(data[8]),
                    geoposition=str(data[9]),
                    immobilizer_status=str(data[10]),
                    central_locking_status=str(data[11])
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
                    left_front_door_status=str(data[3]),
                    right_front_door_status=str(data[4]),
                    left_rear_door_status=str(data[5]),
                    right_rear_door_status=str(data[6]),
                    trunk_status=str(data[7]),
                    hood_status=str(data[8]),
                    geoposition=str(data[9]),
                    immobilizer_status=str(data[10]),
                    central_locking_status=str(data[11])
                )
                return telemetry
            else:
                return None