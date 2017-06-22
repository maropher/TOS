import sqlite3

conn = sqlite3.connect('database.db')
print "Opened database successfully";

conn.execute('CREATE TABLE cart (cartId INTEGER PRIMARY KEY AUTOINCREMENT, watchId int(12) NOT NULL, userId int(12) NOT NULL)')
conn.execute('CREATE TABLE watch (watchId INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(128) NOT NULL, description varchar(512) NOT NULL, imageUrl varchar(512) NOT NULL, star int(1) NOT NULL, price decimal(12,0) NOT NULL)')
conn.execute('CREATE TABLE users (userId INTEGER PRIMARY KEY AUTOINCREMENT, email varchar(128) NOT NULL, nama varchar(128) NOT NULL, nomor varchar(128) NOT NULL, password varchar(512) NOT NULL)')
print "Tables created successfully";
conn.close()
