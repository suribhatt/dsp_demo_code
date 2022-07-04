from .model import Model

class HallAvailable(Model):
    
    def get_hall_available(self,vals):
        status = False
        response = ''
        session_key = vals.get('session_key',False)
        if not session_key:
            response = 'Session key is Required'
        else:
            if not self.validate_session_key(session_key):
                response = 'Session key is not valid'
            else:
                capacity = vals.get('capacity',False)
                time_start = vals.get('time_start',False)
                if not capacity or not time_start:
                    response = 'capacity, time_start are required fetch available hall, please check the api request'
                else:
                    query = """select id_hall,name from hall
                    where  capacity>=%i and id_hall NOT IN(select id_hall from hall_available
                    where time_start <='%s' and time_end >='%s') order by capacity limit 1"""%(capacity,time_start,time_start)
                    execute_response = self.executeS(query)
                    if execute_response.get('status'):
                        status = True
                        actual_response = execute_response.get('response')
                        if actual_response and actual_response[0]:
                            response = {
                                'id_hall':actual_response[0][0],
                                'hall_name':actual_response[0][1]
                            }
                        else:
                            response = 'No Hall Is Available For Given Capacity'
                    else:
                        response = execute_response.get('response')
        return status,response

    def get_hall_data(self,vals):
        status = False
        response = ''
        session_key = vals.get('session_key',False)
        if not session_key:
            response = 'Session key is Required'
        else:
            if not self.validate_session_key(session_key):
                response = 'Session key is not valid'
            else:
                time_start = vals.get('time_start',False)
                time_end = vals.get('time_end',False)
                if not time_start or not time_end:
                    response = 'time_start, time_end are required fetch available hall, please check the api request'
                else:
                    query = """select id_hall_available,id_hall,id_professor,time_start,time_end, state from hall_available where
                    (time_start BETWEEN '%s' AND '%s')"""%(time_start,time_end)
                    execute_response = self.executeS(query)
                    if execute_response.get('status'):
                        status = True
                        actual_response = execute_response.get('response')
                        if actual_response and actual_response[0]:
                            response = []
                            for rs in actual_response:
                                response.append({
                                    'id_hall_available':rs[0],
                                    'id_hall':rs[1],
                                    'id_professor':rs[2],
                                    'time_start':rs[3],
                                    'time_end':rs[4],
                                    'state':rs[5]
                                })
                        else:
                            'No Hall Is Available For Given Time Frame'
                    else:
                        response = execute_response.get('response')
        return status,response
    

    def update_hall_available(self,vals):
        status = False
        response = ''
        session_key = vals.get('session_key',False)
        if not session_key:
            response = 'Session key is Required'
        else:
            if not self.validate_session_key(session_key):
                response = 'Session key is not valid'
            else:
                id_hall_available = vals.get('id_hall_available',False)
                state = vals.get('state',0)
                if not id_hall_available:
                    response = 'id_hall_available are required update available hall, please check the api request'
                else:
                    query = """UPDATE hall_available 
                        SET state = %i
                        WHERE id_hall_available = %i"""%(int(state), int(id_hall_available))
                    execute_response = self.execute(query)
                    if execute_response.get('status'):
                        status = True
                        response = 'Hall Available State Has Updated'
                    else:
                        response = execute_response.get('response')
        return status,response
    
    def add_hall_available(self, vals):
        status = False
        response = ''
        session_key = vals.get('session_key',False)
        if not session_key:
            response = 'Session key is Required'
        else:
            if not self.validate_session_key(session_key):
                response = 'Session key is not valid'
            else:
                id_hall = vals.get('id_hall',False)
                id_professor = vals.get('id_professor',False)
                time_start = vals.get('time_start',False)
                time_end = vals.get('time_end',False)
                if not id_hall or not id_professor or not time_start or not time_end:
                    response = 'id_hall,id_professor,time_start,time_end are required to book hall,please check the api request'
                else:
                    query = "INSERT INTO hall_available (id_hall, id_professor,time_start,time_end,state) VALUES (%i, %i,'%s','%s',1)"%(int(id_hall), int(id_professor), time_start, time_end)
                    execute_response = self.execute(query)
                    if execute_response.get('status'):
                        get_last_id = self.get_last_id('hall_available')
                        status = get_last_id.get('status')
                        if status:
                            response = {'id_hall_available':get_last_id['response'][0][0]}
                    else:
                        response = execute_response.get('response')
        return status,response