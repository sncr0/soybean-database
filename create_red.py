import mysql.connector
import csv
from infra import *
import time

connection, cursor = connect_to_database()

cursor.execute("""
CREATE TABLE IF NOT EXISTS CLIENTS (
    brn INT PRIMARY KEY
);
""")

cursor.execute("""
               CREATE TABLE IF NOT EXISTS CONTRACTS (
                   contract_id INT PRIMARY KEY,
                   client_brn INT, --                                    business registration number
                   FOREIGN KEY (client_brn) REFERENCES CLIENTS(brn)
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PROCESSES (
                   process_id INT PRIMARY KEY  
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS FDA_APPROVAL (
                   fda_id INT PRIMARY KEY,
                   process_id INT,
                   FOREIGN KEY (process_id) REFERENCES PROCESSES(process_id)  
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SITES (
                   site_id INT PRIMARY KEY 
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS DEVELOPED_ON_SITE (
                   site_id INT,
                   process_id INT,
                   FOREIGN KEY (site_id) REFERENCES SITES(site_id),
                   FOREIGN KEY (process_id) REFERENCES PROCESSES(process_id)  
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS EMPLOYEES (
                   employee_id INT PRIMARY KEY
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS WORKS_ON_SITE (
                   employee_id INT,
                   site_id INT,
                   FOREIGN KEY (site_id) REFERENCES SITES(site_id),
                   FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id)  
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SUPPLIERS (
                   supplier_id INT PRIMARY KEY 
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS SUPPLIED_COMPOUNDS (
                   lot_id INT PRIMARY KEY,
                   supplier_id INT,
                   site_id INT,
                   compound_name VARCHAR(100),
                   FOREIGN KEY (supplier_id) REFERENCES SUPPLIERS(supplier_id),
                   FOREIGN KEY (site_id) REFERENCES SITES(site_id) 
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS BATCHES (
                   batch_id INT PRIMARY KEY,
                   process_id INT,
                   site_id INT,
                   FOREIGN KEY (process_id) REFERENCES PROCESSES(process_id),
                   FOREIGN KEY (site_id) REFERENCES SITES(site_id) 
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS IPC (
                   IPC_id INT PRIMARY KEY,
                   batch_id INT,
                   site_id INT,
                   FOREIGN KEY (batch_id) REFERENCES BATCHES(batch_id),
                   FOREIGN KEY (site_id) REFERENCES SITES(site_id) 
               )
               """)

connection.commit()
disconnect_from_database(connection, cursor)


