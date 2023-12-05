drop table if exists TUseSession;
drop table if exists TUser;
drop table if exists TCar;
drop table if exists TComment;
drop table if exists TCarMark;
drop table if exists TRentStatus;
drop table if exists TTelematics;

begin;
DO $$
begin
    if not exists (
        select 1 
        from pg_type 
        where typname = 'door_status'
    ) 
    then
    create type door_status as enum (
        'opened', 
        'closed'
    );
    end if;

    if not exists (
        select 1 
        from pg_type 
        where typname = 'immobilizer_status'
    ) 
    then
    create type immobilizer_status as enum (
        'on', 
        'off'
    );
    end if;

    if not exists (
        select 1 
        from pg_type 
        where typname = 'central_locking_status'
    ) 
    then
    create type central_locking_status as enum (
        'on', 
        'off'
    );
    end if;
end
$$;
commit;

create table TComment (
    _id integer,
    _content text not null,
    _timedate timestamp not null,

    primary key (_id)
);

create table TUser (
    _id integer,
    _role text not null,
    _name text not null,
    _pass text not null,

    primary key (_id)
);

create table TCarMark (
    _id integer,
    _model text not null,
    _mark text not null,
    _color text not null,

    primary key (_id)
);

create table TRentStatus (
    _status text not null,

    primary key (_status)
);

create table TCar (
    _id integer,
    _number text not null,
    _mileage integer,
    _markId integer,
    _status text,

    primary key (_id),
    foreign key (_markId) references TCarMark (_id),
    foreign key (_status) references TRentStatus (_status)
);

create table TUseSession (
    _id integer,
    _startTime timestamp not null,
    _endTime timestamp not null,
    _carId integer,
    _userId integer,

    primary key (_id),
    foreign key (_carId) references TCar (_id),
    foreign key (_userId) references TUser (_id)
);

create table TTelematics (
    _id integer,
    _timedate timestamp not null,
    _carId integer,
    -- door status --
    _leftFrontDoorStatus door_status,
    _rightFrontDoorStatus door_status,
    _leftRearDoorStatus door_status,
    _rightRearDoorStatus door_status,
    _hood door_status,
    _trunk door_status,
    -- geoposition --
    _geoposition text not null,
    -- immobilizer --
    _immobilizerStatus immobilizer_status,
    -- central locking --
    _centralLockingStatus central_locking_status,
    
    primary key (_id),
    foreign key (_carId) references TCar (_id)
);