drop table if exists stubs;
create table stubs (
  url_stub string primary key not null,
  url_source string not null,
  create_date datetime default current_timestamp
);
drop table if exists users;
create table users (
    id integer primary key,
    username string not null,
    password string not null,
    email string not null
);
drop table if exists requests;
create table requests (
    id integer primary key,
    remote_addr string not null,
    stub string not null
)
