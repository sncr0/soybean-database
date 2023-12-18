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

# cursor.execute("""
#                CREATE TYPE EmploymentType AS ENUM ('temporary', 'permanent');
#                """)



#==========================|  PLANTATION  |=================================
cursor.execute("""
               CREATE TABLE IF NOT EXISTS PLANTATION (
                   -- primary key:
                   plantation_name VARCHAR(255) PRIMARY KEY,
                   
                   -- extra:
                   plantation_address VARCHAR(511)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PLANTATION_WORKER (
                   -- primary key:
                   employee_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key:
                    plantation_name VARCHAR(255),

                   -- extra: 
                   employee_first_name VARCHAR(255),
                   employee_middle_name VARCHAR(255),
                   employee_last_name VARCHAR(255),
                   
                   FOREIGN KEY (plantation_name) REFERENCES PLANTATION (plantation_name)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PW_CONTRACT (
                   -- primary key:
                   contract_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key:
                   employee_id VARCHAR(36),
                   plantation_name VARCHAR(255),
                   
                   -- extra:
                   contract_type ENUM('temporary', 'permanent'),
                   
                   FOREIGN KEY (employee_id) REFERENCES PLANTATION_WORKER (employee_id),
                   FOREIGN KEY (plantation_name) REFERENCES PLANTATION_WORKER (plantation_name)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PW_TEMPORARY_CONTRACT (
                   -- primary key:
                   temp_contract_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key:
                   plantation_name VARCHAR(255),
                   employee_id VARCHAR(36),
                   contract_id VARCHAR(36),
                   
                   -- extra:
                   salary INT,
                   start_date DATE,
                   end_date DATE,
                   
                   FOREIGN KEY (contract_id) REFERENCES PW_CONTRACT (contract_id),
                   FOREIGN KEY (plantation_name) REFERENCES PW_CONTRACT (plantation_name),
                   FOREIGN KEY (employee_id) REFERENCES PW_CONTRACT (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PW_PERMANENT_CONTRACT (
                   -- primary key:
                   perm_contract_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key:
                   plantation_name VARCHAR(255),
                   employee_id VARCHAR(36),
                   contract_id VARCHAR(36),
                   
                   -- extra:
                   salary INT,
                   start_date DATE,
                   
                   FOREIGN KEY (contract_id) REFERENCES PW_CONTRACT (contract_id),
                   FOREIGN KEY (plantation_name) REFERENCES PW_CONTRACT (plantation_name),
                   FOREIGN KEY (employee_id) REFERENCES PW_CONTRACT (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PLANTATION_MANAGER (
                   -- primary key:
                   plantation_manager_id VARCHAR(36) PRIMARY KEY, -- maybe we could eliminate site_manager_id and only use the foreign keys?
                   
                   -- foreign key:
                   plantation_name VARCHAR(255),
                   employee_id VARCHAR(36),
                   
                   FOREIGN KEY (plantation_name) REFERENCES PLANTATION (plantation_name),
                   FOREIGN KEY (employee_id) REFERENCES PLANTATION_WORKER (employee_id)
               )
               """)

#==========================|  SITE  |=================================
cursor.execute("""
               CREATE TABLE IF NOT EXISTS SITE (
                   -- primary key: 
                   site_name VARCHAR(255) PRIMARY KEY
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SITE_WORKER (
                   -- primary key:
                   employee_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key: 
                   site_name VARCHAR(255),
                   
                   FOREIGN KEY (site_name) REFERENCES SITE(site_name)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SW_CONTRACT (
                   -- primary key:
                   contract_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key:
                   employee_id VARCHAR(36),
                   site_name VARCHAR(255),
                   
                   -- extra:
                   contract_type ENUM('temporary', 'permanent'),
                   
                   FOREIGN KEY (employee_id) REFERENCES SITE_WORKER (employee_id),
                   FOREIGN KEY (site_name) REFERENCES SITE_WORKER (site_name)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SW_TEMPORARY_CONTRACT (
                   -- primary key:
                   temp_contract_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key:
                   site_name VARCHAR(255),
                   employee_id VARCHAR(36),
                   contract_id VARCHAR(36),
                   
                   -- extra:
                   salary INT,
                   start_date DATE,
                   end_date DATE,
                   
                   FOREIGN KEY (contract_id) REFERENCES SW_CONTRACT (contract_id),
                   FOREIGN KEY (site_name) REFERENCES SW_CONTRACT (site_name),
                   FOREIGN KEY (employee_id) REFERENCES SW_CONTRACT (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SW_PERMANENT_CONTRACT (
                   -- primary key:
                   perm_contract_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key:
                   site_name VARCHAR(255),
                   employee_id VARCHAR(36),
                   contract_id VARCHAR(36),
                   
                   -- extra:
                   salary INT,
                   start_date DATE,
                   
                   FOREIGN KEY (contract_id) REFERENCES SW_CONTRACT (contract_id),
                   FOREIGN KEY (site_name) REFERENCES SW_CONTRACT (site_name),
                   FOREIGN KEY (employee_id) REFERENCES SW_CONTRACT (employee_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SITE_MANAGER (
                   -- primary key:
                   site_manager_id VARCHAR(36) PRIMARY KEY, -- maybe we could eliminate site_manager_id and only use the foreign keys?
                   
                   -- foreign key:
                   site_name VARCHAR(255),
                   employee_id VARCHAR(36),
                   
                   FOREIGN KEY (site_name) REFERENCES SITE(site_name),
                   FOREIGN KEY (employee_id) REFERENCES SITE_WORKER (employee_id)
               )
               """)

# ================================|  PRODUCTION  |=================================
cursor.execute("""
               CREATE TABLE IF NOT EXISTS INVENTORY (
                   -- primary key:
                   -- inventory_id VARCHAR(36) PRIMARY KEY, -- we maybe want this to be a standalone key, but still reference supplier and site (not sure if there is proper syntax for this)
                   harvest_date DATE PRIMARY KEY, 
                   
                   -- foreign key:
                   plantation_name VARCHAR(255),
                   site_name VARCHAR(255),
                   
                   FOREIGN KEY (plantation_name) REFERENCES PLANTATION (plantation_name),
                   FOREIGN KEY (site_name) REFERENCES SITE (site_name)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS BATCH (
                   -- primary key:
                   production_unit INT,
                   production_date DATE,
                   PRIMARY KEY (production_unit, production_date),
                   
                   -- foreign key:
                   harvest_date DATE,
                   plantation_name VARCHAR(255),
                   site_name VARCHAR(255),
                   
                   FOREIGN KEY (plantation_name) REFERENCES INVENTORY (plantation_name),
                   FOREIGN KEY (site_name) REFERENCES INVENTORY (site_name),
                   FOREIGN KEY (harvest_date) REFERENCES INVENTORY (harvest_date)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS IPC (
                   -- primary key:
                   ipc_id VARCHAR(36) PRIMARY KEY,
                   
                   -- foreign key:
                   production_unit INT,
                   production_date DATE,
                   harvest_date DATE,
                   plantation_name VARCHAR(255),
                   site_name VARCHAR(255),
                   
                   FOREIGN KEY (plantation_name) REFERENCES BATCH (plantation_name),
                   FOREIGN KEY (site_name) REFERENCES BATCH (site_name),
                   FOREIGN KEY (harvest_date) REFERENCES BATCH (harvest_date),
                   FOREIGN KEY (production_unit, production_date) REFERENCES BATCH (production_unit, production_date)
                   -- FOREIGN KEY (production_date) REFERENCES BATCH (production_date)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS STOCK (
                   -- primary key:
                   package_date DATE PRIMARY KEY,
                   
                   -- secondary key:
                   production_unit INT,
                   production_date DATE,
                   harvest_date DATE,
                   plantation_name VARCHAR(255),
                   site_name VARCHAR(255),
                   
                   FOREIGN KEY (plantation_name) REFERENCES BATCH (plantation_name),
                   FOREIGN KEY (site_name) REFERENCES BATCH (site_name),
                   FOREIGN KEY (harvest_date) REFERENCES BATCH (harvest_date),
                   FOREIGN KEY (production_unit, production_date) REFERENCES BATCH (production_unit, production_date)
                   -- FOREIGN KEY (production_date) REFERENCES BATCH (production_date)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS CLIENT (
                   client_id INT PRIMARY KEY
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SALES_DEPARTMENT (
                   sales_department_id INT PRIMARY KEY,
                   sales_department_name VARCHAR(255) -- Add additional fields as needed
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SALES_MANAGER (
                   sales_manager_id INT PRIMARY KEY,
                   sales_department_id INT,
                   FOREIGN KEY (sales_department_id) REFERENCES SALES_DEPARTMENT (sales_department_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SALES_ASSOCIATE (
                   sales_associate_id INT PRIMARY KEY,
                   sales_department_id INT,
                   FOREIGN KEY (sales_department_id) REFERENCES SALES_DEPARTMENT (sales_department_id)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SALE (
                   sale_id INT PRIMARY KEY,
                   sales_associate_id INT,
                   client_id INT,
                   package_date DATE,
                   production_unit INT,
                   production_date DATE,
                   harvest_date DATE,
                   plantation_name VARCHAR(255),
                   site_name VARCHAR(255),
                   FOREIGN KEY (sales_associate_id) REFERENCES SALES_ASSOCIATE (sales_associate_id),
                   FOREIGN KEY (client_id) REFERENCES CLIENT(client_id),
                   FOREIGN KEY (package_date) REFERENCES STOCK(package_date),
                   FOREIGN KEY (plantation_name) REFERENCES STOCK (plantation_name),
                   FOREIGN KEY (site_name) REFERENCES STOCK (site_name),
                   FOREIGN KEY (harvest_date) REFERENCES STOCK (harvest_date),
                   FOREIGN KEY (production_unit, production_date) REFERENCES STOCK (production_unit, production_date)
                   -- FOREIGN KEY (production_date) REFERENCES STOCK (production_date)
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
