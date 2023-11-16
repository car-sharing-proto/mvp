drop table if exists TClient;
drop table if exists TRole;
drop table if exists TComment;
drop table if exists TCarMark;
drop table if exists TRentStatus;

create table TComment (
    _id integer,
    _content text not null,
    _timedate text not null,

    primary key (_id)
);

create table TRole (
    _name text not null,

    primary key (_name)
);

create table TClient (
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