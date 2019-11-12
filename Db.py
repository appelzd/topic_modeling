
import pandas
import pyodbc



class Db:

    def write(self, weight, name):
        sql_con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server=tcp:csdev.database.windows.net,1433;Database=anvesademo20_Copy20191003;Trusted_Connection=no;UID=csadmin;Pwd=c$admin14500')

        cursor = sql_con.cursor()
     
        cursor.execute('INSERT INTO PyTest(name, weight) values(?, ?)', name, weight)    

        sql_con.commit()
        cursor.close()
        sql_con.close()

