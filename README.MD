Project: api for management of a pizzeria
Language: Python
Database: MySql

The customer registration has the fields: name, email, telephone and password

Tables in the Bank: inventory, product, product_investor, order, OrderPrice, customer, customerID

Validation occurs by Token:

SECRET_KEY = "OBaratoeLouco"
SQLALCHEMY_DATABASE_URI = 'mysql + pymysql: // root: 123456 @ localhost / pizza'