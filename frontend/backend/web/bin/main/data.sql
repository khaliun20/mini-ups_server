insert into packages( packages_id, state, trucking_num, truck_id, username, warehouse_id, x, y)
values(10001, 'delivering', 123, 1, 'abc', 1, 2, 1);

insert into packages( packages_id, state, trucking_num, truck_id, username, warehouse_id, x, y)
values(10002, 'delivering', 124, 1, 'abc', 1, 2, 5);

insert into packages( packages_id, state, trucking_num, truck_id, username, warehouse_id, x, y)
values(10003, 'delivering', 125, 1, 'abc', 1, 3, 4);

insert into packages( packages_id, state, trucking_num, truck_id, username, warehouse_id, x, y)
values(10004, 'delivering', 126, 1, '', 1, 3, 4);

insert into packages( packages_id, state, trucking_num, truck_id, username, warehouse_id, x, y)
values(10005, 'delivering', 127, 1, '', 1, 3, 4);

insert into packages( packages_id, state, trucking_num, truck_id, username, warehouse_id, x, y)
values(10006, 'in_warehouse', 128, 1, '', 1, 3, 4);

insert into items(id, description, quantity, trucking_num)
values(101, 'item1', 1, 123);

insert into items(id, description, quantity, trucking_num)
values(102, 'item2', 2, 123);

insert into items(id, description, quantity, trucking_num)
values(103, 'item3', 1, 124);

insert into items(id, description, quantity, trucking_num)
values(104, 'item4', 1, 123);

insert into truck(truck_id, state, wid, world_given_state, x, y)
values(2, 'TRAVELING', 1, 'TRAVELING', 25, -25);

insert into truck(truck_id, state, wid, world_given_state, x, y)
values(1, 'TRAVELING', 1, 'TRAVELING', 10, 20);

insert into users(user_id, password, state, username)
values(101,  'abc', '',  'abc');

UPDATE packages SET state = 'preparing_for_pickup' WHERE packages_id = 10004;
UPDATE packages SET state = 'delivered' WHERE packages_id = 10002;
UPDATE packages SET state = 'arrive_warehouse' WHERE packages_id = 10003;
UPDATE packages SET state = 'in_warehouse' WHERE packages_id = 10005;




