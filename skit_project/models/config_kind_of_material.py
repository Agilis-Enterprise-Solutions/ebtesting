# -*- coding: utf-8 -*-

from odoo import fields, models,api


class SkitKindOfMaterial(models.Model):
    _name = 'config.material'
    _description = 'Kind Of Material'

    name = fields.Char('Kind of material')
    spec_item_no = fields.Many2one("skit.config.specitem","Spec's Item number" ,required=True)
    grading = fields.Many2many('config.abrasion' )
    
     
