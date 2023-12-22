from flask import Flask, render_template, request
from API import *
import json

api = Database_API()
app = Flask(__name__)

# @app.route('/redpurchase')
# def display_inventory():
#     stock_objects = api.get("SELECT * FROM STOCK", STOCK)
#     return render_template('redinventory.html', inventory_data=stock_objects)

# @app.route('/purchase')
# def display_inventory():
#     stock_objects = api.get("SELECT * FROM STOCK", STOCK)
#     return render_template('inventory.html', inventory_data=stock_objects)

@app.route('/inventory', methods=['GET'])
def list_inventory():
    stock_objects = api.get("SELECT * FROM STOCK", STOCK)
    return render_template('inventory.html', inventory_data=stock_objects)

    # plantation_name = request.form.get('plantation_name')
    # price = request.form.get('price')

    # # Perform any necessary actions for the purchase
    # # For example, update the database or perform any other operation

    # # Return the purchased item information
    # purchased_item = {'plantation_name': plantation_name, 'price': price}
    # return render_template('inventory.html', purchased_item=purchased_item)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase_item():
    
                                #     <input type="hidden" name="package_date" value="{{ item.package_date }}">
                                # <input type="hidden" name="production_unit" value="{{ item.production_unit }}">
                                # <input type="hidden" name="production_date" value="{{ item.plantation_name }}">
                                # <input type="hidden" name="harvest_date" value="{{ item.plantation_name }}">
                                # <input type="hidden" name="plantation_name" value="{{ item.plantation_name }}">
                                # <input type="hidden" name="field_number" value="{{ item.field_number }}">
                                # <input type="hidden" name="site_name" value="{{ item.site_name }}">
    
    package_date = request.form.get('package_date')
    print(f"package_date: {package_date}")
    production_unit = request.form.get('production_unit')
    print(f"production_unit: {production_unit}")
    production_date = request.form.get('production_date')
    print(f"production_date: {production_date}")
    harvest_date = request.form.get('harvest_date')
    print(f"harvest_date: {harvest_date}")
    plantation_name = request.form.get('plantation_name')
    print(f"plantation_name: {plantation_name}")
    field_number = request.form.get('field_number')
    print(f"field_number: {field_number}")
    site_name = request.form.get('site_name')
    print(f"site_name: {site_name}")
    purchase = api.query(f"""
            UPDATE STOCK
            SET sold = 1
            WHERE package_date = '{package_date}' AND production_unit = '{production_unit}' AND production_date = '{production_date}' AND harvest_date = '{harvest_date}' AND plantation_name = '{plantation_name}' AND field_number = '{field_number}' AND site_name = '{site_name}'
            """, STOCK)
    api.query(f"""
            INSERT INTO SALE (sale_id, package_date, production_unit, production_date, harvest_date, plantation_name, field_number, site_name) VALUES (1, '{package_date}', '{production_unit}', '{production_date}', '{harvest_date}', '{plantation_name}', '{field_number}', '{site_name}')
              """)
    
    
    
    
    # item = json.loads(item_json)
    return "Purchase successful!"
    # Use the 'item' dictionary to perform any necessary actions for the purchase
    # For example, you can access item['plantation_name'], item['price'], etc.

    # Return a response (you can replace this with the information you want to send back)
    # response_message = f'Item purchased!\nPlantation Name: {item["plantation_name"]}, Price: {item["price"]}'
    # return render_template('purchase_response.html', response_message=response_message)


# @app.route('/login')
# def display_inventory():
#     return render_template('inventory.html')

@app.route('/buy', methods=['POST'])
def buy_item():
    item_id = request.form.get('item_id')
    return "Purchase successful!"  # Provide feedback to the user

if __name__ == '__main__':
    app.run(debug=True)
