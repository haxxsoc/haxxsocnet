import sqlite3
con = sqlite3.connect("instance/database.db")
cur = con.cursor()

#cur.execute("CREATE TABLE users(username, email, password)")
#cur.execute("""
#    INSERT INTO users VALUES
#        ('Admin', 'pixiehaxx@gmail.com', 'H@x4s0c0')""")
#con.commit()
res = cur.execute("SELECT business_name, value_value FROM data")
print(res.fetchall())