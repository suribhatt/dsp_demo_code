import re
import json
import mysql.connector
message = 'All Tables Created SuccessFully'
data = {}
with open('config.json') as f:
  data = json.load(f)
if data:
    database_data = data['database']
    mydb = mysql.connector.connect(
    host= database_data.get('host'),
    user=database_data.get('user'),
    password=database_data.get('password'),
    database=database_data.get('database')
    )
    mycursor = mydb.cursor()
    query = ''
    for line in open('install.sql'):
        if not re.search(r';$', line):
            query+= line
        else:
            query+= line
            try:
                mycursor.execute(query)
            except Exception as e:
                message =  "Error While Creating Tables '%s'"%str(e)
            query = ''
else:
    message = 'Unable To Load Json File'
print(message)