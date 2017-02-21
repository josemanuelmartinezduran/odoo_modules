# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _name = "ae.eficine"
    _inherit = "mail.thread"

    def create_move(self, cr, uid, ids, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.poliza_generada:
                return ret
            #creando la poliza
            print("Por crear la poliza")
            poliza_obj = self.pool.get("account.move")
            idpoliza = poliza_obj.create(cr, uid, {
                    'name': i.concepto_poliza,
                    'journal_id': i.diario.id,
                }, context)
            print("Poliza Creada")
            linea_obj = self.pool.get("account.move.line")
            linea_obj.create(cr, uid, {
                    'name': i.concepto_poliza,
                    'account_id': i.cuenta_cargo.id,
                    'debit': i.monto,
                    'move_id': idpoliza,
                }, context)
            print("Poliza de Cargo Creada")
            linea_obj.create(cr, uid, {
                    'name': i.concepto_poliza,
                    'account_id': i.cuenta_abono.id,
                    'credit': i.monto,
                    'move_id': idpoliza,
                }, context)
            self.write(cr, uid, [i.id], {
                'poliza_generada': "Si"
                })
        return ret

    def create_invoice(self, cr, uid, ids, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.factura:
                return ret
            invoice_obj = self.pool.get("account.invoice")
            idfactura = invoice_obj.create(cr, uid, {
                    'name': i.concepto_factura,
                    'partner_id': i.socio.id,
                    'account_id': i.cuenta_factura.id,
                })
            invoiceline_obj = self.pool.get("account.invoice.line")
            invoiceline_obj.create(cr, uid, {
                    'name': i.concepto_factura,
                    'product_id': i.producto_factura.id,
                    'description': i.producto_factura.description,
                    'price_unit': i.monto,
                    'invoice_id': idfactura,
                })
            self.write(cr, uid, [i.id], {
                    'factura': idfactura
                })
        return ret

    name = fields.Char("Nombre")
    monto = fields.Float("Monto")
    socio = fields.Many2one("res.partner", "Socio")
    proyecto = fields.Many2one("ae.proyecto", "Proyecto")
    aprobacion = fields.Date("Fecha de Aprobación")
    documento = fields.Binary("Documento")
    nombre_documento = fields.Char("Nombre Documento")
    cuenta_cargo = fields.Many2one("account.account", string="Cuenta de Cargo")
    cuenta_abono = fields.Many2one("account.account", string="Cuenta Abono")
    concepto_poliza = fields.Char("Concepto de la Póliza")
    poliza_generada = fields.Char("Poliza Generada")
    diario = fields.Many2one("account.journal", string="Diario")
    tipo = fields.Many2one("ae.estimulo", string="Tipo de Estímulo")
    factura = fields.Many2one("account.invoice", string="Factura")
    concepto_factura = fields.Char("Concepto de la Factura")
    cuenta_factura = fields.Many2one("account.account", string="Cuenta de la\
        Factura")
    producto_factura = fields.Many2one("product.product", string="Producto de\
        la Factura")

    class jmdestimulo(models.Model):
        _name = "ae.estimulo"
        name = fields.Char("Nombre")