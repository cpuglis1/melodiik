import psycopg2

class DatabaseHandler:
    def __init__(self, dbname='postgres', host='localhost', port='5432'):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            host=self.host,
            port=self.port
        )
        self.cursor = self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_database(self, db_name):
        try:
            self.connect()
            self.connection.autocommit = True  # Enable autocommit mode to create a database
            self.cursor.execute(f'CREATE DATABASE {db_name};')
            print(f"Database '{db_name}' created successfully!")
        except Exception as error:
            print(f"Error: {error}")
        finally:
            self.close()

    def create_table(self, table_name, schema):
        try:
            self.connect()
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} {schema};')
            self.connection.commit()
        except Exception as error:
            print(f"Error: {error}")
        finally:
            self.close()

    def insert_data(self, table_name, formatted_data):
        try:
            self.connect()
            for entry in formatted_data:
                columns = ', '.join(entry.keys())
                placeholders = ', '.join(['%s'] * len(entry))
                values = tuple(entry.values())
                self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders});', values)
            self.connection.commit()
        except Exception as error:
            print(f"Error: {error}")
        finally:
            self.close()

    def select_data(self, table_name, columns="*", condition=None):
        try:
            self.connect()
            query = f"SELECT {columns} FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            query += ";"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Exception as error:
            print(f"Error: {error}")
            return []
        finally:
            self.close()


def to_integer(value):
    if value == 'N/A':
        return 0
    return int(value.replace(",", ""))

handler = DatabaseHandler(dbname='artist_stats_db')

# Select all rows from the "artist_stats" table
rows = handler.select_data("artist_stats")

# Print the rows
for row in rows:
    print(row)

'''
# Example Usage:
handler = DatabaseHandler()

# Create databases
handler.create_database('artist_disc_db')
handler.create_database('artist_stats_db')

# Use 'artist_stats_db' for further operations
handler.dbname = 'artist_stats_db'

# Create a table
table_name = "artist_stats"
schema = """
(
    "Artist Name" TEXT,
    "Listeners" INTEGER,
    "Plays" INTEGER,
    "URL" TEXT
);
"""
handler.create_table(table_name, schema)

# Insert data into the table
formatted_data = [
    {
        "Artist Name": "Example Artist",
        "Listeners": "2,345",
        "Plays": "123,456",
        "URL": "http://example.com"
    }
    # Add other artist data entries as needed
]
handler.insert_data(table_name, formatted_data)
'''
