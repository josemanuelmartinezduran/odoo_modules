# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _inherit = "account.account"

    balanza_comprobacion = fields.Boolean(string="Balanza General")
    estado_resultados = fields.Boolean(string="Estado de Resultados")
    balance_general = fields.Boolean(string="Balance General", default=True)
    tipo_cuenta = fields.Selection([('acredora', 'Acreedora'),
        ('deudora', 'Deudora')], string="Tipo de Cuenta")
    codigo_agrupador = fields.Char("Codigo Agrupador SAT")