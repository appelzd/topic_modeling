
import pandas
import pyodbc
from config import Configuration


class Db:

    def writeTopics(self, topic):
        sql_con = pyodbc.connect(Configuration.GetDbConnectionString())
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
        sql_con = pyodbc.connect(Configuration.GetDbConnectionString())

        cursor = sql_con.cursor()
     
        #cursor.execute('INSERT INTO Topics(name) values(?)', topic)
        
        sql_con.commit()
        cursor.close()
        sql_con.close()
