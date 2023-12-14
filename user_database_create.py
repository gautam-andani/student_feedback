import sqlite3

# RUN THIS ONE TIME ONLY DURING SETUP

# Connect/ Create this databse file
conn = sqlite3.connect('user_data.db')

# creating a cursor object to execute sql commands
cursor = conn.cursor()

#  create table
# cursor.execute('''
#                CREATE TABLE users (
#                    id INTEGER PRIMARY KEY,
#                    username TEXT UNIQUE NOT NULL,
#                    password TEXT NOT NULL,
#                    authority TEXT NOT NULL
#                )
#                ''')

# # (?, ?, ?) placeholder provides security against SQL injections by preventing malicious users from altering the structure of the sql queries
# # Insert student data
# cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
#                ('gautam', 'gautam', 'student'))

# # Insert teacher data
# cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
#                ('teacher1', 'teacher1', 'teacher'))
# cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
#                ('teacher2', 'teacher2', 'teacher'))
# cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
#                ('teacher3', 'teacher3', 'teacher'))
# cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
#                ('teacher4', 'teacher4', 'teacher'))
# cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
#                ('teacher5', 'teacher5', 'teacher'))
# cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
#                ('teacher6', 'teacher6', 'teacher'))

# Insert other authories data like hod
# cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
            #    ('hod', 'hod', 'hod'))
cursor.execute("INSERT INTO users (username, password, authority) VALUES (?, ?, ?)",
               ('admin', 'admin', 'admin'))



conn.commit()
conn.close()