# -*- coding: utf-8 -*-
from odoo import models, fields, _


class skit_test_template(models.Model):
    _name = 'skit.test.template'

    name = fields.Char("Name")
    test_category = fields.Selection([
                                ('concrete', _('Concrete')),
                                ('steel', _('Steel')),
                                ('soil', _('Soil')),
                                ('chemical', _('Chemical'))],
                                string='Category',
                                default='concrete')
