create database horus;

use horus;

create table voltagem (
    id int primary key auto_increment,
    dataMedicao varchar(255) not null,
    painel varchar(255) not null,
    voltagem float not null
);


create table luminosidade (
    id int primary key auto_increment,
    dataMedicao varchar(255) not null,
    luminosidade float not null
);

create table potencia (
    id int primary key auto_increment,
    dataMedicao varchar(255) not null,
    potencia float not null
);

create table clima (
    id int primary key auto_increment,
    dataMedicao varchar(255) not null,
    clima varchar(255) not null,
    tempo varchar(255) not null
);

create table temperaturaExterna (
    id int primary key auto_increment,
    dataMedicao varchar(255) not null,
    temperatura float not null
);