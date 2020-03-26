# -*- coding: utf-8 -*-
{
    'name': "Skit project",

    'summary': """
        Project
        """,

    'description': """
       Project
    """,

    'author': "Srikesh Infotech",
    'website': "http://www.srikeshinfotech.com",
    'category': 'Project',
    'version': '0.1',
    'depends': ['product', 'sale', 'base', 'project', 'stock',
                'web_kanban_graph'],
    'data': [
        'views/soil_aggregate.xml',
        'views/soil_compaction.xml',
        'views/sieve_analysis.xml',
        'views/config_sieve_analysis.xml',
        'views/soil_consistency.xml',
        'views/soil_abrasion.xml',
        'views/soil_penetration.xml',
        'views/config_soil_abrasion.xml',
        'views/config_branch.xml',
        'views/config_kind_of_material.xml',
        'views/template.xml',
        'views/config_spec_item.xml',
        'security/ir.model.access.csv',
        'report/sieve_analysis_report.xml',
        'report/sieve_analysis_template.xml',
        'report/soil_compaction_report.xml',
        'report/soil_compaction_template.xml',
        'report/soil_consistency_report.xml',
        'report/soil_consistency_template.xml',
        'report/soil_penetration_report.xml',
        'report/soil_penetration_template.xml',
        'report/soil_abrasion_report.xml',
        'report/soil_abrasion_template.xml',
        'report/soil_aggregate_report.xml',
        'report/soil_aggregate_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
