# -*- coding: utf-8 -*-

import logging
from odoo import http
from odoo.http import request
from datetime import datetime
_logger = logging.getLogger(__name__)


class Office365Main(http.Controller):

	@http.route('/dsp_demo_code/',type='http',auth='user')
	def dsp_demo_code(self, *args,**kwargs):
		cloud_connection = request.env['office365.instance']
		try:
			response = cloud_connection.search([('active','=',True)],limit =1)
			_logger.info("======================================query_string%r",kwargs)
			if response:
				get  = cloud_connection._create_office365_flow(response.id, *args, **kwargs)
			action_id = request.env.ref('dsp_demo_code.office365_connection_mapping').id
			url = "/web#id={}&action={}&model=office365.instance&view_type=form".format(response.id,action_id)
			return http.local_redirect(url)
		except Exception as e:
			_logger.error("=========Error Found While Generating Access Token==================================%r",str(e))
	

	@http.route('/dsp_demo_code/fetch_instace_id',type='json',auth='user')
	def fetch_instace_id(self,*args, **kwargs):
		instance_id = request.session.get('instance_id',False)
		instance_env = request.env['office365.instance']
		if not instance_id:
			connection = instance_env.search([('active','=',True)],limit=1)
			request.session['instance_id'] = connection.id
			instance_id = connection.id
		current_date = datetime.now().strftime("%d %b %Y")
		return {'instance_id':instance_id,'current_date':current_date}
	
	@http.route('/dsp_demo_code/change_instance_id',type='json',auth='user')
	def change_instance_id(self,instance_id=1):
		request.session['instance_id'] = int(instance_id)
		return {'instance_id':int(instance_id)}
	

	@http.route('/dsp_demo_code/fetch_instace_details',type='json',auth='user')
	def fetch_instace_details(self,*args, **kwargs):
		selection_instance = {}
		connection = request.env['office365.instance'].search([('active','=',True)])
		for instance in connection:
			selection_instance[instance.id] = instance.name
		return selection_instance
	

	@http.route('/dsp_demo_code/fetch_instance_extra_details',type='json',auth='user')
	def fetch_instance_extra_details(self,instance_id = False,*args, **kwargs):
		data = {}
		models = {'contact':'office365.contact.mapping','task':'office365.task.mapping',
		'calendar':'office365.calendar.mapping',
		'project':'office365.project.mapping'}
		for key,value in models.items():
			html = ''
			count = request.env[value].search_count([('instance_id','=',instance_id)])
			data[key] = {
				'count':count,
			}
			html = self.get_graph_html(instance_id, count, value,html,'#972C8C')
			html = self.get_graph_html(instance_id, count, value,html,'#3BCE99','import')
			data[key]['html'] = html
		return data
	
	def get_graph_html(self,instance_id, count, model,html,color, operation='export'):
		if not count:
			percentage = 0
		else:
			count_operation = request.env[model].search_count([('created_by','=',operation)])
			percentage = int((count_operation*100)/count)
		html+= '''
			<span style="background-color: {};flex: 0 0 {}%;height:10px;"></span>
		'''.format(color,percentage)
		return html
	
	@http.route('/dsp_demo_code/get_synchronisation_id', type ='json', auth='user')
	def get_synchronisation_id(self, action='export', instance=1, *args, **kwargs):
		bulk_synchronization = request.env['office365.bulk.synchronisation']
		vals = {
				'action':action,
				'instance_id':int(instance)
			}
		sync = bulk_synchronization.create(vals)
		return {'id':sync.id}
	
	# @http.route('/dsp_demo_code/fetch_sales_doughnut_data',type='json',auth='user')
	# def fetch_sales_doughnut_data(self, instance_id=1):
	# 	color = {
	# 	'draft':'#45F18A',
	# 	'sale':'#007AFF',
	# 	'done':'#5E2160'
	# 	}
	# 	select_sql_clause = """SELECT count(state) as total_state,
	# 	state 
	# 	FROM sale_order where id in 
	# 	(select name from office365_order where instance_id=%d)
	# 	AND state in ('draft','sale','done')
	# 	group by state"""%instance_id
	# 	request.env.cr.execute(select_sql_clause)
	# 	query_results = request.env.cr.dictfetchall()
	# 	data = {'sale_data':{},'sale_statuses':[],'color':[]}
	# 	sale_data = {result['state'].strip():result['total_state'] for result in query_results}
	# 	for check in color:
	# 		data['sale_data'][check] = sale_data.get(check,0)
	# 		data['color'].append(color[check])
	# 		data['sale_statuses'].append(check.capitalize())
	# 	return data
	
	# @http.route('/dsp_demo_code/fetch_purchase_doughnut_data',type='json',auth='user')
	# def fetch_purchase_doughnut_data(self, instance_id=1):
	# 	color = {
	# 	'draft':'#45F18A',
	# 	'purchase':'#007AFF',
	# 	'done':'#5E2160'
	# 	}
	# 	select_sql_clause = """SELECT count(state) as total_state,
	# 	state 
	# 	FROM purchase_order where id in 
	# 	(select name from office365_purchase_order where instance_id=%d)
	# 	AND state in ('draft','purchase','done')
	# 	group by state"""%instance_id
	# 	request.env.cr.execute(select_sql_clause)
	# 	query_results = request.env.cr.dictfetchall()
	# 	data = {'purchase_data':{},'purchase_statuses':[],'color':[]}
	# 	purchase_data = {result['state'].strip():result['total_state'] for result in query_results}
	# 	for check in color:
	# 		data['purchase_data'][check] = purchase_data.get(check,0)
	# 		data['color'].append(color[check])
	# 		data['purchase_statuses'].append(check.capitalize())
	# 	return data

	@http.route('/dsp_demo_code/get_dashboard_line_data',type = 'json', auth = 'user')
	def get_dashboard_line_data(self,instance_id = 1,month=False,contact=True,calendar=True):
		labels = [
				'Mon', 'Tue',
				'Wed', 'Thu', 'Fri',
				'Sat', 'Sun'
			]
		if month:
			query_contact = """
			select to_char(create_date, 'Dy') AS "day",count(*) as total_count
			FROM office365_contact_mapping WHERE to_char(create_date,'Mon') ='%s' AND instance_id = %d
			GROUP BY to_char(create_date, 'Dy')
			"""%(month,instance_id)
			query_calendar = """
			select to_char(create_date, 'Dy') AS "day",count(id) as total_count
			FROM office365_calendar_mapping WHERE to_char(create_date,'Mon') ='%s' AND instance_id = %d
			GROUP BY to_char(create_date, 'Dy')
			"""%(month,instance_id)
		else:
			query_contact = """
			select to_char(create_date, 'Dy') AS "day",count(*) as total_count
			FROM office365_contact_mapping WHERE instance_id = %d
			GROUP BY to_char(create_date, 'Dy')
			"""%instance_id
			query_calendar = """
			select to_char(create_date, 'Dy') AS "day",count(*) as total_count
			FROM office365_calendar_mapping WHERE instance_id = %d
			GROUP BY to_char(create_date, 'Dy')
			"""%instance_id
		data = {'labels':labels,
		'datasets':[]}
		if contact:
			contact_vals = {
                    'label': "Contact",
                    'fill': False,
                    'lineTension': 1,
                    'backgroundColor': "#FFB661",
                    'borderColor': "#5E2160", 
                    'borderCapStyle': False,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'borderJoinStyle': 'miter',
                    'pointBorderColor': "#5E2160",
                    'pointBackgroundColor': "white",
                    'pointBorderWidth': 1,
                    'pointHoverRadius': 8,
                    'pointHoverBackgroundColor': "#5E2160",
                    'pointHoverBorderColor': "#FFB661",
                    'pointHoverBorderWidth': 2,
                    'pointRadius': 4,
                    'pointHitRadius': 10,
                    'data': [],
                    'spanGaps': True,
                  }
			request._cr.execute(query_contact)
			contact_data = {data['day'].strip():data['total_count'] for data in request._cr.dictfetchall()}
			for label in labels:
				contact_vals['data'].append(int(contact_data.get(label,0)))
			data['datasets'].append(contact_vals)
		if calendar:
			calendar_vals = {
                    'label': "Calendar",
                    'fill': False,
                    'lineTension': 1,
                    'backgroundColor': "#201CD9",
                    'borderColor': "#2492E1", 
                    'borderCapStyle': False,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'borderJoinStyle': 'miter',
                    'pointBorderColor': "#201CD9",
                    'pointBackgroundColor': "white",
                    'pointBorderWidth': 1,
                    'pointHoverRadius': 8,
                    'pointHoverBackgroundColor': "#201CD9",
                    'pointHoverBorderColor': "#2492E1",
                    'pointHoverBorderWidth': 2,
                    'pointRadius': 4,
                    'pointHitRadius': 10,
                    'data': [],
                    'spanGaps': True,
                  }
			request._cr.execute(query_calendar)
			calendar_data = {data['day'].strip():data['total_count'] for data in request._cr.dictfetchall()}
			for label in labels:
				calendar_vals['data'].append(int(calendar_data.get(label,0)))
			data['datasets'].append(calendar_vals)
		# _logger.info("============contact_vals===================%r",contact_data)
		return {
			'data':data
		}