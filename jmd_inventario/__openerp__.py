# -*- coding: utf-8 -*-
{
    'name': 'Personalización de Inventarios',
    'version': '1.0',
    'author': 'José M Martinez',
    'description': "Control de Inventario",
    'summary': '',
    'category': '',
    'website': 'http://hackeando.net',
    'depends': [
        'base',
        'stock',
    ],
    'data': [
        'view/asset_view.xml',
        'view/resguardo_view.xml',
        'view/acta_view.xml',
        'sequence/product_sequence.xml',
        'report/resguardo_report.xml',
        'report/activo_report.xml',
        'report/acta_inicio.xml',
        'report/acta_fin.xml',
        'report/acta_bajas.xml',
    ],
    'js': [
    ],
    'css': [
    ],
    'qweb': [
    ],
    'init_xml': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}