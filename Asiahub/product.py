# -*- coding: utf-8 -*-
from openerp import models, fields, api
from .lib.meli import Meli
from openerp.exceptions import Warning
import json
import urllib
import urllib2
import base64
import json


class jmdproduct(models.Model):
    _inherit = "product.product"
    condition = fields.Char("Condition", default="new")
    warranty = fields.Char("Warranty", default="30 dias")
    currency_name = fields.Char("Currency", default="BRL")
    accepts_mercadopago = fields.Boolean("Accepts Mercado Pago")
    description_meli = fields.Char("Description")
    listing_type_id = fields.Char("Listing Type", default="bronze")
    title_meli = fields.Char("Title Meli")
    qantity_meli = fields.Integer("Aviabke Qantity")
    price_meli = fields.Float("Price")
    buying_mode = fields.Char("Buying Mode", default="buy now")
    category_meli = fields.Char("Category", default="MLB1620")
    pictures_meli = fields.One2many("product.pictures",
        "relation_id", string="Pictures")
    meli_id = fields.Char("MELI ID")
    question_data = fields.Text("Question Data")
    chinesse_name = fields.Char("Chinesse Name")
    #CNova
    CDpto = fields.Char("Department 1st Level")
    CCat = fields.Char("Category 2nd Level")
    CSub1 = fields.Char("Subcategory 3rd Level")
    CSub2 = fields.Char("Subcategory 4th Level")
    CSub3 = fields.Char("Subcategory 5th Level")
    CName = fields.Char("Product Name")
    CDesc = fields.Char("Description")
    CSku = fields.Char("Sku")
    CEan = fields.Char("EAN/ISBN")
    CMarca = fields.Char("Marca")
    CPrice = fields.Char("Price from")
    CPrice2 = fields.Char("Price to")
    CHeight = fields.Char("Height (m)")
    CLenght = fields.Char("Lenght (m)")
    CDepth = fields.Char("Depth(m)")
    CWeight = fields.Char("Weight(kg)")
    CStock = fields.Char("Stock")
    CDeliver = fields.Char("Deliver Time")
    CPictures = fields.Text("Pictures")
    picture1 = fields.Binary("Picture 1")
    picture2 = fields.Binary("Picture 2")
    picture3 = fields.Binary("Picture 3")
    picture4 = fields.Binary("Picture 4")
    picture5 = fields.Binary("Picture 5")
    user_id = fields.Many2one('res.users', string='User',
        track_visibility='onchange', readonly=True,
        default=lambda self: self.env.user)

    @api.one
    def doanswer(self, cr, uid, ids, context=None):
        ret = {}
        meli = Meli(client_id='8751301154221455',
        client_secret="apZXtj36WNWbNZ5zGcR21U2C3AL4e5r0",
        access_token='APP_USR-8751301154221455-082318-1d69df1243e33f308e3d768c0cba5e99__E_F__-226142327')
        body = {
        "question_id": self.name,
        'text': self.answer,
        }
        response = meli.post("/answers", body, {'access_token': meli.access_token})
        print("La respuesta es")
        print((response.content))
        return ret

    @api.one
    def get_questions(self):
        ret = {}
        meli = Meli(client_id='8751301154221455',
        client_secret="apZXtj36WNWbNZ5zGcR21U2C3AL4e5r0",
        access_token='APP_USR-8751301154221455-082318-1d69df1243e33f308e3d768c0cba5e99__E_F__-226142327')
        response = meli.get("/questions/search?item=MLM564607342&access_token=APP_USR-8751301154221455-082318-1d69df1243e33f308e3d768c0cba5e99__E_F__-226142327")
        print(response.content)
        return ret

    @api.one
    def do_uploadcnova(self):
        ret = {}
        url = "https://desenvolvedores.cnova.com/api-portal/proxy/api/v2/loads/products"
        headers = {"client_id" : "7jspqddwKW8M", "access_token" : "sOjBL60bKo3a"}
        data = final_json;
        request = urllib2.Request(url)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_data(final_json)
        return ret

    @api.one
    def do_upload(self):
        ret = {}
        company = self.env['res.company'].browse(
                self.env['res.company']._company_default_get('product.product'))
        if company.mercadolibre_access_token == "":
            raise Warning('The access token is not set')
        meli = Meli(client_id=company.mercadolibre_client_id,
        client_secret=company.mercadolibre_secret_key,
        access_token=company.mercadolibre_access_token)
        body = {
        "condition": self.condition,
        "warranty": "60 Días",
        "currency_id": self.currency_name,
        "accepts_mercadopago": self.accepts_mercadopago,
        "description": self.description_meli,
        "listing_type_id": self.listing_type_id,
        "title": self.title_meli,
        "available_quantity": self.qantity_meli,
        "price": self.price_meli,
        "buying_mode": self.buying_mode,
        "category_id": self.category_meli}
        response = meli.post("/items", body,
            {'access_token': meli.access_token})
        print((response.content))
        dict_response = json.loads(response.content)
        try:
            meli_id = dict_response["id"]
            self.env["mercadolibre.posting"].create({
                'name': dict_response["id"],
                'meli_id': dict_response["id"]})
        except:
            raise Warning(("Invalid Log In Credentials Mercado Libre answered "
                + dict_response["message"]))
        self.write({'meli_id': meli_id})
        return ret


class jmdpictures(models.Model):
    _name = "product.pictures"
    name = fields.Char("Link")
    relation_id = fields.Many2one("product.product")