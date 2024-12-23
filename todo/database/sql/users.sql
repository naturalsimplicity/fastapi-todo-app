-- name: create-new-user$
insert into users (login, name)
values (:login, :name)
returning id;

-- name: check-login-availability$
select cast(count(*) as bool)
from users
where login = :login;
