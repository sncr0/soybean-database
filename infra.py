import mysql.connector
host = 'localhost'
user = 'root'
password = 'aaaa'
#database = 'SOYBEAN'

def connect_to_database(host="localhost", user="root", password="aaaa"):#, database="cdmo"):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
            #database=database
        )

        # Create a cursor object
        cursor = connection.cursor()

        print("Connected to the database")

        # Return both the connection and cursor
        return connection, cursor

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def disconnect_from_database(connection, cursor):
    try:
        # Close the cursor and connection
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("Disconnected from the database")

    except Exception as e:
        print(f"Error during disconnection: {e}")
        