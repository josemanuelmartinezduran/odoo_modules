# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdinvoice(models.Model):
    _inherit = "account.invoice"
    aprobado = fields.Boolean("Aprobado")
    iva = fields.Float("IVA")
    retisr = fields.Float("Retención ISR")
    retiva = fields.Float("Retención IVA")
    total = fields.Float("Total")
    poraprobar = fields.Boolean("Por aprobar")
    caja = fields.Boolean("Caja Chica")