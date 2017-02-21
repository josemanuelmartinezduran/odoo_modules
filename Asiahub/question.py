# -*- coding: utf-8 -*-
from openerp import models, fields, api
from .lib.meli import Meli


class jmdqestion(models.Model):
    _inherit = "mail.thread"
    _name = "meli.question"
    name = fields.Char("Id")
    question = fields.Char("Question")
    answer = fields.Char("Answer")

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


class jmd(models.Model):
    _inherit = "mercadolibre.questions"

    @api.one
    def do_answer(self):
        ret = {}
        company = self.env['res.company'].browse(
                self.env['res.company']._company_default_get('product.product'))
        if company.mercadolibre_access_token == "":
            raise Warning('The access token is not set')
        if self.question_id == "":
            raise Warning("This question has not been downloaded from Mercado")
        if self.status != "UNANSWERED":
            raise Warning("The question is no longer available to be answered")
        meli = Meli(client_id=company.mercadolibre_client_id,
        client_secret=company.mercadolibre_secret_key,
        access_token=company.mercadolibre_access_token)
        body = {
        "question_id": self.question_id,
        'text': self.answer_text,
        }
        response = meli.post("/answers", body,
            {'access_token': meli.access_token})
        print(("Response= " + response.content))
        return ret