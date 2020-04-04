# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit="sale.order"

    rental_status = fields.Selection([
        ('draft', 'Bruillon'),
        ('sent', 'Quotation Sent'),
        ('pickup', 'Reservé'),
        ('return', 'Picked-up'),
        ('returned', 'Libre'),
        ('cancel', 'Annulé'),
    ], string="Etat des affectations", compute='_compute_rental_status', store=True)

class ProductTemplateInherit(models.Model):
    _inherit="product.template"

    today_state = fields.Char(compute="_get_daily_state", string="Etat d'aujourd'hui")
    next_free_dtae = fields.Date('Date de Disponibilité')

    def _get_daily_state(self):
        return "Libre"
