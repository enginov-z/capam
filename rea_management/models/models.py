# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError

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
    today_state_real = fields.Char("Etat d'aujourd'hui ")
    next_free_dtae = fields.Date('Date de Disponibilité')

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
                x.today_state_real = 'Occupé'
                x.next_free_dtae = pickup_this_date.return_date
            else:
                x.today_state = 'l'
                x.today_state_real = 'Libre'
                x.next_free_dtae = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
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
        company_id = self.env['res.company'].search([('name','=',self.company_name)])
        self.x_studio_current_company_2 = company_id.id
        self = self.with_context({
'test': 'test_value',
})
        if self.company_name == self.x_studio_current_company_2.name:
            self.update({
                'x_studio_current_company_bool' : True
            })
        else:
            self.update({
                'x_studio_current_company_bool' : False
            })
    x_studio_current_company_2 = fields.Many2one('res.company', compute=get_default_company)


    

    @api.onchange('x_studio_date_de_naissance')
    def set_age(self):
        if self.x_studio_date_de_naissance:
            self.x_studio_age_1 = int((datetime.datetime.today().date() - self.x_studio_date_de_naissance).days / 365)

class ResCompanyInherit(models.Model):
    _inherit="res.company"

    def get_full_address(self):
        a = "{0},{1},{2},{3}".format(self.street,self.zip, self.city , self.country_id.name)
        self.update({
            'x_studio_contact_address_complete' : a
            'x_studio_contact_address_complete_1' : a
        })

    x_studio_contact_address_complete = fields.Char('Contact adress complete', compute=get_full_address)

    def get_available_beds(self):
        total_products = self.x_studio_lit_totals
        not_available_products = 0 
        
        for x in self.x_studio_field_keWp2_1:
            if len(self.env['sale.order.line'].search(
                [('product_id.product_tmpl_id','=',x.id)
                ,('is_rental','=',True)
                ,('pickup_date','<=',datetime.datetime.today())
                ,('return_date','>=',datetime.datetime.today())
                ])) >0:
                not_available_products = not_available_products + 1 
        self.x_studio_available_beds_temp_1_1 = len(self.x_studio_field_keWp2_1) - not_available_products
        self.update({
            'x_studio_lits_disponible' : len(self.x_studio_field_keWp2_1) - not_available_products
        })

    def get_total_beds(self):
        self.x_studio_total_beds_temp_1 = len(self.x_studio_field_keWp2_1)
        self.update({
            'x_studio_lit_totals' : self.x_studio_total_beds_temp_1
        })
        
    x_studio_available_beds_temp_1_1 = fields.Integer('Lits Disponible', compute=get_available_beds)
    x_studio_total_beds_temp_1 = fields.Integer('Lits totale', compute=get_total_beds)
    x_studio_field_keWp2_1 = fields.One2many('product.template','company_id')

class ReportRangeAvailability(models.Model):
    _name = "report.range.availability1"
    _description = "Beds availability"

    dat = fields.Date('Date')
    free_beds = fields.Integer('Lits disponible')
    occupied_beds = fields.Integer('Lits occupé')

class WizardRangeAvailability(models.Model):
    _name="wizard.range.availability1"

    date_from = fields.Date("Date debut")
    date_to = fields.Date("Date jusqu'a")


    def return_interface(self):
        for x in self.env['report.range.availability1'].search([]):
            x.unlink()
        d1 = self.date_from
        d2 = self.date_to
        c = 0
        r = (d2-d1).days + 1 
        date_list = [d1 + timedelta(days=c) for c in range(0, r)]
        for x in date_list:
            occupied = 0 
            free = 0 
            for y in self.env['product.template'].search([('company_id','=',self.env.company.id)]):
                if len(self.env['sale.order.line'].search([('product_id.product_tmpl_id','=',y.id)
                ,('is_rental','=',True)
                ,('pickup_date','<=',x)
                ,('return_date','>=',x)])) > 0 :
                    occupied = occupied + 1 
                else :
                    free = free + 1 
            self.env['report.range.availability1'].create({
                'dat':x,
                'free_beds':free,
                'occupied_beds': occupied
            })

class respartnerinherit(models.Model):
    _inherit="res.partner"
    _rec_name="name"
    
    display_name = fields.Char(related="name",string="Nom affiché",store=True)

class rentalwizardinherit(models.TransientModel):
    _inherit="rental.wizard"

    @api.onchange('pickup_date')
    def get_return_date(self):
        s = ""
        s = str(type(self.pickup_date))
        if s == "<class 'bool'>":
            self.pickup_date = datetime.datetime.today()
            self.return_date = datetime.datetime.today() + datetime.timedelta(days=10)
    
    def get_pickup_date(self):
        self.pickup_date = datetime.datetime.today()

    return_date = fields.Datetime("Date retour", default=get_return_date)
    pickup_date = fields.Datetime("Date Reservation", default=get_pickup_date)

class orderlineinherit(models.Model):
    _inherit="sale.order.line"
    
    @api.constrains('product_id')
    def control_prod(self):
            if len(self.env['sale.order.line'].search([('id','!=',self.id),('product_id','=',self.product_id.id)
                    ,('is_rental','=',True)
                    ,('pickup_date','<=',self.pickup_date)
                    ,('return_date','>=',self.pickup_date)])) > 0:
                    raise UserError('Erreur , le lit est deja affecté dans cette date')



    


        