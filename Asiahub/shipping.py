# -*- coding: utf-8 -*-
from openerp import models, fields


class jmd_ship(models.Model):
    _inherit = "mail.thread"
    _name = "mercadolibre.ship"
    name = fields.Char("Id")
    shipment_type = fields.Char("Shipment Type")
    status = fields.Char("Status")
    date_created = fields.Char("Date Created")
    address_line = fields.Char("Address Line")
    zip_code = fields.Char("Zip Code")
    city = fields.Char("City")
    state = fields.Char("State")
    country = fields.Char("Country")
    order_id = fields.Many2one("mercadolibre_orders", string="Order")
    product = fields.Char("Product")


class jmd_orders(models.Model):
    _inherit = "mercadolibre.orders"
    ship_ids = fields.One2many("mercadolibre.ship", "order_id",
        string="Shippings")