# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _inherit = "res.currency.rate"
    tipo_cambio = fields.Float("Tipo de Cambio", digits=(10, 4))

    def calcula_tipo(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            if i.tipo_cambio > 0:
                cambio = 1 / i.tipo_cambio
                self.write(cr, uid, [i.id], {'rate': cambio})


class jmdcurrency(models.Model):
    _inherit = "res.currency"
    divisa_referencia = fields.Many2one("res.currency",
        string="Divisa de Referencia")
    factor = fields.Float("Factor", digits=(10, 4))
    mes = fields.Char("Mes")
    year = fields.Char("Año")

    def inserta_tabla(self, cr, uid, ids, context=None):
        rate_obj = self.pool.get("res.currency.rate")
        for i in self.browse(cr, uid, ids, context):
            for j in i.divisa_referencia.rate_ids:
                fecha = j.name
                mes = fecha[5:7]
                year = fecha[0:4]
                if mes == i.mes and year == i.year:
                    tipo_cambio = j.tipo_cambio * i.factor
                    if tipo_cambio == 0:
                        continue
                    rate = 1 / tipo_cambio
                    rate_obj.create(cr, uid, {
                        'name': fecha,
                        'rate': rate,
                        'tipo_cambio': tipo_cambio,
                        'currency_id': i.id,
                        })