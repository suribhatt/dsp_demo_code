from .model import Model

class Hall(Model):
    
    def add_hall(self, vals):
        status = False
        response = ''
        session_key = vals.get('session_key',False)
        if not session_key:
            response = 'Session key is Required'
        else:
            if not self.validate_session_key(session_key):
                response = 'Session key is not valid'
            else:
                name = vals.get('name',False)
                capacity = vals.get('capacity',False)
                if not name or not capacity:
                    response = 'name and capacity are required to add hall,please check the api request'
                else:
                    query = "INSERT INTO hall (name, capacity) VALUES ('%s', %i)"%(name,capacity)
                    execute_response = self.execute(query)
                    if execute_response.get('status'):
                        get_last_id = self.get_last_id('hall')
                        status = get_last_id.get('status')
                        if status:
                            response = {'id_hall':get_last_id['response'][0][0]}
                    else:
                        response = execute_response.get('response')
        return status,response