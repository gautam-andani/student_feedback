import pandas as pd
import sqlite3

def enter_through_excel(path):
# Read the Excel file into a pandas DataFrame

    df = pd.read_excel(path)
    print(df)
    # Connect to the database
    conn = sqlite3.connect('user_data.db')

    # # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    successful = 0
    error = []
    # # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract the data from each column
        
        column1 = row['name']
        column2 = row['authority']
        print(column1,column2)
        # the SQL query
        query = f"INSERT INTO users (username, password, authority) VALUES ('{column1}', '{column1}','{column2}')"
        

        # Execute the SQL query
        try:
            cursor.execute(query)
            successful+=1
        except sqlite3.Error as e:
            error.append(f"{str(e)} error in line {index}")

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()
    return successful,error

# enter_through_excel('uploads/Book1.xlsx')