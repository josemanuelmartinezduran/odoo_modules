# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdpagos(models.Model):
    _name = "ae.cpago"
    _inherit = "mail.thread"
    name = fields.Char("Descripción")
    mes = fields.Selection([('1', "Enero"), ('2', "Febrero"), ('3', "Marzo"),
        ('4', "Abril"), ('5', "Mayo"), ('6', "Junio"), ('7', "Julio"),
        ('8', "Agosto"), ('9', "Septiembre"), ('10', "Octubre"),
        ('11', "Noviembre"), ('12', "Diciembre")])
    year = fields.Char("Año")
    proyecto = fields.Many2one("ae.proyecto", string="Proyecto")
    lineas = fields.One2many("ae.cpago.line", "relacion", string="Lineas")
    tipo = fields.Selection([("Corporativo", "corporativo"),
        ("Distribución/Ventas", "ventas"), ("Producción", "produccion")],
        string="Tipo")

    def fix(self, cr, uid, ids, context=None):
        pl_obj = self.pool.get("ae.cpago.line")
        for i in self.browse(cr, uid, ids, context):
            for j in i.lineas:
                pl_obj.write(cr, uid, [j.id], {'relacion': i.id})

    def concilia(self, cr, uid, ids, context=None):
        ret = {}
        pres_obj = self.pool.get("ae.presupuesto")
        for i in self.browse(cr, uid, ids, context):
            for j in i.lineas:
                if j.pagado:
                    continue
                ms_obj = self.pool.get("messages_server")
                pl_obj = self.pool.get("ae.cpago.line")
                for fact in ms_obj.browse(cr, uid, ms_obj.search(cr, uid, [])):
                    try:
                        if j.rfc == fact.fact.partner_id.vat or\
                            str("MX" + j.rfc) == fact.fact.partner_id.vat:
                            print("RFC Aprobado")
                            #Checando monto
                            print("Checando monto")
                            print((str(j.monto) + "VS" +
                                str(fact.fact.amount_total)))
                            if j.monto == fact.fact.amount_total:
                                print("Monto OK")
                                pl_obj.write(cr, uid,
                                    [j.id], {'recibido': True})
                                #pl_obj.write(cr, uid, [j.id],
                                #    {'pago': fact.id})
                                pl_obj.write(cr, uid, [j.id],
                                    {'factura': fact.fact.id})
                                print("Recibido True")
                                print("Escribiendo en la linea")
                                print((fact.id))
                                print(("La linea"))
                    except:
                        continue
                #Buscando un presupuesto compatible
                for pres in pres_obj.browse(cr, uid, pres_obj.search(cr, uid,
                [('proyecto.id', '=', i.proyecto.id)])):
                    #Buscando una linea de presupuesto que haga match
                    for l in pres.linea:
                        if str(l.clave) == str(j.concepto):
                            if l.mes == i.mes:
                                if l.year == i.year:
                                    self.pool.get("ae.cpago.line").write(cr,
                                    uid, [j.id], {'presupuestado': True})
                                    if l.monto < (l.total + j.monto):
                                        self.pool.get("ae.cpago.line").write(
                                        cr, uid, [j.id],
                                        {'excedido': True})
                                    for fact in ms_obj.browse(cr, uid,
                                        ms_obj.search(cr, uid, [])):
                                        try:
                                            if j.rfc == fact.fact.partner_id.vat or\
                                                str("MX" + j.rfc) ==\
                                                fact.fact.partner_id.vat:
                                                if j.monto == \
                                                    fact.fact.amount_total:
                                                    ms_obj.write(cr, uid, [fact.id],
                                                        {'linea': l.id})
                                                    pl_obj.write(cr, uid, [j.id],
                                                        {'factura': fact.fact.id})
                                        except:
                                            continue
        return ret


class jmdpagoline(models.Model):
    _name = "ae.cpago.line"
    _inherit = "mail.thread"

    def process_payment(self, cr, uid, ids, context=None):
        inv_obj = self.pool.get("account.invoice")
        print("Entrando al metodo")
        for i in self.browse(cr, uid, ids, context):
            print("Aqui 1")
            self.write(cr, uid, [i.id], {
                    'programado': True
                })
            print("Aqui 2")
            inv_obj.write(cr, uid, [i.factura.id], {'state': 'open'})
            print("Aqui 3")
            #creando la poliza

    def provisiona(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            poliza_obj = self.pool.get("account.move")
            idpoliza = poliza_obj.create(cr, uid, {
                    'name': "Provisión factura" + str(i.rfc),
                    'journal_id': i.diario.id,
                }, context)
            linea_obj = self.pool.get("account.move.line")
            print(("Monto " + str(i.factura.amount_total)))
            neto = i.factura.amount_total
            linea_obj.create(cr, uid, {
                    'name': "Cargo al Gasto" + str(i.rfc),
                    'account_id': i.cargo.id,
                    'debit': neto,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "Abono al Proveedor " + str(i.rfc),
                    'account_id': i.abono.id,
                    'credit': neto,
                    'move_id': idpoliza,
                }, context)
            self.write(cr, uid, [i.id], {'provisionado': True})

    def cancela_provision(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            poliza_obj = self.pool.get("account.move")
            idpoliza = poliza_obj.create(cr, uid, {
                    'name': "Cancelación de provisión factura" + str(i.rfc),
                    'journal_id': i.diario.id,
                }, context)
            linea_obj = self.pool.get("account.move.line")
            print(("Monto " + str(i.factura.amount_total)))
            neto = i.factura.amount_total
            linea_obj.create(cr, uid, {
                    'name': "Abono al Gasto" + str(i.rfc),
                    'account_id': i.cargo.id,
                    'credit': neto,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "Cargo al Proveedor " + str(i.rfc),
                    'account_id': i.abono.id,
                    'debit': neto,
                    'move_id': idpoliza,
                }, context)
            self.write(cr, uid, [i.id], {'provisionado': False})

    def cancel_move(self, cr, uid, ids, context=None):
        print("Antes del Ciclo")
        for i in self.browse(cr, uid, ids, context):
            print("Fuera del Ciclo")
            self.write(cr, uid, [i.id], {
                'recibido': False,
                'excedido': False,
                'provisionado': False,
                'ok': False,
                'programado': False,
                'pagado': False,
                'presupuestado': False})
            print("Escrito")
            if(i.asiento):
                self.pool.get('account.move').unlink(cr, uid, [i.asiento.id])
            if(i.factura):
                self.pool.get('account.invoice').unlink(cr, uid, [i.factura.id])
            if(i.apago):
                self.pool.get('account.move').unlink(cr, uid, [i.apago.id])
            if(i.pago):
                self.pool.get('account.voucher').unlink(cr, uid, [i.pago.id])

    def pay(self, cr, uid, ids, context=None):
        inv_obj = self.pool.get("account.invoice")
        pay_obj = self.pool.get("account.voucher")
        usr_obj = self.pool.get("res.users")

        for i in self.browse(cr, uid, ids, context):
            self.write(cr, uid, [i.id], {
                    'pagado': True
                })
            inv_obj.write(cr, uid, [i.factura.id], {'state': 'paid'})
            #creando la poliza
            poliza_obj = self.pool.get("account.move")
            idpoliza = poliza_obj.create(cr, uid, {
                    'name': "Pago factura " + str(i.rfc),
                    'journal_id': i.diario.id,
                }, context)
            linea_obj = self.pool.get("account.move.line")
            print(("Monto " + str(i.factura.amount_total)))
            neto = i.factura.amount_total + i.factura.iva -\
                i.factura.retisr - i.factura.retiva
            linea_obj.create(cr, uid, {
                    'name': "Bancos Factura " + str(i.rfc),
                    'account_id': i.banco.id,
                    'credit': neto,
                    'move_id': idpoliza,
                }, context)
            print("Banco abonado")
            linea_obj.create(cr, uid, {
                    'name': "Proveedores Factura " + str(i.rfc),
                    'account_id': i.abono.id,
                    'debit': neto,
                    'move_id': idpoliza,
                }, context)
            print(("Valor del cargo " + str(i.factura.iva)))
            linea_obj.create(cr, uid, {
                    'name': "IVA Pagado Factura " + str(i.rfc),
                    'account_id': i.iva.id,
                    'debit': i.factura.iva,
                    'credit': 0,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "IVA Pdte Factura " + str(i.rfc),
                    'account_id': i.ivap.id,
                    'credit': i.factura.iva,
                    'debit': 0,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "ISR Ret. Pagado Factura " + str(i.rfc),
                    'account_id': i.risr.id,
                    'credit': i.factura.retisr,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "ISR Ret. Pdte. Factura " + str(i.rfc),
                    'account_id': i.risrp.id,
                    'debit': i.factura.retisr,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "IVA Ret. Pagado Factura " + str(i.rfc),
                    'account_id': i.riva.id,
                    'credit': i.factura.retiva,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "IVA Ret. Pdte. Factura " + str(i.rfc),
                    'account_id': i.rivap.id,
                    'debit': i.factura.retiva,
                    'move_id': idpoliza,
                }, context)
            self.write(cr, uid, [i.id], {'abanco': idpoliza})
            for u in usr_obj.browse(cr, uid, [uid], context):
                pay_id = pay_obj.create(cr, uid, {
                    'partner_id': i.factura.partner_id.id,
                    'amount': neto,
                    'company_id': u.company_id.id,
                    'account_id': i.banco.id,
                    'journal_id': i.diario.id,
                    })
                self.write(cr, uid, [i.id], {'pago': pay_id,
                    'apago': idpoliza})
                inv_obj.write(cr, uid, [i.factura.id],
                    {'payment_ids': [pay_id]})

    def authorize_invoice(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            self.write(cr, uid, [i.id], {'ok': True})
            poliza_obj = self.pool.get("account.move")
            print("Aqui 4")
            idpoliza = poliza_obj.create(cr, uid, {
                    'name': "Factura " + str(i.rfc),
                    'journal_id': i.diario.id,
                }, context)
            print("Aqui 5")
            linea_obj = self.pool.get("account.move.line")
            print(("IVA DE LA FACTURA " + str(i.factura.iva)))
            iva = i.factura.iva
            print(("ISR RET DE LA FACTURA " + str(i.factura.retisr)))
            risr = i.factura.retisr
            print(("EL ISR ES " + str(risr)))
            print(("IVA RET DE LA FACTURA " + str(i.factura.retiva)))
            riva = i.factura.retiva
            linea_obj.create(cr, uid, {
                    'name': "Gasto Factura " + str(i.rfc),
                    'account_id': i.cargo.id,
                    'debit': i.factura.amount_total,
                    'move_id': idpoliza,
                }, context)
            abono_proveedor = i.factura.amount_total + i.factura.iva -\
                i.factura.retisr - i.factura.retiva
            linea_obj.create(cr, uid, {
                    'name': "Proveedor Factura " + str(i.rfc),
                    'account_id': i.abono.id,
                    'credit': abono_proveedor,
                    'move_id': idpoliza,
                }, context)
            print(("EL ISR ES ANTES DE ASENTAR " + str(risr)))
            linea_obj.create(cr, uid, {
                    'name': "ISR Retenido Pendiente Factura " + str(i.rfc),
                    'account_id': i.risrp.id,
                    'credit': risr,
                    'debit': 0,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "IVA Pendiente Factura " + str(i.rfc),
                    'account_id': i.ivap.id,
                    'debit': iva,
                    'move_id': idpoliza,
                }, context)
            linea_obj.create(cr, uid, {
                    'name': "IVA Retenido Pendiente Factura " + str(i.rfc),
                    'account_id': i.rivap.id,
                    'credit': riva,
                    'move_id': idpoliza,
                }, context)
            self.write(cr, uid, [i.id], {'asiento': idpoliza})
        return ret

    def get_account(self, cr, uid, ids, context=None):
        ret = {}
        pt_obj = self.pool.get("ae.presupuesto.template")
        cta_obj = self.pool.get("account.account")
        fl_obj = self.pool.get("account.invoice.line")
        usr_obj = self.pool.get("res.users")
        for i in self.browse(cr, uid, ids, context):
            for u in usr_obj.browse(cr, uid, [uid], context):
                if u.company_id and u.company_id.cuenta_facutra:
                    id_cuenta = u.company_id.cuenta_facutra.id
                    self.write(cr, uid, [i.id], {'abono': id_cuenta})
                    id_diario = u.company_id.diario_factura.id
                    self.write(cr, uid, [i.id], {'diario': id_diario})
                    self.write(cr, uid, [i.id], {'banco':
                        u.company_id.cuenta_pagos.id})
                    id_ivap = u.company_id.cta_ivap.id
                    id_risrp = u.company_id.cta_risrp.id
                    id_rivap = u.company_id.cta_rivap.id
                    self.write(cr, uid, [i.id], {'ivap': id_ivap})
                    self.write(cr, uid, [i.id], {'rivap': id_rivap})
                    self.write(cr, uid, [i.id], {'risrp': id_risrp})
                    id_iva = u.company_id.cta_iva.id
                    id_risr = u.company_id.cta_risr.id
                    id_riva = u.company_id.cta_riva.id
                    self.write(cr, uid, [i.id], {'iva': id_iva})
                    self.write(cr, uid, [i.id], {'riva': id_riva})
                    self.write(cr, uid, [i.id], {'risr': id_risr})
            clave_proyecto = i.relacion.proyecto.cuenta
            clave_linea = ""
            for j in pt_obj.browse(cr, uid,
                pt_obj.search(cr, uid, [("clave", "=", i.concepto)])):
                clave_linea = j.cuenta
            cuenta = str(clave_proyecto) + "-" + str(clave_linea)
            for k in cta_obj.browse(cr, uid, cta_obj.search(cr, uid,
                [('code', '=', cuenta)])):
                for l in i.factura.invoice_line:
                    fl_obj.write(cr, uid, [l.id], {'account_id': k.id})
                    self.write(cr, uid, [i.id], {'cargo': k.id})
        return ret

    name = fields.Char("Nombre")
    relation = fields.Many2one("ea.pago")
    relacion = fields.Many2one("ae.cpago")
    linea = fields.Many2one("ae.presupuesto.linea")
    concepto = fields.Char("Clave del Concepto")
    recibido = fields.Boolean("Recibido")
    excedido = fields.Boolean("Excedido")
    provisionado = fields.Boolean("Provisionado")
    ok = fields.Boolean("Ok Contabilidad")
    programado = fields.Boolean("Programado")
    pagado = fields.Boolean("Pagado")
    presupuestado = fields.Boolean("Presupuestado")
    rfc = fields.Char("RFC")
    monto = fields.Float("Monto")
    divisa = fields.Many2one("res.currency", string="Divisa")
    factura = fields.Many2one("account.invoice", string="Factura")
    pago = fields.Many2one("messages_server", string="Cuenta por Pagar")
    cargo = fields.Many2one("account.account", string="Cuenta de Cargo")
    abono = fields.Many2one("account.account", string="Cuenta Abono")
    banco = fields.Many2one("account.account", string="Cuenta del Banco")
    ivap = fields.Many2one("account.account", string="Cta. IVA Pdte.")
    risrp = fields.Many2one("account.account", string="Cta. Ret. ISR Pdte.")
    rivap = fields.Many2one("account.account", string="Cta de Ret. IVA Pdte.")
    iva = fields.Many2one("account.account", string="Cta. IVA Pagado")
    risr = fields.Many2one("account.account", string="Cta. Ret. ISR Pagado")
    riva = fields.Many2one("account.account", string="Cta de Ret. IVA Pagado")
    diario = fields.Many2one("account.journal", string="Diario")
    asiento = fields.Many2one("account.move", string="Asiento Contable")
    apago = fields.Many2one("account.move", string="Asiento Pago")
    pago = fields.Many2one("account.voucher", string="Pago")


class inherit_jmd_presupuesto(models.Model):
    _inherit = 'ae.presupuesto.linea'

    def get_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.facturas:
                ret[i.id] = ret[i.id] + j.fact.amount_total
        return ret

    facturas = fields.One2many('messages_server', 'linea',
             string='Facturas')
    total = fields.Float("Total")