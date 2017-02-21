# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdcentro(models.Model):
    _inherit = "mail.thread"
    _name = "ae.centro_costos"
    name = fields.Char("Nombre")
    description = fields.Char("Descripción")
    clave = fields.Char("Clave")