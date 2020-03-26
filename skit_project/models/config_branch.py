# -*- coding: utf-8 -*-

from odoo import fields, models


class SkitBranch(models.Model):
    _name = 'config.branch'
    _description = 'Branch'

    name = fields.Char('Branch Name')
    branch_code = fields.Char('Branch code')


class skitProductPrice(models.Model):
    _inherit = 'product.pricelist'
    _description = 'Added New Branch Field'

    branch_id = fields.Many2one('config.branch', 'Branch')


class skitLocation(models.Model):
    _name = 'skit.location'
    _description = 'Location'

    name = fields.Char("Location")
