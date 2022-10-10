create table products (
    productid INTEGER PRIMARY KEY AUTOINCREMENT,
    productname TEXT,
    price FLOAT,
    imagefile TEXT);

    
create table customers (
    customerid INTEGER PRIMARY KEY AUTOINCREMENT,
    customername TEXT);


create table customersproducts (
    cpid INTEGER PRIMARY KEY AUTOINCREMENT,
    productid INTEGER NOT NULL,
    customerid INTEGER NOT NULL,
    FOREIGN key (customerid) REFERENCES customers (customerid),
    FOREIGN key (productid) REFERENCES products (productid)
);

    

    