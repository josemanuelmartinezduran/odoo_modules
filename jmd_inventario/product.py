# -*- coding: utf-8 -*-
from openerp import models, fields, api


class jmd_asset(models.Model):
    _inherit = "mail.thread"
    _name = "product.asset"

    @api.depends('descripcion')
    def get_desc(self):
        for record in self:
            record.desc_40 = record.descripcion[:70]

    desc_40 = fields.Char("Descripcion 40", compute=get_desc)
    numero = fields.Integer("Numero de Activo", default=lambda self:
         self.env["ir.sequence"].get("product.asset"))
    name = fields.Char("Folio del Inventario", default=lambda self:
         self.env["ir.sequence"].get("product.asset.name"))
    descripcion = fields.Char("Descipción")
    clave = fields.Char("Clave CAMBS")
    descripcionl = fields.Char("Descripción Larga")
    adscripcion = fields.Char("Adscripcion")
    responsable = fields.Char("Responsable")
    resguardo = fields.Char("Resguardo")
    origen = fields.Char("Origen")
    ubicacion = fields.Char("Ubicación Fisica")
    grupo = fields.Char("Grupo del Bien")
    tipo = fields.Char("Tipo")
    marca = fields.Char("Marca")
    modelo = fields.Char("Modelo")
    serie = fields.Char("Numero de Serie")
    proveedor = fields.Char("Provedor")
    requisicion = fields.Char("Requisición")
    valor = fields.Float("Valor de Adquisición")
    estado = fields.Char("Estado")
    fecha = fields.Char("Fecha de Adquisición")
    resguargo = fields.Binary("Archivo del resguardo")
    nresguardo = fields.Char("Nombre del Archivo")
    codigo_barras = fields.Char("Codigo de Barras")
    notas = fields.Text("Notas")
    imagen1 = fields.Binary("Imagen 1")
    nimagen1 = fields.Char("Nombre ")
    imagen2 = fields.Binary("Imagen 2")
    nimagen2 = fields.Char("Nombre ")
    hallazgo = fields.Boolean("Hallazgo")
    nuevo = fields.Boolean("Nuevo")
    baja = fields.Boolean("Baja")
    faltante = fields.Boolean("Faltantes")
    sobrante = fields.Boolean("Sobrante")
    coordinacion = fields.Char("Coordinación")

