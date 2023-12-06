import mysql.connector
import csv
from infra import *
import time

connection, cursor = connect_to_database()

cursor.execute("""
               CREATE DATABASE IF NOT EXISTS SOYBEAN;
               """)

cursor.execute("""
               USE SOYBEAN;
               """)



#==========================|  PLANTATION  |=================================
cursor.execute("""
               CREATE TABLE IF NOT EXISTS PLANTATION (
                   site_id INT PRIMARY KEY 
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PLANTATION_WORKER (
                   employee_id INT PRIMARY KEY,
                   site_id INT,
                   FOREIGN KEY (site_id) REFERENCES SITE(site_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PW_CONTRACT (
                   contract_id INT PRIMARY KEY,
                   employee_id INT,
                   site_id INT,
                   FOREIGN KEY (employee_id) REFERENCES PLANTATION_WORKER (employee_id),
                   FOREIGN KEY (site_id) REFERENCES PLANTATION_WORKER(site_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PW_TEMPORARY_CONTRACT (
                   temp_contract_id INT PRIMARY KEY,
                   site_id INT,
                   employee_id INT,
                   contract_id INT,
                   start_date DATE,
                   end_date DATE,
                   FOREIGN KEY (contract_id) REFERENCES PW_CONTRACT (contract_id),
                   FOREIGN KEY (site_id) REFERENCES PW_CONTRACT (site_id),
                   FOREIGN KEY (employee_id) REFERENCES PW_CONTRACT (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PW_PERMANENT_CONTRACT (
                   perm_contract_id INT PRIMARY KEY,
                   site_id INT,
                   employee_id INT,
                   contract_id INT,
                   start_date DATE,
                   FOREIGN KEY (contract_id) REFERENCES PW_CONTRACT (contract_id),
                   FOREIGN KEY (site_id) REFERENCES PW_CONTRACT (site_id),
                   FOREIGN KEY (employee_id) REFERENCES PW_CONTRACT (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SITE_MANAGER (
                   site_manager_id INT PRIMARY KEY, -- maybe we could eliminate site_manager_id and only use the foreign keys?
                   site_id INT,
                   employee_id INT,
                   FOREIGN KEY (site_id) REFERENCES SITE (site_id),
                   FOREIGN KEY (employee_id) REFERENCES PLANTATION_WORKER (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PW_WORKS_AT_SITE (
                   employee_id INT,
                   site_id INT,
                   FOREIGN KEY (site_id) REFERENCES SITE(site_id),
                   FOREIGN KEY (employee_id) REFERENCES PLANTATION_WORKER (employee_id)
               )
               """)

#==========================|  SITE  |=================================
cursor.execute("""
               CREATE TABLE IF NOT EXISTS SITE (
                   site_id INT PRIMARY KEY 
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SITE_WORKER (
                   employee_id INT PRIMARY KEY,
                   site_id INT,
                   FOREIGN KEY (site_id) REFERENCES SITE(site_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SW_CONTRACT (
                   contract_id INT PRIMARY KEY,
                   employee_id INT,
                   site_id INT,
                   FOREIGN KEY (employee_id) REFERENCES SITE_WORKER (employee_id),
                   FOREIGN KEY (site_id) REFERENCES SITE_WORKER (site_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SW_TEMPORARY_CONTRACT (
                   temp_contract_id INT PRIMARY KEY,
                   site_id INT,
                   employee_id INT,
                   contract_id INT,
                   start_date DATE,
                   end_date DATE,
                   FOREIGN KEY (contract_id) REFERENCES SW_CONTRACT (contract_id),
                   FOREIGN KEY (site_id) REFERENCES SW_CONTRACT (site_id),
                   FOREIGN KEY (employee_id) REFERENCES SW_CONTRACT (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SW_PERMANENT_CONTRACT (
                   perm_contract_id INT PRIMARY KEY,
                   site_id INT,
                   employee_id INT,
                   contract_id INT,
                   start_date DATE,
                   FOREIGN KEY (contract_id) REFERENCES SW_CONTRACT (contract_id),
                   FOREIGN KEY (site_id) REFERENCES SW_CONTRACT (site_id),
                   FOREIGN KEY (employee_id) REFERENCES SW_CONTRACT (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SITE_MANAGER (
                   site_manager_id INT PRIMARY KEY, -- maybe we could eliminate site_manager_id and only use the foreign keys?
                   site_id INT,
                   employee_id INT,
                   FOREIGN KEY (site_id) REFERENCES SITE(site_id),
                   FOREIGN KEY (employee_id) REFERENCES SITE_WORKER (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SUPPLIER (
                   supplier_id INT PRIMARY KEY
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SW_WORKS_AT_SITE (
                   employee_id INT,
                   site_id INT,
                   FOREIGN KEY (site_id) REFERENCES SITE(site_id),
                   FOREIGN KEY (employee_id) REFERENCES SITE_WORKER(employee_id)
               )
               """)

# cursor.execute("""
#                CREATE TABLE IF NOT EXISTS SUPPLIES (
#                    plantation_id INT,
#                    site_id INT,
#                    inventory_id INT,
#                    FOREIGN KEY (supplier_id) REFERENCES SUPPLIER (supplier_id),
#                    FOREIGN KEY (site_id) REFERENCES SITE(site_id),
#                      FOREIGN KEY (inventory_id) REFERENCES INVENTORY (inventory_id)
#                )
#                """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS INVENTORY (
                   inventory_id INT PRIMARY KEY, -- we maybe want this to be a standalone key, but still reference supplier and site (not sure if there is proper syntax for this)
                    plantation_id INT,
                   site_id INT,
                   FOREIGN KEY (supplier_id) REFERENCES SUPPLIER (plantation_id),
                   FOREIGN KEY (site_id) REFERENCES SITE (site_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS BATCH (
                   batch_id INT PRIMARY KEY,
                   inventory_id INT,
                   supplier_id INT,
                   site_id INT,
                   FOREIGN KEY (supplier_id) REFERENCES INVENTORY (supplier_id),
                   FOREIGN KEY (site_id) REFERENCES INVENTORY (site_id),
                   FOREIGN KEY (inventory_id) REFERENCES INVENTORY (inventory_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS IPC (
                   ipc_id INT PRIMARY KEY,
                   batch_id INT,
                   inventory_id INT,
                   supplier_id INT,
                   site_id INT,
                   FOREIGN KEY (supplier_id) REFERENCES BATCH (supplier_id),
                   FOREIGN KEY (site_id) REFERENCES BATCH (site_id),
                   FOREIGN KEY (inventory_id) REFERENCES BATCH (inventory_id),
                   FOREIGN KEY (batch_id) REFERENCES BATCH (batch_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS STOCK (
                   stock_id INT PRIMARY KEY,
                   batch_id INT,
                   inventory_id INT,
                   supplier_id INT,
                   site_id INT,
                   FOREIGN KEY (supplier_id) REFERENCES BATCH (supplier_id),
                   FOREIGN KEY (site_id) REFERENCES BATCH (site_id),
                   FOREIGN KEY (inventory_id) REFERENCES BATCH (inventory_id),
                   FOREIGN KEY (batch_id) REFERENCES BATCH (batch_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS CLIENT (
                   client_id INT PRIMARY KEY
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SALES_DEPARTMENT (
                   department_id INT PRIMARY KEY,
                   department_name VARCHAR(255) -- Add additional fields as needed
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SALES_MANAGER (
                   sales_manager_id INT PRIMARY KEY,
                   department_id INT,
                   FOREIGN KEY (department_id) REFERENCES SALES_DEPARTMENT (department_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SALES_ASSOCIATE (
                   sales_associate_id INT PRIMARY KEY,
                   department_id INT,
                   FOREIGN KEY (department_id) REFERENCES SALES_DEPARTMENT (department_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SALE (
                   sale_id INT PRIMARY KEY,
                   sales_associate_id INT,
                   client_id INT,
                   stock_id INT,
                   batch_id INT,
                   inventory_id INT,
                   supplier_id INT,
                   site_id INT,
                   FOREIGN KEY (sales_associate_id) REFERENCES SALES_ASSOCIATE (sales_associate_id),
                   FOREIGN KEY (client_id) REFERENCES CLIENT(client_id),
                   FOREIGN KEY (stock_id) REFERENCES STOCK(stock_id),
                   FOREIGN KEY (supplier_id) REFERENCES STOCK (supplier_id),
                   FOREIGN KEY (site_id) REFERENCES STOCK (site_id),
                   FOREIGN KEY (inventory_id) REFERENCES STOCK (inventory_id),
                   FOREIGN KEY (batch_id) REFERENCES STOCK (batch_id)
               )
               """)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS INVOICE ( -- do we need this?
                   invoice_id INT PRIMARY KEY,
                   sale_id INT,
                   FOREIGN KEY (sale_id) REFERENCES SALE(sale_id)
               )
               """)

connection.commit()
disconnect_from_database(connection, cursor)
