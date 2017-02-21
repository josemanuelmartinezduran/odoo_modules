# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class jmdaccount(models.Model):
    _inherit = "ae.proyecto"
    mex = fields.Char("MEX", size=6)

    @api.one
    @api.constrains('mex')
    def check_lenght(self):
        if len(self.mex) < 6:
            raise ValidationError("MEX debe ser de 6 caracteres")