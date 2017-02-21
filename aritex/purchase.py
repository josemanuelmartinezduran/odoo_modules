# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime


class jmdaccount(models.Model):
    _inherit = "purchase.order.line"

    @api.one
    def get_total(self):
        self.total = self.price_unit * self.product_qty

    @api.onchange("product_id")
    def onchange_product(self):
        self.name = self.product_id.description
        self.date_planned = datetime.date.today().strftime('%Y-%m-%d'),

    proyecto_id = fields.Many2one("ae.proyecto", string="Proyecto")
    centro_costos = fields.Many2one("ae.presupuesto.template",
        string="Centro de Costos")
    comentario = fields.Char("Comentario")
    plazo = fields.Date("Plazo de Entrega")
    descripcion = fields.Text("Descipción", related="product_id.description")
    total = fields.Float("Total", compute=get_total)


class jmdaccount(models.Model):
    _inherit = "purchase.order"
    comprador = fields.Many2one("hr.employee", string="Comprador")
    solicitud = fields.Many2one("hr.employee", string="Solicitud")
    forma = fields.Char("Forma de Pago", related="partner_id.forma_pago")
    credito = fields.Char("Crédito", related="partner_id.credito")
    descuento = fields.Char("Descuento")
    entrega = fields.Date("Fecha de Entrega")