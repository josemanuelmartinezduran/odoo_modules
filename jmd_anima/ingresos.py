# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdingresos(models.Model):
    _name = "ae.ingresos"

    name = fields.Char("Descripción")
    ventana = fields.Many2one("ae.ventana", "Ventana")
    territorio = fields.Many2one("ae.territorio", "Territorio")
    inicio = fields.Date("Inicio")
    fin = fields.Date("Fin")
    monto = fields.Float("Monto")
    proyecto = fields.Many2one("ae.proyecto", "Proyecto")
