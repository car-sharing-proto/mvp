begin;
DO $$
begin
    if not exists (
        select 1 
        from pg_type 
        where typname = 'session_state'
    ) 
    then
    create type session_state as enum (
        'reserved',     -- машина забронирована
        'inspection',   -- осмотр авто
        'paused',       -- режим ожидания
        'active',       -- активная аренда
        'finished'      -- доступна к бронированию
    );
    end if;

    if not exists (
        select 1 
        from pg_type 
        where typname = 'rent_mode'
    ) 
    then
    create type rent_mode as enum (
        'service', 
        'rent'
    );
    end if;
end
$$;
commit;

create table if not exists TComment (
    _id integer,
    _content text not null,
    _timedate timestamp not null,

    primary key (_id)
);

create table if not exists TUser(
    _id integer,
    _role text not null,
    _name text not null,
    _pass text not null,

    primary key (_id)
);

create table if not exists TCarMark (
    _id integer,
    _model text not null,
    _mark text not null,
    _color text not null,

    primary key (_id)
);

create table if not exists TCar (
    _id integer,
    _number text not null,
    _markId integer,
    _isFree boolean,
    _rentMode rent_mode,

    primary key (_id),
    foreign key (_markId) references TCarMark (_id)
);

create table if not exists TUseSession (
    _id bigserial,
    _startTime timestamp not null,
    _endTime timestamp not null,
    _carId integer,
    _userId integer,
    _state session_state,

    primary key (_id),
    foreign key (_carId) references TCar (_id),
    foreign key (_userId) references TUser (_id)
);

create table if not exists TTelematics (
    _id bigserial,
    _timedate timestamp not null,
    _carId integer,
    _data text,
    
    primary key (_id),
    foreign key (_carId) references TCar (_id)
);

INSERT INTO TUser (_id, _name, _role, _pass) 
VALUES (0, 'moxcelix', 'admin', 'aboba');
