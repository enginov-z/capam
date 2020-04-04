# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit="sale.order"

    rental_status = fields.Selection([
        ('free', 'Libre'),
        ('occupied', 'Occupé'),
        ('booked', 'Reservé'),

    ], string="Etat des affectations", compute='_compute_rental_status', store=True)