drop table if exists TUseSession;
drop table if exists TUser;
drop table if exists TRole;
drop table if exists TCar;
drop table if exists TComment;
drop table if exists TCarMark;
drop table if exists TRentStatus;
drop table if exists TTelematics;

create table TComment (
    _id integer,
    _content text not null,
    _timedate timestamp not null,

    primary key (_id)
);

create table TRole (
    _name text not null,

    primary key (_name)
);

create table TUser (
    _id integer,
    _role text not null,

    primary key (_id),
    foreign key (_role) references TRole (_name)
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
    _leftFrontDoorStatus text check (
        _leftFrontDoorStatus in (
            'closed', 
            'opened'
        )
    ), 
    _rightFrontDoorStatus text check (
        _rightFrontDoorStatus in (
            'closed', 
            'opened'
        )
    ), 
    _leftRearDoorStatus text check (
        _leftRearDoorStatus in (
            'closed',
            'opened'
        )
    ), 
    _rightRearDoorStatus text check (
        _rightRearDoorStatus in (
            'closed',
            'opened'
        )
    ), 
    _hood text check (
        _hood in (
            'closed', 
            'opened'
        )
    ), 
    _trunk text check (
        _trunk in (
            'closed', 
            'opened'
        )
    ), 
    -- geoposition --
    _geoposition text not null,
    -- immobilizer --
    _immobilizerStatus text check (
        _immobilizerStatus in (
            'on', 
            'off'
        )
    ), 
    -- central locking --
    _centralLockingStatus text check (
        _centralLockingStatus in (
            'on', 
            'off'
        )
    ), 

    primary key (_id),
    foreign key (_carId) references TCar (_id)
);