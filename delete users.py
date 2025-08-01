import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/database.db')

# Create a cursor object
cursor = conn.cursor()

# Execute the SQL command to delete the table
cursor.execute("DROP TABLE IF EXISTS users")

# Commit the changes
conn.commit()

# Close the connection
conn.close()