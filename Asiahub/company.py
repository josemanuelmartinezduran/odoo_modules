# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdcompany(models.Model):
    _inherit = "res.company"
    cnova_client_id = fields.Char("Client Id")
    cnova_accesstoken = fields.Char("Access Token")
    cnova_url = fields.Char("Url")
    cbt_username = fields.Char("CBT Username")
    cbt_passwd = fields.Char("CBT Passwd")
    cbt_accesstoken = fields.Char("CBT Access Token")