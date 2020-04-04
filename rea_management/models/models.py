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
        for x in self:
            pickup_this_date = self.env['sale.order.line'].search(
                [('product_id.product_tmpl_id','=',x.id)
                ,('is_rental','=',True)
                ,('pickup_date','<=',datetime.datetime.today())
                ,('return_date','>=',datetime.datetime.today())
                ])
            if len(pickup_this_date) > 0 :
                x.today_state = 'o'
                x.next_free_dtae = pickup_this_date.return_date
            else:
                x.today_state = 'l'
                x.next_free_dtae = datetime.datetime.strftime(datetime.datetime.today(), "%d/%m/%Y")
        return True

    def open_create_affectation(self):
        return {
             
            'name': 'Créer affectation',
            'view_mode': 'form',
            
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'context': {'default_is_rental_order': 1, 'search_default_from_rental': 1},
            'target': 'current',
            
        }

class ResPartnerInherit(models.Model):
    _inherit="res.partner"
    def get_default_company(self):
        raise UserWarning(self.env.company)
        return self.env.user.company_id
    x_studio_current_company_2 = fields.Many2one('res.partner', compute=get_default_company)

    

    @api.onchange('x_studio_date_de_naissance')
    def set_age(self):
        if self.x_studio_date_de_naissance:
            self.x_studio_age_1 = int((datetime.datetime.today().date() - self.x_studio_date_de_naissance).days / 365)




