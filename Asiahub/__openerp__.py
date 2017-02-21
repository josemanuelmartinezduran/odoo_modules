# -*- coding: utf-8
{
    "name": "Assiahub Custom",
    "version": "1.0",
    "author": "Jose M Martz",
    "category": "Customization",
    "description": """
    Custom MELI items
    """,
    "website": "",
    "license": "AGPL-3",
    "depends": [
         'base',
         'meli_oerp-master',
    ],
    "demo": [
    ],
    "data": [
        'security/groups.xml',
        'view/meli_view.xml',
        'view/question_view.xml',
        'view/ship_view.xml',
        'view/company_view.xml',
        'view/asiahub_css.xml',
    ],
    'css': [
        ],
    'test': [],
    "installable": True,
    "active": False,
}