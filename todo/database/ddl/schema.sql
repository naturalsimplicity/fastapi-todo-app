-- name: create-table-users#
create table users
(
    id integer primary key autoincrement,
    login varchar(255) not null unique,
    name varchar(255) not null
);

-- name: create-table-items#
create table items
(
    id integer primary key autoincrement,
    user_id integer not null references users(id),
    title varchar(255) not null,
    description text,
    completed bool not null
);
