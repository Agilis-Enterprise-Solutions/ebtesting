# -*- coding: utf-8 -*-
{
    'name': "Skit Soil Drilling",

    'summary': """
        Soil Drilling
        """,

    'description': """
       Soil Drilling
    """,

    'author': "Srikesh Infotech",
    'website': "http://www.srikeshinfotech.com",
    'category': 'Project',
    'version': '0.1',
    'depends': ['product', 'sale', 'base', 'project','skit_test_template','skit_project'],
    'data': [
        "security/ir.model.access.csv",
        'views/product.xml',
        'views/sale.xml',
        'views/ir_sequence.xml',
        'wizard/skit_project_wizard.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
