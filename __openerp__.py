# -*- coding: utf-8 -*-
{
    'name': "人事绩效",

    'summary': """
         hr performance system""",

    'description': """
        hr performance system
    """,

    'author': "SPDB",
    'website': "http://www.spdb.com.cn",
    'category': 'Uncategorized',
    'version': '0.1',
	'sequence': 122,		    
    # any module necessary for this one to work correctly
    'depends': ['hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_performance_ui_view_view.xml',
        'views/hr_performance_views.xml',
        'views/hr_performancefields_views.xml',
        'report/hr_performance_report_views.xml',
        'wizard/hr_performance_bonuscalculation_compute_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/hr_performance.xml',
    ],
    'installable': True,
    'application': True,
}