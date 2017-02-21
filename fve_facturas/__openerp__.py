# -*- coding: utf-8 -*-

{
    'name': 'Anima Estudios',
    'version': '1.0',
    'author': 'Francisco Villegas & José M Martinez',
    'description': "Get SAT invoice",
    'summary': 'Gets SAT (Mexico) inovice from given email account',
    'category': 'account',
    'website': 'http://www.pandix.com.mx & http://hackeando.net',
    'depends': [
        'jmd_anima',
        'project'
    ],
    'data': [
        'security/factuas_security.xml',
        'view/mail.xml',
        'view/pago_view.xml',
        'view/rechazadas_view.xml',
        'view/invoice_view.xml',
        'view/menu.xml',
        'view/voucher_view.xml',
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
