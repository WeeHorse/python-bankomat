create database bankomat;

create table if not exists public.accounts
(
    id         serial
        primary key,
    first_name text              not null,
    last_name  text              not null,
    ssn        text              not null
        unique,
    balance    integer default 0 not null,
    account_nr text              not null
        unique
);
