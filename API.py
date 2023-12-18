import mysql.connector
from faker import Faker
import random
import uuid
import random
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import model_from_json

fake = Faker()



class SITE:
    def __init__(self, site_name):
        self.site_name = site_name

    def insert(self, cursor):
        cursor.execute("INSERT INTO SITE (site_name) VALUES (%s)", (self.site_name,))
    
class SITE_WORKER:
    def __init__(self, SITE: SITE):
        self.employee_id = str(uuid.uuid4())
        self.site_name = SITE.site_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO SITE_WORKER (employee_id, site_name) VALUES (%s, %s)", (self.employee_id, self.site_name))
    
class SW_CONTRACT:
    def __init__(self, SITE_WORKER: SITE_WORKER):
        self.contract_id = str(uuid.uuid4())
        self.site_name = SITE_WORKER.site_name
        self.employee_id = SITE_WORKER.employee_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO SW_CONTRACT (contract_id, site_name, employee_id) VALUES (%s, %s, %s)", (self.contract_id, self.site_name, self.employee_id))

class SW_TEMPORARY_CONTRACT:
    def __init__(self, SW_CONTRACT: SW_CONTRACT):
        self.temp_contract_id = str(uuid.uuid4())
        self.contract_id = SW_CONTRACT.contract_id
        self.site_name = SW_CONTRACT.site_name
        self.employee_id = SW_CONTRACT.employee_id
        self.start_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
        self.end_date = fake.date_between(start_date='today', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
    def insert(self, cursor):
        cursor.execute("INSERT INTO SW_TEMPORARY_CONTRACT (temp_contract_id, contract_id, site_name, employee_id, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (self.temp_contract_id, 
                        self.contract_id, 
                        self.site_name, 
                        self.employee_id, 
                        self.start_date, 
                        self.end_date))
        
class SW_PERMANENT_CONTRACT:
    def __init__(self, SW_CONTRACT: SW_CONTRACT):
        self.perm_contract_id = str(uuid.uuid4())
        self.contract_id = SW_CONTRACT.contract_id
        self.site_name = SW_CONTRACT.site_name
        self.employee_id = SW_CONTRACT.employee_id
        self.start_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
    def insert(self, cursor):
        cursor.execute("""INSERT INTO SW_PERMANENT_CONTRACT 
                    (perm_contract_id, contract_id, site_name, employee_id, start_date) 
                    VALUES (%s, %s, %s, %s, %s)""", 
                    (self.perm_contract_id, self.contract_id, self.site_name, self.employee_id, self.start_date))
        
class SITE_MANAGER:
    def __init__(self, SITE_WORKER: SITE_WORKER, SITE: SITE):
        self.site_manager_id = str(uuid.uuid4())
        self.employee_id = SITE_WORKER.employee_id
        self.site_name = SITE.site_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO SITE_MANAGER (site_manager_id, employee_id, site_name) VALUES (%s, %s, %s)", (self.site_manager_id, self.employee_id, self.site_name))

# =============================================|  PLANTATION  |===================================================        
class PLANTATION:
    def __init__(self, plantation_name):
        self.plantation_name = plantation_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO PLANTATION (plantation_name) VALUES (%s)", (self.plantation_name,))
        
class FIELD:
    def __init__(self, PLANTATION: PLANTATION, field_number, plant_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S'), grow_time = random.randint(0, 100), planted = False):
        self.field_number = field_number
        self.plant_date = plant_date
        self.grow_time = grow_time
        self.plantation_name = PLANTATION.plantation_name
        self.planted = planted
        
    @classmethod    
    def from_query(cls, *args):
        instance = cls.__new__(cls)
        instance.field_number = args[0]
        instance.plantation_name = args[1]
        instance.plant_date = args[2]
        instance.grow_time = args[3]
        instance.planted = args[4]
        return instance
        
    def insert(self, cursor):
        cursor.execute("INSERT INTO FIELD (field_number, plantation_name, plant_date, grow_time, planted) VALUES (%s, %s, %s, %s, %s)", (self.field_number, self.plantation_name, self.plant_date, self.grow_time, self.planted))
        
class PLANTATION_WORKER:
    def __init__(self, PLANTATION: PLANTATION):
        self.employee_id = str(uuid.uuid4())
        self.plantation_name = PLANTATION.plantation_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO PLANTATION_WORKER (employee_id, plantation_name) VALUES (%s, %s)", (self.employee_id, self.plantation_name))

# class WORKS_AT_PLANTATION:
#     def __init__(self, PLANTATION_WORKER: PLANTATION_WORKER, PLANTATION: PLANTATION):
#         self.employee_id = PLANTATION_WORKER.employee_id
#         self.plantation_id = PLANTATION.plantation_name
#     def insert(self, cursor):
#         cursor.execute("INSERT INTO WORKS_AT_PLANTATION (employee_id, plantation_name) VALUES (%s, %s)", (self.employee_id, self.plantation_name))

class PW_CONTRACT:
    def __init__(self, PLANTATION_WORKER: PLANTATION_WORKER):
        self.contract_id = str(uuid.uuid4())
        self.plantation_name = PLANTATION_WORKER.plantation_name
        self.employee_id = PLANTATION_WORKER.employee_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO PW_CONTRACT (contract_id, plantation_name, employee_id) VALUES (%s, %s, %s)", (self.contract_id, self.plantation_name, self.employee_id))

class PW_TEMPORARY_CONTRACT:
    def __init__(self, PW_CONTRACT: PW_CONTRACT):
        self.temp_contract_id = str(uuid.uuid4())
        self.contract_id = PW_CONTRACT.contract_id
        self.plantation_name = PW_CONTRACT.plantation_name
        self.employee_id = PW_CONTRACT.employee_id
        self.start_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
        self.end_date = fake.date_between(start_date='today', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
    def insert(self, cursor):
        cursor.execute("INSERT INTO PW_TEMPORARY_CONTRACT (temp_contract_id, contract_id, plantation_name, employee_id, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)", (self.temp_contract_id, self.contract_id, self.plantation_name, self.employee_id, self.start_date, self.end_date))
        
class PW_PERMANENT_CONTRACT:
    def __init__(self, PW_CONTRACT: PW_CONTRACT):
        self.perm_contract_id = str(uuid.uuid4())
        self.contract_id = PW_CONTRACT.contract_id
        self.plantation_name = PW_CONTRACT.plantation_name
        self.employee_id = PW_CONTRACT.employee_id
        self.start_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
    def insert(self, cursor):
        cursor.execute("INSERT INTO PW_PERMANENT_CONTRACT (perm_contract_id, contract_id, plantation_name, employee_id, start_date) VALUES (%s, %s, %s, %s, %s)", (self.perm_contract_id, self.contract_id, self.plantation_name, self.employee_id, self.start_date))
        
class PLANTATION_MANAGER:
    def __init__(self, PLANTATION_WORKER: PLANTATION_WORKER, PLANTATION: PLANTATION):
        self.plantation_manager_id = str(uuid.uuid4())
        self.employee_id = PLANTATION_WORKER.employee_id
        self.plantation_name = PLANTATION.plantation_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO PLANTATION_MANAGER (plantation_manager_id, employee_id, plantation_name) VALUES (%s, %s, %s)", (self.plantation_manager_id, self.employee_id, self.plantation_name))

# ==============================================|  PRODUCTION ROUTE  |=====================================================
class INVENTORY:
    def __init__(self, SITE: SITE, PLANTATION: PLANTATION, harvest_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')):
        self.harvest_date = harvest_date
        self.site_name = SITE.site_name
        self.plantation_name = PLANTATION.plantation_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO INVENTORY (harvest_date, site_name, plantation_name) VALUES (%s, %s, %s)", (self.harvest_date, self.site_name, self.plantation_name))
        
class BATCH:
    def __init__(self, INVENTORY: INVENTORY, production_unit = 0, production_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')):
        self.production_unit = production_unit
        self.production_date = production_date
        self.harvest_date = INVENTORY.harvest_date
        self.plantation_name = INVENTORY.plantation_name
        self.site_name = INVENTORY.site_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO BATCH (production_unit, production_date, harvest_date, plantation_name, site_name) VALUES (%s, %s, %s, %s, %s)", (self.production_unit, self.production_date, self.harvest_date, self.plantation_name, self.site_name))

class IPC:
    def __init__(self, BATCH: BATCH):
        self.ipc_id = str(uuid.uuid4())
        self.production_unit = BATCH.production_unit
        self.production_date = BATCH.production_date
        self.harvest_date = BATCH.harvest_date
        self.plantation_name = BATCH.plantation_name
        self.site_name = BATCH.site_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO IPC (ipc_id, production_unit, production_date, harvest_date, plantation_name, site_name) VALUES (%s, %s, %s, %s, %s, %s)", (self.ipc_id, self.production_unit, self.production_date, self.harvest_date, self.plantation_name, self.site_name))

class STOCK:
    def __init__(self, BATCH: BATCH, package_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')):
        self.package_date = package_date
        self.production_unit = BATCH.production_unit
        self.production_date = BATCH.production_date
        self.harvest_date = BATCH.harvest_date
        self.plantation_name = BATCH.plantation_name
        self.site_name = BATCH.site_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO STOCK (package_date, production_unit, production_date, harvest_date, plantation_name, site_name) VALUES (%s, %s, %s, %s, %s, %s)", (self.package_date, self.production_unit, self.production_date, self.harvest_date, self.plantation_name, self.site_name))
    

    
class CLIENT:
    def __init__(self):
        self.client_id = random.randint(100000000, 999999999)
    def insert(self, cursor):
        cursor.execute("INSERT INTO CLIENT (client_id) VALUES (%s)", (self.client_id,))
        
class SALES_DEPARTMENT:
    def __init__(self, name):
        self.sales_department_id = random.randint(100000000, 999999999)
        self.sales_department_name = name
    def insert(self, cursor):
        cursor.execute("INSERT INTO SALES_DEPARTMENT (sales_department_id, sales_department_name) VALUES (%s, %s)", (self.sales_department_id, self.sales_department_name))
    
class SALES_ASSOCIATE:
    def __init__(self, SALES_DEPARTMENT: SALES_DEPARTMENT):
        self.sales_associate_id = random.randint(100000000, 999999999)
        self.sales_department_id = SALES_DEPARTMENT.sales_department_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO SALES_ASSOCIATE (sales_associate_id, sales_department_id) VALUES (%s, %s)", (self.sales_associate_id, self.sales_department_id))
        
class SALES_MANAGER:
    def __init__(self, SALES_DEPARTMENT: SALES_DEPARTMENT):
        self.sales_manager_id = random.randint(100000000, 999999999)
        self.sales_department_id = SALES_DEPARTMENT.sales_department_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO SALES_MANAGER (sales_manager_id, sales_department_id) VALUES (%s, %s)", (self.sales_manager_id, self.sales_department_id))
        
class SALE:
    def __init__(self, SALES_ASSOCIATE: SALES_ASSOCIATE, 
                CLIENT: CLIENT,
                STOCK: STOCK):
        self.sale_id = random.randint(100000000, 999999999)
        self.sales_associate_id = SALES_ASSOCIATE.sales_associate_id
        self.client_id = CLIENT.client_id
        self.package_date = STOCK.package_date
        self.production_unit = STOCK.production_unit
        self.production_date = STOCK.production_date
        self.harvest_date = STOCK.harvest_date
        self.plantation_name = STOCK.plantation_name
        self.site_name = STOCK.site_name
    def insert(self, cursor):
        cursor.execute("INSERT INTO SALE (sale_id, sales_associate_id, client_id, package_date, production_unit, production_date, harvest_date, plantation_name, site_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.sale_id, self.sales_associate_id, self.client_id, self.package_date, self.production_unit, self.production_date, self.harvest_date, self.plantation_name, self.site_name))

class Database_API:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'aaaa'
         
    def connect(self, verbose = False):   
        try:
            # Establish a connection to the MySQL server
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )

            # Create a cursor object
            self.cursor = self.connection.cursor()
            if verbose == True:
                print("Connected to the database")

            # Return both the connection and cursor
            #return connection, cursor

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
    def disconnect(self, verbose = False):
        try:
            # Close the cursor and connection
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None and self.connection.is_connected():
                self.connection.close()
                if verbose == True:
                    print("Disconnected from the database")

        except Exception as e:
            print(f"Error during disconnection: {e}")
        
    def query(self, q, verbose = False):
        try:
            self.connect()
            self.cursor.execute("USE SOYBEAN;")
            
            # Execute the query
            self.cursor.execute(q)
            self.connection.commit()
                        
            self.disconnect()

             
        except mysql.connector.Error as err:
            print(f"Error: {err}")  
            
    def insert(self, q, t, verbose = False):
        try:
            self.connect()
            self.cursor.execute("USE SOYBEAN;")
            
            # Execute the query
            self.cursor.execute(q, t)
            
            self.connection.commit()
                        
            self.disconnect()

                
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    def fetch(self, q, verbose = False):
        try:
            self.connect()
            self.cursor.execute("USE SOYBEAN;")
            
            # Execute the query
            self.cursor.execute(q)

            # Fetch all the records
            records = self.cursor.fetchall()
                        
            self.disconnect()

            # Print each row
            if verbose:
                for row in records:
                    print(row)
                
            return records

                
        except mysql.connector.Error as err:
            print(f"Error: {err}") 
            
    def from_query_dep(self, cls, *args):
        instance = cls.__new__(cls)
        instance.__init__(*args)
        return instance
    
    def create_from_query(cls, *args):
        if len(args) != len(cls.__init__.__code__.co_varnames):
            raise ValueError(f"Expected {len(cls.__init__.__code__.co_varnames)} arguments, but got {len(args)}")

        instance = super(cls, cls).__new__(cls)
        for attr, value in zip(cls.__init__.__code__.co_varnames, args):
            setattr(instance, attr, value)
        return instance
        
    def create_database(self):

        self.cursor.execute("""
                    CREATE DATABASE IF NOT EXISTS SOYBEAN;
                    """)

        self.cursor.execute("""
                    USE SOYBEAN;
                    """)

        #==========================|  PLANTATION  |=================================
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PLANTATION (
                        -- primary key:
                        plantation_name VARCHAR(255) PRIMARY KEY,
                        
                        -- extra:
                        plantation_address VARCHAR(511)
                    )
                    """)
        
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS FIELD (
                            -- primary key:
                            field_number INT PRIMARY KEY,
                            
                            -- foreign key:
                            plantation_name VARCHAR(255),
                            
                            -- extra:
                            plant_date DATE,
                            grow_time INT,
                            planted BOOLEAN DEFAULT FALSE,
                                                        
                            FOREIGN KEY (plantation_name) REFERENCES PLANTATION (plantation_name) 
                        )                           
                            """)

        self.cursor.execute("""
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

        self.cursor.execute("""
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

        self.cursor.execute("""
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

        self.cursor.execute("""
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

        self.cursor.execute("""
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
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS SITE (
                        -- primary key: 
                        site_name VARCHAR(255) PRIMARY KEY
                    )
                    """)

        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS SITE_WORKER (
                        -- primary key:
                        employee_id VARCHAR(36) PRIMARY KEY,
                        
                        -- foreign key: 
                        site_name VARCHAR(255),
                        
                        FOREIGN KEY (site_name) REFERENCES SITE(site_name)
                    )
                    """)

        self.cursor.execute("""
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

        self.cursor.execute("""
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

        self.cursor.execute("""
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

        self.cursor.execute("""
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
        self.cursor.execute("""
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

        self.cursor.execute("""
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

        self.cursor.execute("""
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

        self.cursor.execute("""
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

        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS CLIENT (
                        client_id INT PRIMARY KEY
                    )
                    """)

        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS SALES_DEPARTMENT (
                        sales_department_id INT PRIMARY KEY,
                        sales_department_name VARCHAR(255) -- Add additional fields as needed
                    )
                    """)

        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS SALES_MANAGER (
                        sales_manager_id INT PRIMARY KEY,
                        sales_department_id INT,
                        FOREIGN KEY (sales_department_id) REFERENCES SALES_DEPARTMENT (sales_department_id)
                    )
                    """)

        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS SALES_ASSOCIATE (
                        sales_associate_id INT PRIMARY KEY,
                        sales_department_id INT,
                        FOREIGN KEY (sales_department_id) REFERENCES SALES_DEPARTMENT (sales_department_id)
                    )
                    """)

        self.cursor.execute("""
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
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS INVOICE ( -- do we need this?
                        invoice_id INT PRIMARY KEY,
                        sale_id INT,
                        FOREIGN KEY (sale_id) REFERENCES SALE(sale_id)
                    )
                    """)
        self.connection.commit()

    def populate_database(self):
        site_names = ["New York"]
        SITE_NUMBERS = 1
        SITE_WORKERS_PER_SITE = 10
        RATIO_TEMPORARY_PERMANENT = 0.5
        site_list = []
        for site_name in site_names:
            site = SITE(site_name)
            site_list.append(site)
            site.insert(self.cursor)
            for j in range(0,SITE_WORKERS_PER_SITE):
                employee = SITE_WORKER(site)
                employee.insert(self.cursor)
                contract = SW_CONTRACT(employee)
                contract.insert(self.cursor)
                if random.random() < RATIO_TEMPORARY_PERMANENT:
                    temporary_contract = SW_TEMPORARY_CONTRACT(contract)
                    temporary_contract.insert(self.cursor)
                else:
                    permanent_contract = SW_PERMANENT_CONTRACT(contract)
                    permanent_contract.insert(self.cursor)
                # works_at_site = WORKS_AT_SITE(employee, site)
                # works_at_site.insert(self.cursor)
            
            employee = SITE_WORKER(site)
            employee.insert(self.cursor)
            contract = SW_CONTRACT(employee)
            contract.insert(self.cursor)
            permanent_contract = SW_PERMANENT_CONTRACT(contract)
            permanent_contract.insert(self.cursor)
            site_manager = SITE_MANAGER(employee, site)
            site_manager.insert(self.cursor)
            
            
        plantation_names = ["Jersey City"]
        PLANTATION_NUMBERS = 1
        PLANTATION_WORKERS_PER_PLANTATION = 10
        RATIO_TEMPORARY_PERMANENT = 0.5
        NUMBER_OF_FIELDS = 10
        plantation_list = []
        for plantation_name in plantation_names:
            plantation = PLANTATION(plantation_name)
            plantation_list.append(plantation)
            plantation.insert(self.cursor)
            
            for j in range(0,NUMBER_OF_FIELDS):
                field = FIELD(plantation, j)
                field.insert(self.cursor)
            
            for j in range(0,PLANTATION_WORKERS_PER_PLANTATION):
                employee = PLANTATION_WORKER(plantation)
                employee.insert(self.cursor)
                contract = PW_CONTRACT(employee)
                contract.insert(self.cursor)
                if random.random() < RATIO_TEMPORARY_PERMANENT:
                    temporary_contract = PW_TEMPORARY_CONTRACT(contract)
                    temporary_contract.insert(self.cursor)
                else:
                    permanent_contract = PW_PERMANENT_CONTRACT(contract)
                    permanent_contract.insert(self.cursor)
                # works_at_plantation = WORKS_AT_PLANTATION(employee, plantation)
                # works_at_plantation.insert(self.cursor)
            
            employee = PLANTATION_WORKER(plantation)
            employee.insert(self.cursor)
            contract = PW_CONTRACT(employee)
            contract.insert(self.cursor)
            permanent_contract = PW_PERMANENT_CONTRACT(contract)
            permanent_contract.insert(self.cursor)
            plantation_manager = PLANTATION_MANAGER(employee, plantation)
            plantation_manager.insert(self.cursor)
            
        sales_department_names = ["Tokyo"]
        SALES_DEPARTMENT_NUMBER = len(sales_department_names)
        NUMBER_OF_SALES_ASSOCIATES = 1
        sales_department_list = []
        sales_associate_list = []
        for sales_department_name in sales_department_names:
            sales_department = SALES_DEPARTMENT(sales_department_name)
            sales_department.insert(self.cursor)
            sales_department_list.append(sales_department)
            for j in range(0, NUMBER_OF_SALES_ASSOCIATES):
                sales_associate = SALES_ASSOCIATE(sales_department)
                sales_associate.insert(self.cursor)
                sales_associate_list.append(sales_associate)
            sales_manager = SALES_MANAGER(sales_department)
            sales_manager.insert(self.cursor)

        DEPLETED_STOCK_ITEMS = 10
        AVAILABLE_STOCK_ITEMS = 1
        BATCHES_PER_INVENTORY = 1
        IPC_PER_BATCH = 1
        stock_list = []
        for site_instance in site_list:
            for plantation_instance in plantation_list:
                inventory = INVENTORY(site_instance, plantation_instance)
                inventory.insert(self.cursor)
                for i in range(0,BATCHES_PER_INVENTORY):
                    batch = BATCH(inventory)
                    batch.insert(self.cursor)
                    for j in range(0,IPC_PER_BATCH):
                        ipc = IPC(batch)
                        ipc.insert(self.cursor)
                    stock = STOCK(batch)
                    stock_list.append(stock)
                    stock.insert(self.cursor)
                    
        CLIENT_NUMBERS = 1
        client_list = []
        for i in range(0, CLIENT_NUMBERS):
            client = CLIENT()
            client_list.append(client)
            client.insert(self.cursor)
            
        for stock_instance in stock_list:
            buyer = client_list[random.randint(0, CLIENT_NUMBERS-1)]
            seller = sales_associate_list[random.randint(0, NUMBER_OF_SALES_ASSOCIATES-1)]
            sale = SALE(seller, buyer, stock_instance)
            sale.insert(self.cursor)

        self.connection.commit()
    
    def get(self, query, cls):
        self.connect()
        self.cursor.execute("USE SOYBEAN;")
        self.cursor.execute(query)
        column_names = [desc[0] for desc in self.cursor.description]
        results = self.cursor.fetchall()
        self.disconnect()
        return [cls.from_query(*row) for row in results]
        # return [cls(**dict(zip(column_names, row))) for row in results]
    
    def display_plantations(self):
        fields = self.get("SELECT * FROM FIELD", FIELD)
        for field in fields:
            print(f"{field.field_number} {field.plant_date} {field.grow_time} {field.plantation_name}")
            
    def harvest_soybeans(plantation, field_number):

        pass   
    
    def get_stock(self):
        pass
    
    def load_model(self, model_json_file, model_weights_file):
        json_file_path = './lake/cv/model.json'
        with open(json_file_path, 'r') as json_file:
            loaded_model_json = json_file.read()

        # Create the model from the loaded JSON
        loaded_model = model_from_json(loaded_model_json)

        # Load the weights into the model
        loaded_model.load_weights("./lake/cv/model_weights.h5")

        # Compile the loaded model (you might need to compile it with the same configuration as when you saved it)
        loaded_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return loaded_model

    def generate_field_images(self, ratio_soil_soybean, number_of_images = 100):
        
        images = []
        for i in range(0,int(round(ratio_soil_soybean*100))):
            images.append("soil/" + random.choice(os.listdir("./lake/cv/dataset/soil")))
            
        for i in range(0,int(round((1-ratio_soil_soybean)*100))):
            images.append("soybean/" + random.choice(os.listdir("./lake/cv/dataset/soybean")))

        input = []
        image_size = (224, 224)  # Adjust to match VGG16 input size

        for image in images:
            image = cv2.imread(f"./lake/cv/dataset/{image}")
            img = cv2.resize(image, image_size)
            input.append(img)

        input = np.array(input)
        input = tf.keras.applications.vgg16.preprocess_input(input)
                
        return(input)
        