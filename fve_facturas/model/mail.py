# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import poplib
from email.Parser import Parser
from xml.dom import minidom


class mail_server (osv.Model):

    _name = 'mail_server'

    def eliminar_movimientos(self, cr, uid, ids, context=None):
        revisados = self.pool.get("messages_server")
        facturas = self.pool.get("account.invoice")
        rechazo_obj = self.pool.get("ae.rechazadas")
        move_obj = self.pool.get("account.move")

        for ir in self.browse(cr, uid, ids, context):
            #conectando
            if ir.i_layer is True:
                m = poplib.POP3_SSL(ir.i_server, ir.i_port)
            else:
                m = poplib.POP3(ir.i_server, ir.i_port)
            m.user(ir.i_user)
            m.pass_(ir.i_pass)

            #leyendo los mails
            mensajes = len(m.list()[1])

            for i in range(mensajes):
                response, headerLines, bytes = m.retr(i + 1)
                mensaje = '\n'.join(headerLines)
                p = Parser()
                email = p.parsestr(mensaje)
                if email.is_multipart():
                    part_count = 0
                    for part in email.get_payload():
                        part_count = part_count + 1
                        tipo = part.get_content_type()
                        if tipo == "application/xml" or tipo == "text/xml":
                            try:
                                fp = open('fact_process.xml', 'wb')
                                fp.write(part.get_payload(decode=True))
                                fp.close()
                                doc = minidom.parse('fact_process.xml')
                            except:
                                rechazo_obj.create(cr, uid, {
                                        'name': "XML No Válido",
                                        'descripcion': email
                                        })
                                continue
                            tagFolio = "tfd:TimbreFiscalDigital"
                            foli = ""
                            try:
                                folio = 0
                                folio = doc.getElementsByTagName(tagFolio)[0]
                                foli = folio.getAttribute('UUID')
                                print(("Folio de la factura" + str(foli)))
                            except:
                                rechazo_obj.create(cr, uid, {
                                        'name': "UUID No Encontado",
                                        'descripcion': doc
                                        })
                                print("Rompiendo el cicle X")
                                continue
                            #print(lFolio)
                            #print("Eiminando" + str(foli))
                            for ms in revisados.browse(cr, uid,
                                revisados.search(cr, uid, [('name', '=',
                                foli)])):
                                if(ms.fact and ms.fact.move_id):
                                    try:
                                        move_obj.write(cr, uid,
                                        [ms.fact.move_id.id],
                                        {'state': 'draft'})
                                        move_obj.unlink(cr, uid,
                                        [ms.fact.move_id.id])
                                    except:
                                        print("Movimiento no eliminado")
                                    try:
                                        facturas.unlink(cr, uid, [ms.fact.id])
                                    except:
                                        print("Factura no eliminada")

                                try:
                                    revisados.unlink(cr, uid, [ms.id])
                                except:
                                    print(("No se elimino " + str(foli)))

        return True

    def recibir_facturas(self, cr, uid, ids, context=None):
        revisados = self.pool.get("messages_server")
        facturas = self.pool.get("account.invoice")
        lineas = self.pool.get("account.invoice.line")
        partners = self.pool.get("res.partner")
        rechazo_obj = self.pool.get("ae.rechazadas")

        for ir in self.browse(cr, uid, ids, context):
            #conectando
            if ir.i_layer is True:
                m = poplib.POP3_SSL(ir.i_server, ir.i_port)
            else:
                m = poplib.POP3(ir.i_server, ir.i_port)
            m.user(ir.i_user)
            m.pass_(ir.i_pass)

            #leyendo los mails
            mensajes = len(m.list()[1])

            for i in range(mensajes):
                response, headerLines, bytes = m.retr(i + 1)
                mensaje = '\n'.join(headerLines)
                p = Parser()
                email = p.parsestr(mensaje)
                if email.is_multipart():
                    part_count = 0
                    for part in email.get_payload():
                        part_count = part_count + 1
                        tipo = part.get_content_type()
                        if tipo == "application/xml" or tipo == "text/xml":
                            try:
                                fp = open('fact_process.xml', 'wb')
                                fp.write(part.get_payload(decode=True))
                                fp.close()
                                doc = minidom.parse('fact_process.xml')
                            except:
                                rechazo_obj.create(cr, uid, {
                                        'name': "XML No Válido",
                                        'descripcion': email
                                        })
                                continue
                            tagFolio = "tfd:TimbreFiscalDigital"
                            foli = ""
                            try:
                                folio = 0
                                folio = doc.getElementsByTagName(tagFolio)[0]
                                foli = folio.getAttribute('UUID')
                                print(("Folio de la factura" + str(foli)))
                            except:
                                rechazo_obj.create(cr, uid, {
                                        'name': "UUID No Encontado",
                                        'descripcion': doc
                                        })
                                print("Rompiendo el cicle X")
                                continue
                            #print(lFolio)
                            try:
                                tagEmpresa = 'cfdi:Receptor'
                                empresa = doc.getElementsByTagName(tagEmpresa)[0]
                                nempresa = empresa.getAttribute('rfc')
                                print(("Nombre empresa " + nempresa))
                                u_obj = self.pool.get("res.users")
                                print("Aqui 1")
                                con = False
                                print("Aqui 2")
                                print(("User id " + str(uid)))
                                print("Aqui 3")
                                for cp in u_obj.browse(cr, uid, [uid]):
                                    print("Aqui 4")
                                    print(("Probando " + nempresa + "VS" +
                                        cp.company_id.rfc))
                                    print((str(nempresa != cp.company_id.rfc)))
                                    print("Aqui 4")
                                    if nempresa != cp.company_id.rfc:
                                        print("Broken")
                                        rechazo_obj.create(cr, uid, {
                                        'name': "Empresas no coinciden",
                                        'descripcion': nempresa + " VS " +
                                        cp.company_id.name
                                        })
                                        con = True
                                if con:
                                    print("Rompido")
                                    continue
                            except:
                                print("Aqui se rompio")
                                rechazo_obj.create(cr, uid, {
                                        'name': "Empresa no coincide",
                                        'descripcion': email
                                        })
                                continue
                            #revisar que no existe ya el registro
                            print("Aqui 5")
                            idm = revisados.search(cr, uid,
                                [('name', '=', foli),
                                ('cancelada', '=', False)])
                            print("Aqui 6")
                            ids_e = len(revisados.browse(cr, uid, idm, context))
                            print(ids_e)
                            print("Aqui 7")
                            if ids_e == 0:
                                print("Creando Factura")
                                #leyendo la fecha
                                tagComprobante = 'cfdi:Comprobante'
                                fe = doc.getElementsByTagName(tagComprobante)[0]
                                fecha = fe.getAttribute('fecha')
                                print(('Fecha: ' + fecha[0:10]))

                                iva = 0.0
                                riva = 0.0
                                risr = 0.0
                                try:
                                    print("Buscando Impuestos")
                                    ti = 'cfdi:Traslado'
                                    liva = doc.getElementsByTagName(ti)[0]
                                    print("Existe el IVA 0")
                                    siva = str(liva.getAttribute('importe'))
                                    print(("Valor del IVA" + siva))
                                    print((type(siva)))
                                    print((float(siva)))
                                    print("X")
                                    iva = float(siva)
                                    print(("EL IVA ES POR " + str(iva)))
                                    print("Mensaje x")
                                    ti2 = 'cfdi:Retencion'
                                    elemento = doc.getElementsByTagName(ti2)[0]
                                    print(("Que raro" + str(elemento)))
                                    for lret in doc.getElementsByTagName(ti2):
                                        print("Retención encontrada")
                                        impuesto = lret.getAttribute('impuesto')
                                        print(("Es XX " + impuesto))
                                        if impuesto == "IVA":
                                            print("Es IVA")
                                            riva = float(lret.getAttribute(
                                                'importe'))
                                            print(("Retencion " + str(riva)))
                                        print("No Es IVA")
                                        if impuesto == "ISR":
                                            print("Es ISR")
                                            risr = float(lret.getAttribute(
                                                'importe'))
                                            print(("Retencion " + str(risr)))
                                    print("Sali del ciclo")
                                except:
                                    print("Impuesto no encontrado")
                                #leyendo el RFC de quien emite la factura
                                print("Continuando")
                                tagEmisor = 'cfdi:Emisor'
                                emisor = doc.getElementsByTagName(tagEmisor)[0]
                                rfc = emisor.getAttribute('rfc')
                                print(("Proveedr: " + rfc))
                                #buscando al cliente por rfc
                                id_proveedor = 0
                                print("Aqui 8")
                                par = partners.search(cr, uid,
                                     [('vat', '=', rfc)])
                                print("Aqui 9")
                                iP = len(partners.browse(cr, uid, par, context))
                                print("Aqui 10")
                                if iP == 0:
                                    print("Aqui 11")
                                    rfc = "MX" + rfc
                                    print("Aqui 12")
                                    par = partners.search(cr, uid,
                                     [('vat', '=', rfc)])
                                    print("Aqui 13")
                                    iP = len(partners.browse(cr, uid, par,
                                        context))
                                if iP == 0:

                                    mensaje = 'No existe el proveedor con RFC'
                                    print(('Error de Proveedor' + mensaje
                                         + ': ' + rfc))
                                    rechazo_obj.create(cr, uid, {
                                        'name': emisor,
                                        'rfc': rfc,
                                        'descripcion': "RFC No Encontrado"
                                        })
                                    continue

                                for i in partners.browse(cr, uid, par, context):
                                    id_proveedor = i.id

                                #creando la factura
                                id_fact = facturas.create(cr, uid,
                                     {
                                      'partner_id': id_proveedor,
                                      'date_invoice': fecha[0:10],
                                      'account_id': 209,
                                      'journal_id': 2,
                                      'type': 'in_invoice',
                                      'reference_type': 'none',
                                      'currency_id': 34,
                                      'iva': iva,
                                      'retiva': riva,
                                      'retisr': risr,
                                     },
                                 context)

                                #leyendo los conceptos de compra
                                #print("Productos")
                                tagConcepto = 'cfdi:Concepto'
                                prods = doc.getElementsByTagName(tagConcepto)
                                for prod in prods:
                                    cantidad = prod.getAttribute('cantidad')
                                    desc = prod.getAttribute('descripcion')
                                    precio = prod.getAttribute('valorUnitario')
                                    #print("")
                                    #print("    Cant.: " + cantidad)
                                #print("    Desc.: " + desc.encode("latin1"))
                                    #print("    Precio: " + precio)
                                    #creando las lineas de la factura
                                    lineas.create(cr, uid,
                                         {
                                            'invoice_id': id_fact,
                                            'name': desc,
                                            'quantity': cantidad,
                                            'price_unit': precio,
                                            'account_id': 28131,
                                         },
                                     context)

                                #Colocando los impuestos
                                for fa in facturas.browse(cr, uid, [id_fact]):
                                    total = fa.amount_total + iva - riva - risr
                                    facturas.write(cr, uid, [fa.id],
                                        {'total': total})

                                #creando el registro de guardado
                                revisados.create(cr, uid,
                                     {
                                      'name': foli,
                                      'from': email["From"],
                                      'to': email["To"],
                                      'fact': id_fact,
                                      'fecha': fecha[0:10],
                                      'proveedor': id_proveedor,
                                     },
                                 context)
        return True

    _columns = {
        'name': fields.char('Description'),

        'i_server': fields.char('Server'),
        'i_port': fields.integer('Port'),
        'i_type': fields.selection([('i', 'IMAP'), ('p', 'POP')], 'Protocol'),
        'i_layer': fields.boolean('SSL'),
        'i_user': fields.char('User'),
        'i_pass': fields.char('Password'),

        'o_server': fields.char('Server'),
        'o_port': fields.integer('Port'),
        'o_layer': fields.boolean('SSL'),
        'o_user': fields.char('User'),
        'o_pass': fields.char('Password')
    }


class messages_server (osv.Model):
    _inherit = "mail.thread"
    _name = 'messages_server'
    _columns = {
        'name': fields.char('Folio'),
        'from': fields.char('De'),
        'to': fields.char('Para'),
        'fact': fields.many2one('account.invoice', string='Factura'),
        'fecha': fields.date('Fecha'),
        'linea': fields.many2one('ae.presupuesto.linea',
             string='Presupuesto'),
        'proveedor': fields.many2one("res.partner", string="Proveedor"),
        'costos': fields.one2many("ae.ccostos_line",
            "message_id", string="Distribución de Costos", ),
        'uid': fields.char("UID"),
        'cancelada': fields.boolean("Cancelada")
    }


class jmdccostos(osv.Model):
    _inherit = "mail.thread"
    _name = "ae.ccostos_line"
    _columns = {
        'name': fields.char(string="Descripción", size=40),
        'monto': fields.float(string="Monto", digits=(9, 2)),
        'centro': fields.many2one("ae.centro_costos",
            string="Centro de Costos"),
        'comentario': fields.char("Comentario"),
        'message_id': fields.many2one("messages_server",
            string="Gasto", ondelete="set null"),
        'proyecto_id': fields.many2one("ae.proyecto", string="Proyecto"),
        }


class relacion_presupuesto_mensaje(osv.Model):
    _name = 'presupuesto_mensaje'
    _columns = {
        'id_m': fields.integer('Id del mensaje'),
        'id_p': fields.integer('id de la linea')
    }