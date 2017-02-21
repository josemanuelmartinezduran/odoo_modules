# -*- coding: utf-8 -*-
{
    "name": "SOFOM",
    "version": "1.0",
    "author": "Jose M Martz",
    "category": "Account",
    "description": """
    Sistema de crédito y cobranza
    """,
    "website": "http://hackeando.net",
    "license": "AGPL-3",
    "depends": [
         'product',
         'crm',
         'base_geolocalize',
         'account',
    ],
    "demo": [
    ],
    "data": [
        "sequence/solicitud_sequence.xml",
        "sequence/cotizacion_sequence.xml",
        "sequence/lead_sequence.xml",
        "sequence/pago_sequence.xml",
        "sequence/partner_sequence.xml",
        "view/colonia_view.xml",
        "view/producto_view.xml",
        "view/partner_view.xml",
        "view/lead_view.xml",
        "view/cotizador_view.xml",
        "view/solicitud_view.xml",
        "view/spari_view.xml",
        "view/tasa_view.xml",
        "view/plazo_view.xml",
        "view/credito_view.xml",
        "view/destino_view.xml",
        "view/abono_view.xml",
        "view/maps_view.xml",
        "view/mappayment_view.xml",
        "workflow/credito_workflow.xml",
        "report/cotizacion_report.xml",
        "report/solicitud_report.xml",
        "report/dictamen_report.xml",
        "report/contrato_report.xml",
        "report/caratula_report.xml",
        "report/resumen_report.xml",
        "report/comprobante_report.xml",
        "report/estadocuenta_report.xml",
        "report/anexoa_report.xml",
        "report/anexob_report.xml",
        "report/anexoc_report.xml",
        "report/anexod_report.xml",
        "report/anexoe_report.xml",
        "report/oxxo_report.xml",
    ],
    'css': [],
    'test': [],
    "installable": True,
    "active": False,
}