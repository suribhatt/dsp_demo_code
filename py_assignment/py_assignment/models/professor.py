from .model import Model

class Professor(Model):
    
    def add_professor(self, vals):
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
                if not name:
                    response = 'name is required to add professor,please check the api request'
                else:
                    query = "INSERT INTO professor (name) VALUES ('%s')"%(name)
                    execute_response = self.execute(query)
                    if execute_response.get('status'):
                        get_last_id = self.get_last_id('professor')
                        status = get_last_id.get('status')
                        if status:
                            response = {'id_professor':get_last_id['response'][0][0]}
                    else:
                        response = execute_response.get('response')
        return status,response