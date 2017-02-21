# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _name = "ae.proyecto"
    _inherit = "mail.thread"

    name = fields.Char("Nombre del Proyecto")
    productor = fields.Char("Productor")
    director = fields.Char("Director")
    lproductor = fields.Char("Productor de Linea")
    cop = fields.Html("Coproductores")
    distribuidor = fields.Char("Distribuidor")
    aventas = fields.Char("Agente de Ventas")
    eficine = fields.One2many("ae.eficine", "proyecto", string="Eficine")
    presupuesto = fields.One2many("ae.presupuesto", "proyecto",
        string="Proyecto")
    venta = fields.One2many("ae.venta", "proyecto", string="Venta")
    inicio = fields.Date("Fecha de inicio")
    fin = fields.Date("Fecha final")
    estreno = fields.Date("Fecha de estreno")
    ingreso = fields.One2many("ae.ingresos", "proyecto", string="Ingresos")
    cuenta = fields.Char("Clave de a cuenta")