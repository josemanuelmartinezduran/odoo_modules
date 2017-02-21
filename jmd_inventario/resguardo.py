# -*- coding: utf-8 -*-
from openerp import models, fields, api


class jmd(models.Model):
    _inherit = "mail.thread"
    _name = "inv.resguardo"
    name = fields.Char("Nombre de la Persona")
    fecha = fields.Date("Fecha")
    area = fields.Char("Area de Adscripción")
    puesto = fields.Char("Puesto")
    ubicacion = fields.Char("Ubicación Física")
    estatus = fields.Char("Estatus")
    num_empleado = fields.Char("Numero de Empleado")
    rfc = fields.Char("RFC")
    numero = fields.Char("Numero de Resguardo")
    num_bienes = fields.Integer("Numero de Bienes")
    num_faltantes = fields.Integer("Total de faltantes")
    total_monto = fields.Float("Valor del Resguardo")
    total_bajas = fields.Integer("Total de Bajas")
    linea_ids = fields.One2many("inv.resguardo.line",
        "relation_id", string="Lineas")
    responsable_bienes = fields.Char("Responsable de los Bienes")
    puesto_responsable = fields.Char("Puesto del Responsable")
    administrativo = fields.Char("Responsable Administrativo", default="WENCES JIMÉNEZ BARRIOS")
    puesto_administrativo = fields.Char("Puesto del Responsable Administrativo", default="GERENTE DE CONTROL DE BIENES Y ASEGURAMIENTO")

    @api.one
    def do_fill(self):
        ret = {}
        print("Inside")
        print((self.name))
        bienes = 0
        faltantes = 0
        monto = 0.0
        bajas = 0
        consecutivo = 1
        for j in self.linea_ids:
            j.unlink()
        for i in self.env["product.asset"].search([('responsable',
            'like', self.name)]):
            bienes += 1
            if i.faltante:
                faltantes += 1
            if i.baja:
                bajas += 1
            monto += i.valor
            self.env["inv.resguardo.line"].create({
                    'name': i.name,
                    'codigo': i.clave,
                    'relation_id': self.id,
                    'numero': i.numero,
                    'marca': i.marca,
                    'modelo': i.modelo,
                    'serie': i.serie,
                    'proveedor': i.proveedor,
                    'descripcion': i.descripcion,
                    'estado': i.estado,
                    'fecha': i.fecha,
                    'clave': i.clave,
                    'valor': i.valor,
                    'dcorta': i.descripcionl,
                    'consecutivo': consecutivo,
                    'ubicacion': i.ubicacion,
                })
            consecutivo = consecutivo + 1
        self.write({'num_bienes': bienes,
                    'num_faltantes': faltantes,
                    'total_monto': monto})
        return ret


class jmd_linea(models.Model):
    _inherit = "mail.thread"
    _name = "inv.resguardo.line"
    name = fields.Char("Activo")
    codigo = fields.Char("Codigo")
    numero = fields.Char("Numero")
    relation_id = fields.Many2one("inv.resguardo",
        string="Relation")
    marca = fields.Char("Marca")
    modelo = fields.Char("Modelo")
    serie = fields.Char("Numero de Serie")
    proveedor = fields.Char("Provedor")
    descripcion = fields.Char("Descripción Larga")
    dcorta = fields.Char("Descripción")
    estado = fields.Char("Estado")
    fecha = fields.Char("Fecha de Adquisición")
    clave = fields.Char("Clave")
    valor = fields.Float("Valor")
    ubicacion = fields.Char("Ubicación")
    consecutivo = fields.Integer("Consecutivo")