# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime,date



class SoilAggregate(models.Model):
    _name = "skit.soil.aggregate"
    _description = "Soil Aggregate Test"

    name = fields.Char(string="Lab Result No.", readonly=True)
    date_labtest = fields.Date(string="Date", readonly=True)
    project_id = fields.Many2one('project.project', "Project Name")
    location_id = fields.Many2one('skit.location', String="Location")
#     contractor = fields.Many2one('res.users', string="Contractor")
    contractor = fields.Many2one('res.partner',string="Contrator",domain="[('is_company','=',True)]")
    sample_identify = fields.Char(string="Sample Identification",
                                  default="Not Stated")
    kind_of_material = fields.Many2one('config.material' ,string = 'Kind of Material')
    qty_rep = fields.Char(string="Quantity Represented", default="Not Stated")
    sample = fields.Char(string="Sampled At", default="Jobsite")
    source = fields.Char(string="Original Source", default="Not Stated")
    supplied_by = fields.Many2one('res.users', string="Supplied By")
    sample_by = fields.Many2one('res.users', string="Sampled By")
#     spec_item_no = fields.Many2one('skit.soil.aggregate.specification',string="Spec's Item No.",  domain="[('kind_of_material', '=', kind_of_material)]")
    spec_item_no = fields.Char("Spec's Item No.")
    proposed = fields.Text(string="Proposed Use")
    designation_sampled = fields.Many2one('res.partner', "Designation",
                                          readonly=True)
    designation_submitted = fields.Many2one('res.partner', "Designation",
                                          readonly=True)
    grade_check = fields.Boolean("check")
    grade = fields.Many2one("config.abrasion",String="Grade")
    date_performed = fields.Datetime(string="Date", readonly=True)
    date_submit = fields.Datetime(string="Date", readonly=True)
    submitted_by = fields.Many2one('res.users', string="Submitted By")
    # line fields test summary
    lab_result = fields.Char(string=" Related Lab Result", readonly=True)
#     lab_number = fields.Char(string="Laboratory Number", readonly=True)
    sieve_analysis = fields.Char(string="Sieve Analysis" ,compute='compute_sieve_no')
    soil_consistency = fields.Char(string="Soil Consistency" ,compute='compute_consistency_no')
    soil_abrasion = fields.Char(string="Soil Abrasion"  ,compute='compute_abrasion_no')
    soil_compaction = fields.Char(string="Soil Compaction"  ,compute='compute_compaction_no')
    soil_penetration = fields.Char(string="Soil Penetration"  ,compute='compute_penetration_no')
    remarks = fields.Text(string="Remarks")
    tested_by = fields.Many2one('res.users', "Tested By", readonly=True)
#     witnessed_by = fields.Many2one('res.users', "Witnessed By")
    witnessed_by = fields.Many2many('res.partner',string="Witnessed By",domain="[('is_company','=',False)]")
    checked_by = fields.Many2one('res.users', "Checked By", readonly=True)
    checked_date = fields.Datetime("Checked Date", readonly=True, copy=False)
    attested_by = fields.Many2one('res.users', "Attested By", readonly=True)
    tested_date = fields.Datetime("Tested Date", readonly=True, copy=False)
    witnessed_date = fields.Datetime("Witnessed Date")
    attested_date = fields.Datetime("Attested Date", readonly=True, copy=False)
    state = fields.Selection([('draft', 'Draft'),
                              ('submit', 'Submit'),
                              ('confirm', 'Confirm'),
                              ('verify', 'Verify'),
                              ('approved', 'Approved'),
                              ('cancelled', 'Cancelled')], string='Status',
                             readonly=True, copy=False, index=True,
                             track_visibility='onchange')
    sieve_lab_no=fields.Many2one('skit.sieve.analysis','Lab Result Number')
    consistency_lab_no=fields.Many2one('skit.soil.consistency','Lab Result Number')
    compaction_lab_no=fields.Many2one('skit.soil.compaction','Lab Result Number')
    penetration_lab_no=fields.Many2one('skit.soil.penetration','Lab Result Number')
    abrasion_lab_no=fields.Many2one('skit.soil.abrasion','Lab Result Number')
    sieve_tab_ids = fields.One2many('sieve.analysis.tab', 'aggregate_id')
    consistency_tab_ids = fields.One2many('soil.consistency.tab', 'aggregate_id')
    compaction_tab_ids = fields.One2many('soil.compaction.tab', 'aggregate_id')
    penetration_tab_ids = fields.One2many('soil.penetration.tab', 'aggregate_id')
    abrasion_tab_ids = fields.One2many('soil.abrasion.tab', 'aggregate_id')
    
    
    @api.onchange('kind_of_material')
    def onchange_kind_of_material(self):
        for material in self:
            kind_of_material = material.kind_of_material
            material.update({ 'spec_item_no' : kind_of_material.spec_item_no.name})
            grade = kind_of_material.grading
            if grade :
                material.update({'grade_check' :True})
            else :
                material.update({'grade_check':False})
        return {
                    'domain':{
                    'grade':[(('id', 'in', grade.ids))],
               },}      
    
    # Submit Button Action
    @api.multi
    def sa_action_submit(self):
        user = self.env['res.users'].browse(self.env.uid)
        if (self.submitted_by):
            self.write({'state': 'submit',
                        'tested_by': user.id,
                        'tested_date': datetime.today(),
                        'designation_submitted': self.submitted_by.partner_id.id,
                        'date_submit': datetime.today()})
    # Confirm Button Action
    @api.multi
    def sa_action_confirm(self):
        user = self.env['res.users'].browse(self.env.uid)
        self.write({'state': 'confirm',
                    'checked_by': user.id,
                    'checked_date': datetime.today()})

    # Verify Button Action
    @api.multi
    def sa_action_verify(self):
        self.write({'state': 'verify'})

    # Approve Button Action
    @api.multi
    def sa_action_approve(self):
        user = self.env['res.users'].browse(self.env.uid)
        if not self.date_labtest:
            self.write({'date_labtest': date.today()})
        self.write({'state': 'approved',
                    'attested_by': user.id,
                    'attested_date': datetime.today(),
                    'sievetest_date': date.today()})


    # Cancel Button Action
    @api.multi
    def sa_action_cancel(self):
        self.write({'state': 'cancelled'})

    # Reset Button that can only be activated when approved by
    # the Branch Lead Technician.
    # This Button will delete the results as this intends
    # to repeat the test performed.
    @api.multi
    def sa_action_reset(self):
        orders = self.filtered(lambda s: s.state in ['cancelled'])
        return orders.write({
            'state': 'draft',
       })
        
    @api.onchange('sample_by')
    def _onchange_sample_by(self):
        sample_by = self.sample_by
        if sample_by :
            self.designation_sampled = sample_by.partner_id.id
            self.date_performed = datetime.today()

    @api.depends('sieve_lab_no')
    def compute_sieve_no(self):
        for aggregate in self :
            lab_id = aggregate.sieve_lab_no
            aggregate.update({
                'sieve_analysis' : lab_id.name
                })
        
    @api.depends('consistency_lab_no')
    def compute_consistency_no(self):
        for aggregate in self :
            lab_id = aggregate.consistency_lab_no
            aggregate.update({
                'soil_consistency' : lab_id.name
                })
        
    @api.depends('compaction_lab_no')
    def compute_compaction_no(self):
        for aggregate in self :
            lab_id = aggregate.compaction_lab_no
            aggregate.update({
                'soil_compaction' : lab_id.name
                })
        
    @api.depends('abrasion_lab_no')
    def compute_abrasion_no(self):
        for aggregate in self :
            lab_id = aggregate.abrasion_lab_no
            aggregate.update({
                'soil_abrasion' : lab_id.name
                })
    
    @api.depends('penetration_lab_no')
    def compute_penetration_no(self):
        for aggregate in self :
            lab_id = aggregate.penetration_lab_no
            aggregate.update({
                'soil_penetration' : lab_id.name
                })
    @api.model
    def create(self,vals):

        vals['state'] = "draft"
        material_id = (vals.get('kind_of_material'))
        material = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material_id)],limit=1)
        if material.grading :
            material_max_min_ids = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material_id),('grading','=',material.grading.id)])
        else :
            material_max_min_ids = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material_id)])
        liquid_req = material.liquid_limit or '-'
        plastic_req = material.plasticity_index or '-'
        abrasion_req = material.abrasion or '-'
        cbr_req = material.cbr or '-'
        specifications=[]
        for max_min_id in material_max_min_ids:
            max = max_min_id.max_value_range
            min = max_min_id.min_value_range
            specification="-"
            if min == max and max  :
                specification =str(max)
            elif min and max :
                specification = str(min) + "-" + str(max)
            elif max :
                specification = str(max)
            elif min :
                specification = str(min)
            specifications.append(specification)
        lab_id = vals.get('sieve_lab_no')
        if lab_id :
            sieve_id = self.env['skit.sieve.analysis'].search([('id','=',lab_id)])
            item = self.env['skit.sieve.analysis.line'].search([('analysis_id','=',sieve_id.id)])
            sieve = self.env['sieve.analysis.tab'].search([('aggregate_id','=',self.id)])
        compaction_id = vals.get('compaction_lab_no')
        compaction = self.env['skit.soil.compaction'].search([('id','=',compaction_id)])
        max_dry = compaction.max_dry_density
        moisture = compaction.optimum_moisture_content
        compaction_tab = self.env['soil.compaction.tab']
        abrasion_id = vals.get('abrasion_lab_no')
        abrasion = self.env['skit.soil.abrasion'].search([('id','=',abrasion_id)])
        loss= abrasion.abrasion_loss
        abrasion_label = 'Abrasion Loss (%)'
        abrasion_tab = self.env['soil.abrasion.tab']
        compaction_label = ['Maximum Dry Density gm/cc','Optimum Moisture Content %']
        consistency_id = vals.get('consistency_lab_no')
        consistency = self.env['skit.soil.consistency'].search([('id', '=',consistency_id)])
        liquid = consistency.liquid_limit
        plastic = consistency.plastic_limit 
        consistency_tab=self.env['soil.consistency.tab']
        consistency_label = ['Liquid Limit (LL)','Plastic Limit (PL)']
        penetration_id = vals.get('penetration_lab_no')
        penetration = self.env['skit.soil.penetration'].search([('id','=',penetration_id)])
        penetration_tab = self.env['soil.penetration.tab']
        cbr = penetration.cbr_100_per
        swell = penetration.swell
        cbr_label = ['CBR Value (%)','Swell (%)']
        
        if (vals.get('sample_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', vals['sample_by'])])
            vals['designation_sampled'] = res_user.partner_id.id
            vals['date_performed'] = datetime.today()
        result = super(SoilAggregate, self).create(vals)
        n=0
        if lab_id :
            for line in item :
               sieve.create({    
                               'aggregate_id':int(result['id']),
                               'grading': line.sieve_size,
                             'requirement':specifications[n] ,
                             'result': line.percent_of_passing 
                               })
               n=n+1
        
        for value in compaction_label :
            if max_dry and moisture :
                if value =='Maximum Dry Density gm/cc':
                    compaction_tab.create({
                        'aggregate_id' :int(result['id']),
                        'grading' :value,
                        'requirement' :'-',
                        'result' :max_dry
                        })
                else :
                    compaction_tab.create({
                        'aggregate_id':int(result['id']),
                        'grading':value,
                        'requirement' :'-',
                        'result' :moisture
                        })
             
        for id in abrasion :
            if loss:
                abrasion_tab.create({
                'aggregate_id': int(result['id']),
                'grading':abrasion_label,
                 'requirement':abrasion_req,
                'result': loss 
                })
        
        for value in consistency_label :
            if liquid and plastic:
                if value == 'Liquid Limit (LL)' :
                    consistency_tab.create({ 
                       'aggregate_id' : int(result['id']),
                       'grading':value,
                       'requirement' :liquid_req,
                       'result' : liquid 
                       })
                else:
                   consistency_tab.create({ 
                       'aggregate_id' : int(result['id']),
                       'grading':value,
                       'requirement' :plastic_req,
                       'result' : plastic 
                       })
                   
        for value in cbr_label :
            if cbr and swell :
                if value =='CBR Value (%)' :
                    penetration_tab.create({
                        'aggregate_id' : int(result['id']),
                        'grading' : value,
                        'requirement' : cbr_req,
                        'result' : cbr
                        })
                else :
                    penetration_tab.create({
                        'aggregate_id' : int(result['id']),
                        'grading': value,
                        'requirement' :'-',
                        'result' : swell
                        })
        return result 
        
    @api.multi
    def write(self,value):
        
        material_id = (value.get('kind_of_material')) or self.kind_of_material.id
        material = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material_id)],limit=1)
        liquid_req = material.liquid_limit or '-'
        plastic_req = material.plasticity_index or '-'
        abrasion_req = material.abrasion or '-'
        cbr_req = material.cbr or '-'
        material_max_min_ids = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material_id)])
        if material.grading :
            material_max_min_ids = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material_id),('grading','=',material.grading.id)])
        else :
            material_max_min_ids = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material_id)])
        specifications=[]
        for max_min_id in material_max_min_ids:
            max = max_min_id.max_value_range
            min = max_min_id.min_value_range
            specification="-"
            if min == max and max  :
                specification =str(max)
            elif min and max :
                specification = str(max) + "-" + str(min)
            elif max :
                specification = str(max)
            elif min :
                specification = str(min)
            specifications.append(specification)
        
        lab_id = value.get('sieve_lab_no') or self.sieve_lab_no.id
        sieve_id = self.env['skit.sieve.analysis'].search([('id','=',lab_id)])
        item = self.env['skit.sieve.analysis.line'].search([('analysis_id','=',sieve_id.id)])
        sieve = self.env['sieve.analysis.tab']
        sieve_line = self.env['sieve.analysis.tab'].search([('aggregate_id','=',self.id)])
        compaction_id = value.get('compaction_lab_no') or self.compaction_lab_no.id
        compaction = self.env['skit.soil.compaction'].search([('id','=',compaction_id)])
        max_dry = compaction.max_dry_density
        moisture = compaction.optimum_moisture_content
        compaction_tab = self.env['soil.compaction.tab']
        compaction_link = self.env['soil.compaction.tab'].search([('aggregate_id','=',self.id)])
        compaction_label = ['Maximum Dry Density gm/cc','Optimum Moisture Content %']
        abrasion_id = value.get('abrasion_lab_no') or self.abrasion_lab_no.id
        abrasion = self.env['skit.soil.abrasion'].search([('id','=',abrasion_id)])
        loss = abrasion.abrasion_loss
        abrasion_label = 'Abrasion Loss (%)'
        abrasion_tab = self.env['soil.abrasion.tab']
        abrasion_link = self.env['soil.abrasion.tab'].search([('aggregate_id','=',self.id)])
        consistency_id = value.get('consistency_lab_no') or self.consistency_lab_no.id
        consistency = self.env['skit.soil.consistency'].search([('id', '=',consistency_id)])
        liquid = consistency.liquid_limit
        plastic = consistency.plastic_limit 
        consistency_tab = self.env['soil.consistency.tab']
        consistency_link = self.env['soil.consistency.tab'].search([('aggregate_id','=',self.id)])
        consistency_label = ['Liquid Limit (LL)','Plastic Limit (PL)']
        penetration_id = value.get('penetration_lab_no') or self.penetration_lab_no.id
        penetration = self.env['skit.soil.penetration'].search([('id','=',penetration_id)])
        penetration_tab = self.env['soil.penetration.tab']
        penetration_link = self.env['soil.penetration.tab'].search([('aggregate_id','=',self.id)])
        cbr = penetration.cbr_100_per
        swell = penetration.swell
        cbr_label = ['CBR Value (%)','Swell (%)']
        
        if (value.get('sample_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', value['sample_by'])])
            value['designation_sampled'] = res_user.partner_id.id
            value['date_performed'] = datetime.today()
            
        result = super(SoilAggregate, self).write(value)
        n=0
        if specifications :
            if sieve_line:
                        sieve_line.unlink()
                       
            for line in item:
                 grading=line.sieve_size
                 require=line.specification
                 result=line.percent_of_passing
                 sieve.create({    
                                 'aggregate_id':self.id,
                                 'grading': grading,
                                 'requirement': specifications[n],
                                 'result': result
                                 })
                 n=n+1
        if compaction_id :
            if compaction_link :
                compaction_link.unlink()
            if max_dry and moisture :
                for value in compaction_label :
                     if value == 'Maximum Dry Density gm/cc':
                         compaction_tab.create({
                             'aggregate_id' :self.id,
                             'grading' :value,
                             'requirement':'-',
                             'result' :max_dry
                             })
                     else :
                         compaction_tab.create({
                             'aggregate_id':self.id,
                             'grading':value,
                             'requirement':'-',
                             'result' :moisture
                             })
        if abrasion_id:
            if abrasion_link :
                abrasion_link.unlink()
            if loss:
                abrasion_tab.create({
                    'aggregate_id':self.id,
                     'grading': abrasion_label,
                     'requirement' :abrasion_req,
                     'result': loss 
                     })
                
        if consistency_id :        
            if consistency_link :
                consistency_link.unlink()
            if liquid and plastic:
                for value in consistency_label :
                     if value == 'Liquid Limit (LL)' :
                         consistency_tab.create({ 
                            'aggregate_id' :self.id,
                            'grading':value,
                            'requirement':liquid_req,
                            'result' : liquid })
                     else:
                        consistency_tab.create({ 
                            'aggregate_id' :self.id,
                            'grading':value,
                            'requirement' :plastic_req,
                            'result' : plastic })
                        
        if penetration_id :
            if penetration_link :
                penetration_link.unlink()
            if cbr and swell :
                for value in cbr_label :
                    if value =='CBR Value (%)' :
                        penetration_tab.create({
                            'aggregate_id' : self.id,
                            'grading' : value,
                            'requirement':cbr_req,
                            'result' : cbr
                            })
                    else :
                        penetration_tab.create({
                            'aggregate_id' : self.id,
                            'grading': value,
                            'requirement':'-',
                            'result' : swell
                            })
            
        return result
    
    
class SieveAnalysisTab(models.Model):
    _name = "sieve.analysis.tab"
    _description = "Sieve Analysis Tab" 
    
    aggregate_id = fields.Many2one('skit.soil.aggregate')
    grading = fields.Char("Grading")
    requirement = fields.Char("Requirement")
    result = fields.Float("Result")
    
class SoilConsistency(models.Model):
    _name = "soil.consistency.tab"
    _description = "Soil Consistency Tab"
    
    aggregate_id = fields.Many2one('skit.soil.aggregate',string="Consistency")
    grading = fields.Char("Grading")
    requirement = fields.Char("Requirement")
    result = fields.Char("Result")
    
class SoilCompaction(models.Model):
    _name = "soil.compaction.tab"
    _description = "Soil Compaction Tab"
    
    aggregate_id = fields.Many2one('skit.soil.aggregate')
    grading = fields.Char("Grading")
    requirement = fields.Char("Requirement")
    result = fields.Char("Result")
    
class SoilPenetration(models.Model):
    _name = "soil.penetration.tab"
    _description = "Soil Penetration Tab"
    
    aggregate_id = fields.Many2one('skit.soil.aggregate')
    grading = fields.Char("Grading")
    requirement = fields.Char("Requirement")
    result = fields.Char("Result")
    
    
class SoilAbrasion(models.Model):
    _name = "soil.abrasion.tab"
    _description = "Soil Abrasion Tab"
    
    aggregate_id = fields.Many2one('skit.soil.aggregate')
    grading = fields.Char("Grading")
    requirement = fields.Char("Requirement")
    result = fields.Float("Result")
#         