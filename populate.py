import mysql.connector
import csv
from infra import *
import time
from faker import Faker
import random

fake = Faker()

class SITE:
    def __init__(self):
        self.site_id = random.randint(100000000, 999999999)
    def insert(self, cursor):
        cursor.execute("INSERT INTO SITES (site_id) VALUES (%s)", (self.site_id,))

class EMPLOYEE:
    def __init__(self, SITE: SITE):
        self.employee_id = random.randint(100000000, 999999999)
        self.site_id = SITE.site_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO EMPLOYEE (employee_id, site_id) VALUES (%s, %s)", (self.employee_id, self.site_id))

class CONTRACT:
    def __init__(self, EMPLOYEE: EMPLOYEE):
        self.contract_id = random.randint(100000000, 999999999)
        self.site_id = EMPLOYEE.site_id
        self.employee_id = EMPLOYEE.employee_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO CONTRACT (contract_id, site_id, employee_id) VALUES (%s, %s, %s)", (self.contract_id, self.site_id, self.employee_id))

class TEMPORARY_CONTRACT:
    def __init__(self, CONTRACT: CONTRACT):
        self.temp_contract_id = random.randint(100000000, 999999999)
        self.contract_id = CONTRACT.contract_id
        self.site_id = CONTRACT.site_id
        self.employee_id = CONTRACT.employee_id
        self.start_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
        self.end_date = fake.date_between(start_date='today', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
    def insert(self, cursor):
        cursor.execute("INSERT INTO TEMPORARY_CONTRACT (temp_contract_id, contract_id, site_id, employee_id, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)", (self.temp_contract_id, self.contract_id, self.site_id, self.employee_id, self.start_date, self.end_date))
        
class PERMANENT_CONTRACT:
    def __init__(self, CONTRACT: CONTRACT):
        self.perm_contract_id = random.randint(100000000, 999999999)
        self.contract_id = CONTRACT.contract_id
        self.site_id = CONTRACT.site_id
        self.employee_id = CONTRACT.employee_id
        self.start_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
    def insert(self, cursor):
        cursor.execute("INSERT INTO PERMANENT_CONTRACT (perm_contract_id, contract_id, site_id, employee_id, start_date) VALUES (%s, %s, %s, %s, %s)", (self.perm_contract_id, self.contract_id, self.site_id, self.employee_id, self.start_date))
        
class SITE_MANAGER:
    def __init__(self, EMPLOYEE: EMPLOYEE, SITE: SITE):
        self.site_manager_id = random.randint(100000000, 999999999)
        self.employee_id = EMPLOYEE.employee_id
        self.site_id = SITE.site_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO SITE_MANAGER (site_manager_id, employee_id, site_id) VALUES (%s, %s, %s)", (self.site_manager_id, self.employee_id, self.site_id))
        
class SUPPLIER:
    def __init__(self):
        self.supplier_id = random.randint(100000000, 999999999)
    def insert(self, cursor):
        cursor.execute("INSERT INTO SUPPLIER (supplier_id) VALUES (%s)", (self.supplier_id))
        
class WORKS_AT_SITE:
    def __init__(self, EMPLOYEE: EMPLOYEE, SITE: SITE):
        self.employee_id = EMPLOYEE.employee_id
        self.site_id = SITE.site_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO WORKS_AT_SITE (employee_id, site_id) VALUES (%s, %s)", (self.employee_id, self.site_id))

class INVENTORY:
    def __init__(self, SITE: SITE, SUPPLIER: SUPPLIER):
        self.inventory_id = random.randint(100000000, 999999999)
        self.site_id = SITE.site_id
        self.supplier_id = SUPPLIER.supplier_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO INVENTORY (inventory_id, site_id, supplier_id) VALUES (%s, %s, %s)", (self.inventory_id, self.site_id, self.supplier_id))
        
class BATCH:
    def __init__(self, INVENTORY: INVENTORY):
        self.batch_id = random.randint(100000000, 999999999)
        self.inventory_id = INVENTORY.inventory_id
        self.supplier_id = INVENTORY.supplier_id
        self.site_id = INVENTORY.site_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO BATCH (batch_id, inventory_id, supplier_id, site_id) VALUES (%s, %s, %s, %s)", (self.batch_id, self.inventory_id, self.supplier_id, self.site_id))

class IPC:
    def __init__(self, BATCH: BATCH):
        self.ipc_id = random.randint(100000000, 999999999)
        self.batch_id = BATCH.batch_id
        self.inventory_id = BATCH.inventory_id
        self.supplier_id = BATCH.supplier_id
        self.site_id = BATCH.site_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO IPC (ipc_id, batch_id, inventory_id, supplier_id, site_id) VALUES (%s, %s, %s, %s, %s)", (self.ipc_id, self.batch_id, self.inventory_id, self.supplier_id, self.site_id))

class STOCK:
    def __init__(self, BATCH: BATCH):
        self.stock_id = random.randint(100000000, 999999999)
        self.batch_id = BATCH.batch_id
        self.inventory_id = BATCH.inventory_id
        self.supplier_id = BATCH.supplier_id
        self.site_id = BATCH.site_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO STOCK (stock_id, batch_id, inventory_id, supplier_id, site_id) VALUES (%s, %s, %s, %s, %s)", (self.stock_id, self.batch_id, self.inventory_id, self.supplier_id, self.site_id))
        
class CLIENT:
    def __init__(self):
        self.client_id = random.randint(100000000, 999999999)
    def insert(self, cursor):
        cursor.execute("INSERT INTO CLIENT (client_id) VALUES (%s)", (self.client_id))
        
class SALES_DEPARTMENT:
    def __init__(self):
        self.sales_department_id = random.randint(100000000, 999999999)
        self.department_name = "AAAA"
    def insert(self, cursor):
        cursor.execute("INSERT INTO SALES_DEPARTMENT (sales_department_id, department_name) VALUES (%s, %s)", (self.sales_department_id, self.department_name))
    
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
        self.stock_id = STOCK.stock_id
        self.batch_id = STOCK.batch_id
        self.inventory_id = STOCK.inventory_id
        self.supplier_id = STOCK.supplier_id
        self.site_id = STOCK.site_id
    def insert(self, cursor):
        cursor.execute("INSERT INTO SALE (sale_id, sales_associate_id, client_id, stock_id, batch_id, inventory_id, supplier_id, site_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (self.sale_id, self.sales_associate_id, self.client_id, self.stock_id, self.batch_id, self.inventory_id, self.supplier_id, self.site_id))

connection, cursor = connect_to_database()
cursor.execute("""
               USE SOYBEAN;
               """)

SITE_NUMBERS = 1
EMPLOYEES_PER_SITE = 10
RATIO_TEMPORARY_PERMANENT = 0.5
for i in range(0,SITE_NUMBERS):
    site = SITE()
    site.insert(cursor)
    for j in range(0,EMPLOYEES_PER_SITE):
        employee = EMPLOYEE(site)
        employee.insert(cursor)
        contract = CONTRACT(employee)
        contract.insert(cursor)
        if random.random() < RATIO_TEMPORARY_PERMANENT:
            temporary_contract = TEMPORARY_CONTRACT(contract)
            temporary_contract.insert(cursor)
        else:
            permanent_contract = PERMANENT_CONTRACT(contract)
            permanent_contract.insert(cursor)
        works_at_site = WORKS_AT_SITE(employee, site)
        works_at_site.insert(cursor)
    
    employee = EMPLOYEE(site)
    employee.insert(cursor)
    contract = CONTRACT(employee)
    contract.insert(cursor)
    permanent_contract = PERMANENT_CONTRACT(contract)
    permanent_contract.insert(cursor)
    site_manager = SITE_MANAGER(employee, site)
    site_manager.insert(cursor)
    
connection.commit()

disconnect_from_database(connection, cursor)