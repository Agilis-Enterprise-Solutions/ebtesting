# -*- coding: utf-8 -*-

from odoo import fields, models


class SkitConfigSoilAbrasion(models.Model):
    _name = 'config.soil.abrasion'
    _description = 'SOIL ABRASION TEST – CONFIGURATION'

    name = fields.Char("Passing")
    retained_on = fields.Char("RETAINED On")
    grading = fields.Many2one('config.abrasion', "Grading")
    specification = fields.Char("Specification")
    total = fields.Char("Total")


class SkitConfigAbrasion(models.Model):
    _name = 'config.abrasion'
    _description = 'SOIL ABRASION TEST – CONFIGURATION'

    name = fields.Char("Grading")
    no_of_sphere = fields.Integer("No.of Spheres")
    mass_charge = fields.Char("Mass of Charge,g")
