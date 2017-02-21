# -*- coding: utf-8 -*-
from openerp import models, fields, api


class jmdacta(models.Model):
    _inherit = "mail.thread"
    _name = "utils.acta"
    name = fields.Char("Adscripción")
    texto_apertura = fields.Text("Acta de Inicio",
        default="Siendo las xxxx horas del día xxxx del mes de octubre del año 2016 en las instalaciones del edificio que ocupa la Agencia promotora de xxxxxxxxxxxx. De la Financiera Nacional de Desarrollo Agropecuario, Rural, Forestal y Pesquero, se levanta la presente acta con la que se dan por iniciados los trabajos de SERVICIO DE LEVANTAMIENTO DE INVENTARIO DE BIENES MUEBLES E INSTRUMENTALES, que se encuentran en resguardo en la citada agencia para uso del personal que labora en dicho sitio. El objeto de este servicio es para confirmar la identificación física de los bienes, asimismo para dar cumplimiento a lo dispuesto por el Artículos 207, fracción II y 229 y 230 del Acuerdo en el que se establecen las disposiciones en Materia de Recursos Materiales y Servicios Generales, publicado en el Diario Oficial de la Federación el 16 de julio de 2010, reformado mediante el Acuerdo por el que se modifica el diverso por el que se establecen las disposiciones en Materia de Recursos Materiales y Servicios Generales publicado en el mismo instrumento de difusión el 20 de julio de 2011 y 03 de octubre de 2012; así como la actividad 2 del numeral 5.6.3., del Manual Administrativo de Aplicación General en Materia de Recursos Materiales y Servicios Generales; políticas 5.2.2.4, 5.2.2.6, 5.2.2.7 y 5.2.2.9 del Manual de Políticas y Procedimientos para la Administración y el Manejo de Almacenes.\
                Participan por la Empresa XXXXXXXXXXXXXXXXXXXXXX, Coordinación Regional XXXXXXX Agencia Estatal XXXXXXX los C. XXXXXXX Responsable del Servicio, XXXXXX Jefe de Departamento de Recursos Materiales y Servicios Generales, XXXXXXX Agente Estatal XXXXXXX ");
    texto_cierre = fields.Text("Acta de Cierre",
        default="Siendo las XXXXXXXXX horas del día XXXXX del mes de XXXXXXX del año 2016 en las instalaciones del edificio que ocupa la Agencia promotora de XXXXXXXXXXXXXXX de la Financiera Nacional de Desarrollo Agropecuario Rural, Forestal y Pesquero, se levanta la presente acta de cierre o conclusión de los trabajos de levantamiento de inventario de bienes muebles e instrumentales correspondiente al ejercicio fiscal 2016, que se encuentran en posesión y resguardo en dicha agencia, a efecto de dar cumplimiento a los dispuesto por los artículos 207 fracción II, 229 y 230 del Acuerdo en el que se establecen las disposiciones en Materia de Recursos Materiales y Servicios Generales, publicado en el Diario Oficial de la Federación el 16 de julio de 2010, reformado mediante el Acuerdo por el que se modifica el diverso por el que se establecen las disposiciones en Materia de Recursos Materiales y Servicios Generales publicado en el mismo instrumento de difusión el 20 de julio de 2011 y 03 de octubre de 2012; así como la actividad 9 del numeral 5.6.3., del Manual Administrativo de  Aplicación General en Materia de Recursos Materiales y Servicios Generales; política 5.2.2.6 del Manual de Políticas y Procedimientos para la Administración y el Manejo de Almacenes.\
        Participan por la Empresa prestadora de servicio XXXXXXXXXXXXXXXXXX Coordinación Regional Administrativo XXXXXXXXXXX los C. XXXXXXXXXXXXXXX Jefe de Departamento de Recursos Materiales y Servicios Generales y XXXXXXXXXXXXX.")
    acta_fin_cierre = fields.Text("Cierre Acta", default="No habiendo otro asunto que manifestar, se cierra la presente Acta, firmando por los que intervienen, siendo las 17:30 horas del día XXX de XXXXXXXXXXX de 2016.")
    persona_ids = fields.One2many("utils.personas", "relation_id",
        string="Personas")
    texto_bajas = fields.Text("Acta de Bajas", default="En la Ciudad de XXXXX siendo las 17:00 horas del día XX de XXXXXXX  2016, se procede a registrar en el Sistema de Control de Bienes (SICOB) diversos bienes muebles y equipo de administración que se reportaron como no identificados con folio de inventario de activo fijo de Financiera Nacional durante el levantamiento físico correspondiente al ejercicio fiscal 2016 en la Agencia estatal xxxxxxx de la FND.  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
                                                        De conformidad con los numerales 5.2.2.9 y 5.2.2.13 del Manual de Políticas y Procedimientos para la Administración de Bienes y el Manejo de Almacenes., 7.1.5 y 7.1.6 del Procedimiento para la Baja y Destino Final de los Bienes Muebles e Inmuebles, así como la fracción V del numeral 207 del Acuerdo por el que se establecen las Disposiciones en Materia de Recursos Materiales y Servicios Generales, se hace constar que los bienes que a continuación se enlistan, son propiedad de la Financiera Nacional de Desarrollo Agropecuario, Rural, Forestal y Pesquero, procediéndose a registrar como activo fijo en el Sistema de Control de Bienes (SICOB), así como contablemente, mismos que quedan identificados con el folio de inventario correspondiente y resguardados con los datos que los identifiquen de manera individual y valor conforme a bienes similares.-------------------------------------------------------------------------------------------------------------------------------------------------------------")
    texto_bajas2 = fields.Text("Final de las bajas", default="No habiendo otro asunto que agregar, se firma la presente Acta por triplicado, cerrándose el mismo día de su inicio a las 18:00 horas del día de la fecha. --------------------------------------------------------------")
    total_activos = fields.Integer("Total Bienes")
    total_faltantes = fields.Integer("Total de Faltantes")
    total_inventario = fields.Integer("Total Inventariado")
    total_bajas = fields.Integer("Total de Bajas")
    total_resguardos = fields.Integer("Total de Resguardos")
    fecha = fields.Char("Fecha")
    linea_ids = fields.One2many("acta.line","relation_id", string="Hallazgos")

    @api.one
    def do_fill(self):
        ret = {}
        total_act = 0
        faltantes = 0
        bajas = 0
        resguardos = 0
        print("Inside")
        print((self.name))
        for i in self.env["inv.resguardo"].search([('area',
            'like', self.name)]):
            resguardos += 1
            bajas += i.total_bajas
            total_act += i.num_bienes
            print("In")
            self.env["utils.personas"].create({
                    'name': i.name,
                    'total_bienes': i.num_bienes,
                    'total_faltantes': i.num_faltantes,
                    'monto': i.total_monto,
                    'fecha': i.fecha,
                    'relation_id': self.id,
                })
        for i in self.env["product.asset"].search([('adscripcion',
            'like', self.name)]):
            if(i.baja or i.faltante or i.sobrante):
                self.env["inv.resguardo.line"].create({
                    'name': i.descripcion,
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
                    'baja': i.baja,
                    'faltante': i.faltante,
                    'sobrante': i.sobrante,
                    'responsable': i.responsable,
                })
        self.write({'total_activos': total_act,
            'total_faltantes': faltantes,
            'total_inventario': (total_act - faltantes),
            'total_bajas': bajas,
            'total_resguardos': resguardos
            })
        return ret


class jmdpersona(models.Model):
    _inherit = "mail.thread"
    _name = "utils.personas"
    name = fields.Char("Persona")
    total_bienes = fields.Integer("Total Bienes")
    total_faltantes = fields.Integer("Total Faltantes")
    relation_id = fields.Many2one("utils.acta", string="Relation")
    monto = fields.Float("Monto")
    fecha = fields.Char("Fecha")


class jmd_linea(models.Model):
    _inherit = "mail.thread"
    _name = "acta.line"
    name = fields.Char("Activo")
    codigo = fields.Char("Codigo")
    numero = fields.Char("Numero")
    relation_id = fields.Many2one("utils.acta",
        string="Relation")
    marca = fields.Char("Marca")
    modelo = fields.Char("Modelo")
    serie = fields.Char("Numero de Serie")
    proveedor = fields.Char("Provedor")
    descripcion = fields.Char("Descripción")
    estado = fields.Char("Estado")
    fecha = fields.Char("Fecha de Adquisición")
    clave = fields.Char("Clave")
    valor = fields.Float("Valor")
    baja = fields.Boolean("Baja")
    sobrante = fields.Boolean("Sobrante")
    faltante = fields.Boolean("Faltante")
    responsable = fields.Char("Responsable")