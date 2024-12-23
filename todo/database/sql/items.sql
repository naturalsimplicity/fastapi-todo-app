-- name: create-new-item$
insert into items (user_id, title, description, completed)
values (:user_id, :title, :description, :completed)
returning id;

-- name: get-all-items
select id, user_id, title, description, completed
from items;

-- name: get-user-items
select i.id, i.user_id, i.title, i.description, i.completed
from items i
join users u on i.user_id = u.id
where u.login = :login;

-- name: check-if-item-exists$
select count(*)
from items
where id = :item_id;

-- name: get-item^
select id, user_id, title, description, completed
from items
where id = :item_id;

-- name: update-item!
update items
set user_id = :user_id,
    title = :title,
    description = :description,
    completed = :completed
where id = :item_id;

-- name: delete-item!
delete from items
where id = :item_id;

-- name: get_item_creator$
select user_id
from items
where id = :item_id;
