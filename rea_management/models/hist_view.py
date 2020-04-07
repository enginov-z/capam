# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError

class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('hist', "Histogramme")])

class ActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(selection_add=[('hist', "Histogramme")])