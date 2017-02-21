# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdventa(models.Model):
    _name = "ae.venta"
    _inherit = "mail.thread"

    def create_move(self, cr, uid, ids, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.poliza_generada:
                return ret
            #creando la poliza
            #print("Por crear la poliza")
            #poliza_obj = self.pool.get("account.move")
            #idpoliza = poliza_obj.create(cr, uid, {
            #        'name': i.concepto_poliza,
            #        'journal_id': i.diario.id,
            #    }, context)
            #print("Poliza Creada")
            #linea_obj = self.pool.get("account.move.line")
            #linea_obj.create(cr, uid, {
            #        'name': i.concepto_poliza,
            #        'account_id': i.cuenta_cargo.id,
            #        'debit': i.monto,
            #        'move_id': idpoliza,
            #    }, context)
            #print("Poliza de Cargo Creada")
            #linea_obj.create(cr, uid, {
            #        'name': i.concepto_poliza,
            #        'account_id': i.cuenta_abono.id,
            #        'credit': i.monto,
            #        'move_id': idpoliza,
            #    }, context)
            #self.write(cr, uid, [i.id], {
            #    'poliza_generada': "Si"
            #    })
        return ret

    def create_invoice(self, cr, uid, ids, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.factura:
                return ret
            invoice_obj = self.pool.get("account.invoice")
            idfactura = invoice_obj.create(cr, uid, {
                    'name': i.concepto_factura,
                    'partner_id': i.coproductor.id,
                    'account_id': i.cuenta_factura.id,
                })
            self.write(cr, uid, [i.id], {
                    'factura': idfactura
                })
        return ret

    name = fields.Char("Nombre")
    ventana = fields.Many2one("ae.ventana", "Ventana")
    territorio = fields.Many2one("ae.territorio", "Territorio")
    inicio = fields.Date("Inicio")
    fin = fields.Date("Fin")
    monto = fields.Float("Monto")
    tipo = fields.Selection([('capital', 'Capital'), ('especie', 'Especie')],
        "Tipo de contribución")
    proyecto = fields.Many2one("ae.proyecto", "Proyecto")
    coproductor = fields.Many2one("res.partner", string="Cliente")
    cuenta_cargo = fields.Many2one("account.account", string="Cuenta de Cargo")
    cuenta_abono = fields.Many2one("account.account", string="Cuenta Abono")
    concepto_poliza = fields.Char("Concepto de la Póliza")
    poliza_generada = fields.Char("Poliza Generada")
    diario = fields.Many2one("account.journal", string="Diario")
    factura = fields.One2many("account.invoice", "venta_id", string="Factura")
    concepto_factura = fields.Char("Concepto de la Factura")
    cuenta_factura = fields.Many2one("account.account", string="Cuenta de la\
        Factura")


class jmdaccount(models.Model):
    _inherit = "account.invoice"
    venta_id = fields.Many2one("ae.venta", string="Venta")


class jmdventana(models.Model):
    _name = "ae.ventana"
    name = fields.Char("Nombre")


class jmdterritorio(models.Model):
    _name = "ae.territorio"
    name = fields.Char("Nombre")