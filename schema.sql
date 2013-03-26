drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  uri string not null,
  short_url string not null
);
