# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdrechazadas(models.Model):
    _inherit = "mail.thread"
    _name = "ae.rechazadas"
    name = fields.Char("Nombre")
    rfc = fields.Char("RFC")
    monto = fields.Float("Monto")
    motivo = fields.Char("Motivo")
    descripcion = fields.Text("Descripción")