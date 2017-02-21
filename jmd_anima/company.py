# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdcompany(models.Model):
    _inherit = "res.company"
    rfc = fields.Char("RFC")
    cuenta_facutra = fields.Many2one("account.account",
        string="Cuenta Facturas")
    diario_factura = fields.Many2one("account.journal",
        string="Diario Facturas")
    cuenta_pagos = fields.Many2one("account.account",
        string="Cuenta Pagos")
    cta_ivap = fields.Many2one("account.account",
        string="Cta. IVA Pdte.")
    cta_rivap = fields.Many2one("account.account",
        string="Cta. Ret. IVA Pdte.")
    cta_risrp = fields.Many2one("account.account",
        string="Cta. Ret. ISR Pdte.")
    cta_iva = fields.Many2one("account.account",
        string="Cta. IVA Pagado")
    cta_risr = fields.Many2one("account.account",
        string="Cta. Ret. ISR Pagado")
    cta_riva = fields.Many2one("account.account",
        string="Cta. Ret. IVA Pagado")