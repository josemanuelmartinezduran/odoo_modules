# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdprediction(models.Model):
    _name = "ae.prediccion"
    _inherit = "mail.thread"

    def _compute_total(self):
        for record in self:
            record.total = 0
            for i in record.linea:
                record.total = record.total + i.monto
        return True

    def cargar_conceptos(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context):
            print("Inicio")
            obj_template = self.pool.get("ae.presupuesto.template")
            obj_linea = self.pool.get("ae.presupuesto.linea")
            print("Segundo")
            for i in obj_template.browse(cr, uid, obj_template.search(cr, uid,
                [('name', 'ilike', '')])):
                print("Aqui")
                obj_linea.create(cr, uid, {
                    'name': i.name,
                    'categoria': i.categoria.id,
                    'monto': i.monto,
                    'presupuesto': record.id,
                    })
        return True

    name = fields.Char("Nombre")
    proyecto = fields.Many2one("ae.proyecto", "Proyecto")
    total = fields.Float(compute='_compute_total', string="Total")
    state = fields.Selection([('nuevo', 'Nuevo'), ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado')], string="Estado")
    linea = fields.One2many("ae.prediccion.linea", "presupuesto")


class jmdbudgetline(models.Model):
    _name = "ae.prediccion.linea"

    name = fields.Char("Nombre")
    categoria = fields.Many2one("ae.presupuesto.categoria", "Categoría")
    monto = fields.Float("Monto")
    presupuesto = fields.Many2one("ae.prediccion", "Relacion")
    mes = fields.Selection([('1', "Enero"), ('2', "Febrero"), ('3', "Marzo"),
        ('4', "Abril"), ('5', "Mayo"), ('6', "Junio"), ('7', "Julio"),
        ('8', "Agosto"), ('9', "Septiembre"), ('10', "Octubre"),
        ('11', "Noviembre"), ('12', "Diciembre")])
    year = fields.Integer("Año")
    divisa = fields.Char("Divisa")
