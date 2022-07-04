from .db import Db
import json
from pathlib import Path
path = Path(__file__).parent / "../config.json"
class Model(Db):
    
    def validate_session_key(self,session_key):
        status = False
        data = {}
        with open(path) as f:
            data = json.load(f)
        if data:
            oursession_key = data['session_key']
            if oursession_key==session_key:
                status = True
        return status
