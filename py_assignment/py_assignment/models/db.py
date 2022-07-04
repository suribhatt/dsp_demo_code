import re
import json
import mysql.connector
from pathlib import Path
path = Path(__file__).parent / "../config.json"
class Db:
    _cr = None
    _conn = None

    def __init__(self):
        data = {}
        with open(path) as f:
            data = json.load(f)
        if data:
            try:
                database_data = data['database']
                self._conn = mysql.connector.connect(
                host= database_data.get('host'),
                user=database_data.get('user'),
                password=database_data.get('password'),
                database=database_data.get('database')
                )
                self._cr = self._conn.cursor(buffered=True)
            except:
                pass
    
    def __del__(self):
        if self._cr and self._conn:
            self._conn.close()
            self._cr.close()
            
    def execute(self,query):
        status,response = False,''
        try:
            response = self._cr.execute(query)
            status = True
        except Exception as e:
            response = str(e)
        return {'status':status,'response':response}
    
    def executeS(self,query):
        status,response = False,''
        try:
            self._cr.execute(query)
            response = self._cr.fetchall()
            status = True
        except Exception as e:
            response = str(e)
        return {'status':status,'response':response}
        
    def get_last_id(self, table):
        primary_key = 'id_%s'%table
        query = 'SELECT %s from %s ORDER BY %s DESC limit 1'%(primary_key,table,primary_key)
        response = self.executeS(query)
        return response
        


