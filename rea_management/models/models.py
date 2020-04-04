# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit="sale.order"

    x_rental_status = fields.Selection(selection=[
        ('free', 'Libre'),
        ('occupied', 'Occupé'),
        ('booked', 'Reservé'),

    ], string="Etat des affectations")
