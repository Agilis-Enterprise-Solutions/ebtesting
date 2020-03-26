# -*- coding: utf-8 -*-

from odoo import fields, models,api

class SkitSpecItem(models.Model):
    _name = 'skit.config.specitem'
    _decription =" Spec' Item number" 
    
    name = fields.Char("Spec's Item number")       