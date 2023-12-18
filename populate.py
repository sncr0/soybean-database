import mysql.connector
import csv
from infra import *
import time
from faker import Faker
import random
import uuid

fake = Faker()

# =================================|  SITE  |=======================================
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
        
# class WORKS_AT_SITE:
#     def __init__(self, SITE_WORKER: SITE_WORKER, SITE: SITE):
#         self.employee_id = SITE_WORKER.employee_id
#         self.site_id = SITE.site_id
#     def insert(self, cursor):
#         cursor.execute("INSERT INTO WORKS_AT_SITE (employee_id, site_id) VALUES (%s, %s)", (self.employee_id, self.site_id))

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

connection, cursor = connect_to_database()
cursor.execute("""
               USE SOYBEAN;
               """)

site_names = ["New York"]
SITE_NUMBERS = 1
SITE_WORKERS_PER_SITE = 10
RATIO_TEMPORARY_PERMANENT = 0.5
site_list = []
for site_name in site_names:
    site = SITE(site_name)
    site_list.append(site)
    site.insert(cursor)
    for j in range(0,SITE_WORKERS_PER_SITE):
        employee = SITE_WORKER(site)
        employee.insert(cursor)
        contract = SW_CONTRACT(employee)
        contract.insert(cursor)
        if random.random() < RATIO_TEMPORARY_PERMANENT:
            temporary_contract = SW_TEMPORARY_CONTRACT(contract)
            temporary_contract.insert(cursor)
        else:
            permanent_contract = SW_PERMANENT_CONTRACT(contract)
            permanent_contract.insert(cursor)
        # works_at_site = WORKS_AT_SITE(employee, site)
        # works_at_site.insert(cursor)
    
    employee = SITE_WORKER(site)
    employee.insert(cursor)
    contract = SW_CONTRACT(employee)
    contract.insert(cursor)
    permanent_contract = SW_PERMANENT_CONTRACT(contract)
    permanent_contract.insert(cursor)
    site_manager = SITE_MANAGER(employee, site)
    site_manager.insert(cursor)
    
    
plantation_names = ["Jersey City"]
PLANTATION_NUMBERS = 1
PLANTATION_WORKERS_PER_PLANTATION = 10
RATIO_TEMPORARY_PERMANENT = 0.5
plantation_list = []
for plantation_name in plantation_names:
    plantation = PLANTATION(plantation_name)
    plantation_list.append(plantation)
    plantation.insert(cursor)
    for j in range(0,PLANTATION_WORKERS_PER_PLANTATION):
        employee = PLANTATION_WORKER(plantation)
        employee.insert(cursor)
        contract = PW_CONTRACT(employee)
        contract.insert(cursor)
        if random.random() < RATIO_TEMPORARY_PERMANENT:
            temporary_contract = PW_TEMPORARY_CONTRACT(contract)
            temporary_contract.insert(cursor)
        else:
            permanent_contract = PW_PERMANENT_CONTRACT(contract)
            permanent_contract.insert(cursor)
        # works_at_plantation = WORKS_AT_PLANTATION(employee, plantation)
        # works_at_plantation.insert(cursor)
    
    employee = PLANTATION_WORKER(plantation)
    employee.insert(cursor)
    contract = PW_CONTRACT(employee)
    contract.insert(cursor)
    permanent_contract = PW_PERMANENT_CONTRACT(contract)
    permanent_contract.insert(cursor)
    plantation_manager = PLANTATION_MANAGER(employee, plantation)
    plantation_manager.insert(cursor)
    
sales_department_names = ["Tokyo"]
SALES_DEPARTMENT_NUMBER = len(sales_department_names)
NUMBER_OF_SALES_ASSOCIATES = 1
sales_department_list = []
sales_associate_list = []
for sales_department_name in sales_department_names:
    sales_department = SALES_DEPARTMENT(sales_department_name)
    sales_department.insert(cursor)
    sales_department_list.append(sales_department)
    for j in range(0, NUMBER_OF_SALES_ASSOCIATES):
        sales_associate = SALES_ASSOCIATE(sales_department)
        sales_associate.insert(cursor)
        sales_associate_list.append(sales_associate)
    sales_manager = SALES_MANAGER(sales_department)
    sales_manager.insert(cursor)

DEPLETED_STOCK_ITEMS = 10
AVAILABLE_STOCK_ITEMS = 1
BATCHES_PER_INVENTORY = 1
IPC_PER_BATCH = 1
stock_list = []
for site_instance in site_list:
    for plantation_instance in plantation_list:
        inventory = INVENTORY(site_instance, plantation_instance)
        inventory.insert(cursor)
        for i in range(0,BATCHES_PER_INVENTORY):
            batch = BATCH(inventory)
            batch.insert(cursor)
            for j in range(0,IPC_PER_BATCH):
                ipc = IPC(batch)
                ipc.insert(cursor)
            stock = STOCK(batch)
            stock_list.append(stock)
            stock.insert(cursor)
            
CLIENT_NUMBERS = 1
client_list = []
for i in range(0, CLIENT_NUMBERS):
    client = CLIENT()
    client_list.append(client)
    client.insert(cursor)
    
for stock_instance in stock_list:
    buyer = client_list[random.randint(0, CLIENT_NUMBERS-1)]
    seller = sales_associate_list[random.randint(0, NUMBER_OF_SALES_ASSOCIATES-1)]
    sale = SALE(seller, buyer, stock_instance)
    sale.insert(cursor)

connection.commit()

disconnect_from_database(connection, cursor)