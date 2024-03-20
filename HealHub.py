import psycopg2

# Database connection parameters
host = "pgserver.mau.se"
database = "ao9145"
user = "ao9145"
password = "4wg0nyxw"
port = "5432"  # Default PostgreSQL port

# Establish a connection to the PostgreSQL server
try:
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    # Create a cursor to interact with the database
    cursor = connection.cursor()

    # Commit the changes
    connection.commit()

except psycopg2.Error as e:
    print(f"Error: Unable to connect to the database\n{e}")