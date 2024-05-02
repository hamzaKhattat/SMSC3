from mysql.connector import connect
import pandas as pd
def get_all_data():
        connection = connect(host="localhost", user="root", password="", database="templates")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM generator")  # Fixed typo 'sekect' to 'SELECT'
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        connection.close()
        return rows 
print(get_all_data())
