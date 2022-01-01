-- select * from products
-- where inventory > 0 and cast(price as numeric(18,2)) >= 10;

-- select * from products
-- where inventory = 0 limit 2;

insert into products (name, price, inventory)
values ('tortila', 4, 1000) returning *;

delete from Products where id >= 17;




