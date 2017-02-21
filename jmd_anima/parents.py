# -*- coding: utf-8 -*-
from openerp import models, fields, api


class jmdparents(models.Model):
    _inherit = "mail.thread"
    _name = "utils.parents"
    name = fields.Char("Descripción")
    cuenta_raiz = fields.Many2one("account.account", string="Cuenta Raiz")
    longitud = fields.Integer("Longitud de las cuentas")
    empresa = fields.Many2one("res.company", string="Empresa")
    excepciones = fields.One2many("utils.parents.errors", "parent_id",
        string="Cuentas con excepciones")
    tipo_vista = fields.Many2one("account.account.type",
        string="Tipo Para Vistas")
    inicia_con = fields.Char("Inicia con")

    @api.multi
    def set_parents(self):
        acc_obj = self.env['account.account']
        for l in acc_obj.search([('company_id', '=', self.empresa.id)]):
            codigo = l.code
            if codigo[:1] != self.inicia_con:
                continue
            print(("Cuenta " + str(l.code)))
            if len(codigo) == self.longitud:
                print("Primer Orden")
                l.write({'parent_id': self.cuenta_raiz.id})
                try:
                    l.write({'type': 'view', 'user_type': self.tipo_vista.id})
                except:
                    self.env["utils.parents.errors"].write({
                        'name': 'No puede ser vista',
                        'cuenta': l.id,
                        'parent_id': self.id})
            elif len(codigo) == (self.longitud * 2 + 1):
                print("Segundo Orden")
                parent = codigo[:self.longitud]
                busqueda = acc_obj.search([('code', '=', parent),
                    ('company_id', '=', self.empresa.id)])
                if len(busqueda) == 0:
                    self.env["utils.parents.errors"].write({
                            'name': 'Padre no encontrado' + str(parent),
                            'cuenta': l.id,
                            'parent_id': self.id})
                for p in busqueda:
                    l.write({'parent_id': p.id})
                    try:
                        p.write({'type': 'view',
                            'user_type': self.tipo_vista.id})
                    except:
                        self.env["utils.parents.errors"].write({
                            'name': 'No puede ser vista',
                            'cuenta': p.id,
                            'parent_id': self.id})
            elif len(codigo) == (self.longitud * 3 + 2):
                print("Tercer Orden")
                parent = codigo[:self.longitud * 2 + 1]
                busqueda = acc_obj.search([('code', '=', parent),
                    ('company_id', '=', self.empresa.id)])
                if len(busqueda) == 0:
                    self.env["utils.parents.errors"].write({
                            'name': 'Padre no encontrado' + str(parent),
                            'cuenta': l.id,
                            'parent_id': self.id})
                for p in busqueda:
                    l.write({'parent_id': p.id})
                    try:
                        p.write({'type': 'view',
                            'user_type': self.tipo_vista.id})
                    except:
                        self.env["utils.parents.errors"].write({
                            'name': 'No puede ser vista',
                            'cuenta': p.id,
                            'parent_id': self.id})
            elif len(codigo) == (self.longitud * 4 + 3):
                print("Cuarto Orden")
                parent = codigo[:self.longitud * 3 + 2]
                busqueda = acc_obj.search([('code', '=', parent),
                    ('company_id', '=', self.empresa.id)])
                if len(busqueda) == 0:
                    self.env["utils.parents.errors"].write({
                            'name': 'Padre no encontrado' + str(parent),
                            'cuenta': l.id,
                            'parent_id': self.id})
                for p in busqueda:
                    l.write({'parent_id': p.id})
                    try:
                        p.write({'type': 'view',
                            'user_type': self.tipo_vista.id})
                    except:
                        self.env["utils.parents.errors"].write({
                            'name': 'No puede ser vista',
                            'cuenta': p.id,
                            'parent_id': self.id})
            elif len(codigo) == (self.longitud * 5 + 4):
                print("Quinto Orden")
                parent = codigo[:self.longitud * 4 + 3]
                busqueda = acc_obj.search([('code', '=', parent),
                    ('company_id', '=', self.empresa.id)])
                if len(busqueda) == 0:
                    self.env["utils.parents.errors"].write({
                            'name': 'Padre no encontrado' + str(parent),
                            'cuenta': l.id,
                            'parent_id': self.id})
                for p in busqueda:
                    l.write({'parent_id': p.id})
                    try:
                        p.write({'type': 'view',
                            'user_type': self.tipo_vista.id})
                    except:
                        self.env["utils.parents.errors"].write({
                            'name': 'No puede ser vista',
                            'cuenta': p.id,
                            'parent_id': self.id})
        return True


class jmderrors(models.Model):
    _name = "utils.parents.errors"
    name = fields.Char("Descripción")
    cuenta = fields.Many2one("account.account", string="Cuenta")
    parent_id = fields.Many2one("utils.parents", string="Generador de Arbol")