# -*- coding: utf-8 -*-
{
  "name"                 :  "DSP Demo Code",
  "summary"              :  """Bi-directional synchronization of calenders,contacts,tasks,projects with Office365""",
  "category"             :  "cloud",
  "version"              :  "1.1.2",
  "sequence"             :  1,
  "author"               :  "DSP Software Pvt. Ltd.",
  "description"          :  """DSP Demo Code
==============================
This module only shows the demo of the code, It might not install on your server as it require our support
 """,
  "depends"              :  ['crm',
  'project'],
  "data"                 :  [
    'security/office365_security.xml',
    'security/ir.model.access.csv',
    'views/office/instance.xml',
    'views/mapping/contact_mapping.xml',
    'views/mapping/calendar_mapping.xml',
    'views/mapping/task_mapping.xml',
    'views/mapping/project_mapping.xml',
    'views/office/dashboard.xml',
    'views/office/office365_synchronization.xml',
    'views/office/menu.xml',
    'wizard/office365_message.xml',
    'wizard/office365_bulk_synchronization.xml',
    'wizard/office365_manual_synchronization.xml',
    'data/cron.xml',
    'data/server.xml'],
  'qweb':[
		'static/src/xml/office365_dashboard.xml'
	],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "external_dependencies":  {'python': ['requests']},
}
