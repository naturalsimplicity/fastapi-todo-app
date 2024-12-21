-- name: create-new-item$
insert into items (user_id, title, description, completed)
values (:user_id, :title, :description, :completed)
returning id;

-- name: get-all-items
select id, user_id, title, description, completed
from items;

-- name: get-user-items
select id, user_id, title, description, completed
from items
where user_id = :user_id;

-- name: check-if-item-exists$
select count(*)
from item
where id = :item_id;

-- name: get-item^
select id, user_id, title, description, completed
from items
where id = :item_id;

-- name: update-item!
update items
set title = :title,
    description = :description,
    completed = :completed
where id = :item_id;

-- name: delete-item!
delete from items
where id = :item_id;
