# -*- coding: utf-8 -*-
{
    'name': "Magestore training module",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Magestore",
    'website': "http://www.magestore.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
        'hr'
    ],

    # always loaded
    'data': [
        'module/module_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/Task.xml',
        # 'views/mission.xml',
        'views/course.xml',
        'views/trainee.xml',
        'views/contract.xml',
        'views/mentor.xml',
        'views/review.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
