def verify(username, password):
    '''This function retrieves user data from the
    database and check it against password provided'''
    import sqlite3
    # Connect/ Create this databse file
    conn = sqlite3.connect('user_data.db')

    # creating a cursor object to execute sql commands

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    if user and user[2] == password:
        authority = user[3]
        conn.close()
        return authority
    conn.close()
    return None # invalid credentials oR USER don't exist
        
    
    
def get_all_data():
    '''raw data of all users'''
    import sqlite3
    
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Fetch all data
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    
    return data
