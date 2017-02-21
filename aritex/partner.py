# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdpartner(models.Model):
    _inherit = "res.partner"
    forma_pago = fields.Char("Forma de Pago")
    credito = fields.Char("Credito")
    contacto = fields.Char("Nombre del Contacto")
    rfc = fields.Char("RFC")