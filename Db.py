
import pandas
import pyodbc



class Db:

    def writeTopics(self, topic):
        sql_con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server=tcp:csdev.database.windows.net,1433;Database=anvesademo20_Copy20191003;Trusted_Connection=no;UID=csadmin;Pwd=c$admin14500')

        tmp = topic.split('+')
        
            
        cursor = sql_con.cursor()
     
        cursor.execute('INSERT INTO Topics(name) values(?)', topic)
        
        curse = cursor.execute('select @@IDENTITY') 
        id = curse.fetchval()
        
        for t in tmp:
            a = t.split('"') 
            cursor.execute('INSERT INTO TopicWords(TopicId ,name, weight) values(?,?, ?)', id, a[1], a[0][:-1])    

        sql_con.commit()
        cursor.close()
        sql_con.close()

    def writeFilePrediction(self, filename, likelyhood, topicId):
        sql_con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server=tcp:csdev.database.windows.net,1433;Database=anvesademo20_Copy20191003;Trusted_Connection=no;UID=csadmin;Pwd=c$admin14500')

        cursor = sql_con.cursor()
     
        #cursor.execute('INSERT INTO Topics(name) values(?)', topic)
        
        sql_con.commit()
        cursor.close()
        sql_con.close()
