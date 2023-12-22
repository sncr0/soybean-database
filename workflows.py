from API import *
api = Database_API()
api.connect()
api.create_database()
api.populate_database()

api.plant_field([2], "Jersey City")
field_list = api.get("SELECT * FROM FIELD WHERE field_number = 2 AND PLANTATION_NAME = \"Jersey City\"", FIELD)

api.load_model("./lake/cv/model.json", "./lake/cv/model.h5")
images = api.generate_field_images(0.95, 10)
predicted_fraction = api.predict_fraction(images, field_list[0],  0.95)
predicted_total_cost = api.predict_total_cost(predicted_fraction)

url = api.push_to_azure(field_list[0], images)

# First harvest: no correction
api.harvest_soybeans("Jersey City", "New York", 2, url = url, prediction = predicted_total_cost)

inventory_list = api.get(f"SELECT * FROM INVENTORY WHERE site_name = \"New York\" AND plantation_name = \"Jersey City\" AND harvest_date = \"2023-12-22\"", INVENTORY)
api.start_batch(inventory_list[0], 0)

batch_list = api.get(f"SELECT * FROM BATCH WHERE site_name = \"New York\" AND plantation_name = \"Jersey City\" AND harvest_date = \"2023-12-22\" AND production_unit = 0 AND production_date = \"2023-12-22\"", BATCH)
actual_production_cost = 6.25 # corresponds to 100% yield
api.finish_batch(batch_list[0], production_cost = actual_production_cost, price = actual_production_cost*api.markup )

images = api.generate_field_images(0.3, 10)

field_list = api.get("SELECT * FROM FIELD WHERE field_number = 3 AND PLANTATION_NAME = \"Jersey City\"", FIELD)

predicted_fraction = api.predict_fraction(images, field_list[0], 0.3)
predicted_total_cost = api.predict_total_cost(predicted_fraction)

field_list = api.get("SELECT * FROM FIELD WHERE field_number = 3 AND PLANTATION_NAME = \"Jersey City\"", FIELD)
url = api.push_to_azure(field_list[0], images)

api.correct_price("Jersey City")