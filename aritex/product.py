# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _inherit = "product.product"
    categoria = fields.Many2one("ae.presupuesto.linea",
        string="Categoría del Presupuesto")
    proyecto = fields.Many2one("ae.presupuesto", string="Presupuesto")