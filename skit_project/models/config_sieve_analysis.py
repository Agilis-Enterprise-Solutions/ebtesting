# -*- coding: utf-8 -*-

from odoo import fields, models,api



class SkitSoilAggregateSpecification(models.Model):
    _name = "skit.soil.aggregate.specification"
    _description = "Skit Soil Aggregate Specification"

    kind_of_material = fields.Many2one('config.material', string="Kind of material")
    grading = fields.Many2one('config.abrasion',string="Grading")
    sieve_size = fields.Char(string="Size")
    max_value_range = fields.Char(string="Max Value Range")
    min_value_range = fields.Char(string="Min Value Range")
    name = fields.Char(string="Spec's Item No.",readonly=True)
    liquid_limit = fields.Char(string="Liquid Limit")
    plasticity_index = fields.Char(string="Plasticity Index")
    abrasion = fields.Char(string="Abrasion")
    fractural_face = fields.Char(string="Fractural Face")
    cbr = fields.Char(string="CBR")
    astm = fields.Char(string = "ASTM D1633")
    
    @api.onchange('kind_of_material')
    def onchange_kind_of_material(self):
        if self.kind_of_material :
            for material in self:
                kind_of_material = material.kind_of_material
                grading = kind_of_material.grading
                material.update({ 'name' : kind_of_material.spec_item_no.name})
                return{
                        'domain':{
                            'grading':[(('id', 'in', grading.ids))],
                    },}  
    @api.model
    def create(self, vals):
        kind_of_material = vals.get('kind_of_material')
        if (vals.get('kind_of_material')):
            grading = self.env['config.material'].search([
                    ('id', '=', kind_of_material)],limit=1)
            name = grading.spec_item_no.name
            vals['name']=name
            result = super(SkitSoilAggregateSpecification, self).create(vals)
        return result
    
    @api.multi
    def write(self, vals):
        kind_of_material = vals.get('kind_of_material')
        if (vals.get('kind_of_material')):
            grading = self.env['config.material'].search([
                    ('id', '=', kind_of_material)],limit=1)
            name = grading.spec_item_no.name
            vals['name']=name
            result = super(SkitSoilAggregateSpecification, self).write(vals)
        return result

  
class SkitSoilCoarseAggregate(models.Model):
    _name = "skit.soil.coarse.fine.aggregate"

    name = fields.Many2one('config.material', string="Kind of material")
    grading = fields.Many2one('config.abrasion',string="Grading")
    sieve_size = fields.Char(string="Size")
    max_value_range = fields.Char(string="Max Value Range")
    min_value_range = fields.Char(string="Min Value Range")
    spec_item_no = fields.Char(string="Spec's Item No.")
    soundness = fields.Char(string="Soundness")
    abrasion = fields.Char(string="Abrasion")
    wash_loss = fields.Char(string = "Wash Loss")
    clay_lumps = fields.Char(string = "Clay Lumps")
    
    @api.onchange('name')
    def onchange_kind_of_material(self):
        if self.kind_of_material :
            for material in self:
                kind_of_material = material.kind_of_material
                grading = kind_of_material.grading
                material.update({ 'name' : kind_of_material.spec_item_no.name})
                return{
                        'domain':{
                            'grading':[(('id', 'in', grading.ids))],
                    },}
    