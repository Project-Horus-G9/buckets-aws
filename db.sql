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
