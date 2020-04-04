# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class SaleOrderInherit(models.Model):
    _inherit="sale.order"

    x_rental_status = fields.Selection(selection=[
        ('draft', 'Brouillon'),
        ('sent', 'A Confirmer'),
        ('pickup', 'Reservé'),
        ('return', 'A retourné'),
        ('returned', 'Libre'),
        ('cancel', 'Annulé'),
    ], string="Etat des affectations")


class ProductTemplateInherit(models.Model):
    _inherit="product.template"

    today_state = fields.Selection(selection=[
        ('l', 'Libre'),
        ('o', 'Occupé'),
        ('r', 'Reservé'),
       
    ],compute="_get_daily_state", string="Etat d'aujourd'hui")
    next_free_dtae = fields.Char('Date de Disponibilité')

    def _get_daily_state(self):
        #get actual state
        self.ensure_one()
        pickup_this_date = self.env['sale.order.line'].search(
            [('product_tmpl_id','=',self.id)
            ,('is_rental','=',True)
            ,('pickup_date','<=',datetime.datetime.today())
            ,('return_date','>=',datetime.datetime.today())
            ])
        if len(pickup_this_date > 0 ):
            self.today_state = 'o'
            self.next_free_dtae = pickup_this_date.return_date
        else:
            self.today_state = 'l'
            self.next_free_dtae = datetime.datetime.strftime(datetime.datetime.today(), "%d/%m/%Y")
        return True

    def open_create_affectation(self):
        return {
            'xml_id':339, 
            'name': 'Créer affectation',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'target': 'new',
            
        }




