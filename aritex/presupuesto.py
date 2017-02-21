# -*- coding: utf-8 -*-
from openerp import models, fields, api


class jmdaccount(models.Model):
    _inherit = "ae.presupuesto.linea"

    linea = fields.Many2one("ae.presupuesto.template",
        string="Centro de Costos")


class jmdpresupuesto(models.Model):
    _inherit = "ae.presupuesto"

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
                    'linea': i.id,
                    'clave': i.clave,
                    'categoria': i.categoria.id,
                    'monto': i.monto,
                    'presupuesto': record.id,
                    })
        return True

    @api.multi
    def calcula(self):
        for i in self.linea:
            orden = 0
            facturado = 0
            pagado = 0
            print("Entro al Método")
            for j in self.env["purchase.order.line"].search([('proyecto_id',
                '=', self.proyecto.id), ('centro_costos', '=', i.linea.id)]):
                print("Entrando")
                #Encontrando a que columna pertenece
                if not j.order_id.invoiced:
                    print("orden")
                    print(j.price_subtotal)
                    orden += j.price_subtotal
                elif j.order_id.state not in ["done"] and j.order_id.invoiced:
                    print("facturado")
                    facturado += j.price_subtotal
                elif j.order_id.state in ["done"]:
                    print("pagado")
                    pagado += j.price_subtotal
            i.oc = orden
            print("Orden " +  str(orden))
            i.facturado = facturado
            print("Facturado " +  str(facturado))
            i.pagado = pagado
            print("Pagado " +  str(pagado))
            i.write({'oc': orden,
                'facturado': facturado,
                'pagado': pagado})

        return True