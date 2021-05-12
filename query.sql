-- insert data into account table
INSERT INTO account (email, acc_status, warnings, password)
VALUES ("doe@example.com", 2, 4, "doe124");
INSERT INTO account (email, acc_status, warnings, password)
VALUES ("jhondoe@example.com", 1, 2, "jhondoe124");

-- insert data into personal_acc table
INSERT INTO personal_acc ( account_id, first_name, last_name, address, balance, credit_card)
VALUES (5, "Jhon", "Doe", "New York, NY 10017", 499.00, "557543454");

-- insert data into user_order table
INSERT INTO user_orders ( account_id, subtotal, purchase_date, date_shipped, tracking_no, order_status, shipper)
VALUES (5, 50.00, "2021-04-12", "2021-04-12", 1234567, 1, "Movers");

-- insert data into purchased_items table
INSERT INTO purchased_items (transaction_id, item_name, amount, item_price, vote_score)
VALUES ( 17, "MacBook Air", 1, 999.00, 1);

-- get product rating from purchased_items table
SELECT  COUNT(vote_score)  FROM purchased_items 
WHERE  item_name= "MacBook Air" AND vote_score = 5;

SELECT  COUNT(vote_score)  FROM purchased_items 
WHERE item_name= "MacBook Air"  AND  vote_score = 4;

SELECT  COUNT(vote_score)  FROM purchased_items 
WHERE  item_name= "MacBook Air" AND vote_score = 3;

SELECT  COUNT(vote_score)  FROM purchased_items 
WHERE item_name= "MacBook Air" AND vote_score = 2;

SELECT  COUNT(vote_score)  FROM purchased_items 
WHERE  item_name= "MacBook Air" AND vote_score =1 ;

SELECT AVG(vote_score) FROM purchased_items WHERE item_name= "MacBook Air";

-- insert data into supplier_acc table
INSERT INTO supplier_acc (account_id, company_name) VALUES (2, "NJsuppliers");

INSERT INTO product ( product_name, price, purpose, architecture, dimensions, weight, quantity_sold, supplied_by)
VALUES ( "MacBook Pro 14", 1999.00, 2, 2, "0.63 inch, 14inches'",  5.8 , 25, 2);

INSERT INTO system ( product_id, cpu, ram_size, gpu, hdd_size, operating_system)
VALUES ( 3, "Intel Core i7", "16 GB", "Intel UHD 630", "1T GB", "macOS Big Sur");

SELECT product_name, purpose, price, cpu, gpu, ram_size, hdd_size, operating_system
FROM product
INNER JOIN system ON product.product_id = system.product_id;

SELECT product.product_id as id, product_name, purpose, price, cpu, gpu, ram_size, hdd_size, operating_system
FROM product
INNER JOIN system ON product.product_id = system.product_id;

-- select 3 systems
SELECT product.product_id as id, product_name, purpose, price, cpu, gpu, ram_size, hdd_size, operating_system
FROM product
INNER JOIN system ON product.product_id = system.product_id
LIMIT 3;

-- select 3 best seller computers based on quantity sold
SELECT  product_name, price, dimensions, weight, quantity_sold 
FROM product
ORDER By quantity_sold DESC
LIMIT 3;

-- top 3 best selling computers with all the parts
SELECT product.product_id as id, product_name, purpose, price, cpu, gpu, ram_size, hdd_size, operating_system, quantity_sold
FROM product
INNER JOIN system ON product.product_id = system.product_id
ORDER BY product.quantity_sold DESC
LIMIT 3;

-- select one product from both product and system for a given product_id
SELECT product.product_id as id, product_name, purpose, architecture, price, cpu, gpu, ram_size, hdd_size, operating_system, dimensions, weight
FROM product
INNER JOIN system ON product.product_id = system.product_id
WHERE id = 3;

-- select mac systems
SELECT product.product_id as id, product_name, purpose, price, cpu, gpu, ram_size, hdd_size, operating_system
FROM product
INNER JOIN system ON product.product_id = system.product_id
WHERE  UPPER( product_name) LIKE '%MAC%' and UPPER( operating_system) LIKE '%MAC%';

-- sql query for windows systems
INSERT INTO product ( product_name, price, purpose, architecture, dimensions, weight, quantity_sold, supplied_by)
VALUES ( "Lenovo15.6", 529.00, 2, 1, "14.3,10 , 1.02",  3.49 , 2, 1);

INSERT INTO system ( product_id, cpu, ram_size, gpu, hdd_size, operating_system)
VALUES ( 11, "Intel Core i5", "8 GB", "Intel Iris XE", "256 GB", "Windows 10 Home");

SELECT * FROM product;

SELECT * FROM system;

DELETE FROM product WHERE product_id = 8;
DELETE FROM system WHERE product_id = 8;

SELECT product.product_id as id, product_name, price, cpu, gpu, ram_size, hdd_size, operating_system
FROM product
INNER JOIN system ON product.product_id = system.product_id
WHERE  UPPER(operating_system) LIKE '%WINDOWS%';

-- sql query for linux system
INSERT INTO product ( product_name, price, purpose, architecture, dimensions, weight, quantity_sold, supplied_by)
VALUES ( "Acer 14Inch", 5009.00, 1, 1, "12.93 x 9.27 x 1.7",  2.96 , 2, 1);

INSERT INTO system ( product_id, cpu, ram_size, gpu, hdd_size, operating_system)
VALUES ( 14, "AMD Ryzen", "8 GB", "NVIDIA Quadro", "512 GB", "Linux Mint");

SELECT * FROM product;

SELECT * FROM system;

DELETE FROM product WHERE product_id = 8;
DELETE FROM system WHERE product_id = 8;

SELECT product.product_id as id, product_name, price, cpu, gpu, ram_size, hdd_size, operating_system
FROM product
INNER JOIN system ON product.product_id = system.product_id
WHERE  UPPER(operating_system) LIKE '%LINUX%';

-- cpu data
INSERT INTO product ( product_name, price, purpose, architecture, dimensions, weight, quantity_sold, supplied_by)
VALUES ( "Intel Core i5 906KA", 229.00, 1, 1, "0 x 0 x 0 in",  0.0 , 2, 1);

INSERT INTO cpu( product_id, cpu_socket, speed, processor_count) 
VALUES ( 17, "LGA 1151", "3.7 GHz", 6 );

SELECT * FROM product;

SELECT * FROM cpu;

SELECT product.product_id as id, product_name, cpu_socket, speed, processor_count, price
FROM product
INNER JOIN cpu ON product.product_id = cpu.product_id;

SELECT product.product_id as id, product_name, cpu_socket, speed, processor_count, price
FROM product
INNER JOIN cpu ON product.product_id = cpu.product_id
WHERE id=16;

-- memory data
VALUES ( "Patriot Viper Steel", 91.00, 0, 0, "0 x 0 x 0 in",  0.0 , 2, 1);

INSERT INTO ram( product_id, capacity, memory_speed, ram_type) 
VALUES ( 24, "16 GB", "DDR4 3200", "DDR4");

SELECT * FROM product;

SELECT * FROM ram;

SELECT product.product_id as id, product_name, capacity, memory_speed, ram_type, price
FROM product
INNER JOIN ram ON product.product_id = ram.product_id;

SELECT product.product_id as id, product_name, capacity, memory_speed, ram_type, price
FROM product
INNER JOIN ram ON product.product_id = ram.product_id
WHERE id = 22;

-- gpu data
INSERT INTO product ( product_name, price, purpose, architecture, dimensions, weight, quantity_sold, supplied_by)
VALUES ( "GeForce RTX 3090", 999.00, 0, 0, "0 x 0 x 0 in",  0.0 , 2, 1);

INSERT INTO gpu( product_id, memory_size, memory_speed) 
VALUES ( 27, "24 GB", "1785 MHz");

SELECT * FROM product;

SELECT * FROM gpu;

SELECT product.product_id as id, product_name, memory_size, memory_speed, price
FROM product
INNER JOIN gpu ON product.product_id = gpu.product_id;

SELECT product.product_id as id, product_name, memory_size, memory_speed, price
FROM product
INNER JOIN gpu ON product.product_id = gpu.product_id
WHERE id = 25;

-- pc case data
INSERT INTO pc_case( product_id, motherboard_support, io_ports, fan_support, hdd_support, psu_support) 
VALUES ( 30, "ATX, E-ATX", "3xUSB 3.0/Audio","2x120mm Fan","2x3.5 inch", "ATX");

SELECT * FROM product;

SELECT * FROM pc_case;

SELECT product.product_id as id, product_name, motherboard_support, io_ports, fan_support, hdd_support, psu_support,  price
FROM product
INNER JOIN pc_case ON product.product_id = pc_case.product_id;

SELECT product.product_id as id, product_name,  dimensions, weight, motherboard_support, io_ports, fan_support, hdd_support, psu_support,  price
FROM product
INNER JOIN pc_case ON product.product_id = pc_case.product_id
WHERE id = 28;

-- psu data
INSERT INTO psu( product_id, power, psu_type) 
VALUES ( 33, "850W", "ATX12V / EPS12V");

SELECT * FROM product;

SELECT * FROM psu;

SELECT product.product_id as id, product_name, power, psu_type,  price
FROM product
INNER JOIN psu ON product.product_id = psu.product_id;

SELECT product.product_id as id, product_name,dimensions, weight, power, psu_type,  price
FROM product
INNER JOIN psu ON product.product_id = psu.product_id
WHERE id = 33;