# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, date


class SieveAnalysis(models.Model):
    _name = "skit.sieve.analysis"
    _description = " Sieve Analysis Of Soil Aggregates"

    name = fields.Char(string="Lab Result No.", readonly=True)
    sievetest_date = fields.Date(string="Date", readonly=True)
    project_id = fields.Many2one('project.project', "Project Name")
    location_id = fields.Many2one('skit.location', String="Location")
    contractor = fields.Many2one('res.partner',string="Contrator",domain="[('is_company','=',True)]")
    sample_identify = fields.Char(string="Sample Identification",
                                  default="Not Stated")
#     kind_of_material = fields.Many2one('config.material' ,string = 'Kind of Material')
    
    kind_of_material = fields.Many2one('config.material' ,string = 'Kind of Material' )  
    qty_rep = fields.Char(string="Quantity Represented", default="Not Stated")
    sample = fields.Char(string="Sampled At", default="Jobsite")
    source = fields.Char(string="Original Source", default="Not Stated")
    supplied_by = fields.Many2one('res.users', string="Supplied By")
    sample_by = fields.Many2one('res.users', string="Sampled By")
#     spec_item_no = fields.Many2one('skit.config.specitem',"Spec's Item No")
    spec_item_no = fields.Char("Spec's Item No")
    proposed = fields.Text(string="Proposed Use")
    designation_sampled = fields.Many2one('res.partner', "Designation",
                                            readonly=True)
    designation_submitted = fields.Many2one('res.partner', "Designation",
                                            readonly=True)
    date_performed = fields.Datetime(string="Date", readonly=True)
    date_submit = fields.Datetime(string="Date", readonly=True)
    submitted_by = fields.Many2one('res.users', string="Submitted By")
    state = fields.Selection([('draft', 'Draft'),
                              ('submit', 'Submit'),
                              ('confirm', 'Confirm'),
                              ('verify', 'Verify'),
                              ('approved', 'Approved'),
                              ('cancelled', 'Cancelled')], string='Status',
                             readonly=True, copy=False, index=True,
                             default='draft', track_visibility='onchange')
    weight_after_wash = fields.Integer(string="Weight After Washing")
    oven_dry_weight = fields.Integer(string="Oven Dry Weight Of Sample")
    original_weight_wet = fields.Integer("Original Weight Of Sample @ Wet")
    wash_loss = fields.Float(string="Wash Loss %",
                             compute='compute_wash_loss')
    moisture_content = fields.Float(string="Moisture Content",
                                    compute='compute_moisture_content')
    tested_by = fields.Many2one('res.users', "Tested By", readonly=True)
    witnessed_by = fields.Many2many('res.partner',string="Witnessed By",domain="[('is_company','=',False)]")
    checked_by = fields.Many2one('res.users', "Checked By", readonly=True)
    checked_date = fields.Datetime("Checked Date", readonly=True, copy=False)
    attested_by = fields.Many2one('res.users', "Attested By", readonly=True)
    tested_date = fields.Datetime("Tested Date", readonly=True, copy=False)
    sieve_line_ids = fields.One2many('skit.sieve.analysis.line', 'analysis_id')
    witnessed_date = fields.Datetime("Witnessed Date")
    attested_date = fields.Datetime("Attested Date", readonly=True, copy=False)
    task_id = fields.Integer("Task" ,compute='_compute_task_id')
    grade_check = fields.Boolean("check")
    grade = fields.Many2one("config.abrasion",String="Grade")
    
#     @api.onchange('spec_item_no')
#     def onchange_spec_item_no(self):
#          material_id = self.env['config.material'].search([('spec_item_no','=',self.spec_item_no.id)],limit=1)
#          grading = material_id.grading
#          gradeA=['Item 201','Item 202','Item 204','Item 300'] 
#          gradeB=['Item 200','Item 104']
#          spec_item =self.spec_item_no.name
#          if spec_item in gradeB :
#              grade = self.env['config.abrasion'].search([('name','=','Grade A')])
#              self.update({'kind_of_material':False})
#          elif spec_item in gradeA :
#             grade = self.env['config.abrasion'].search([('name','=','Grade A')])
#             self.update({'kind_of_material':grade.id})
#          else :
#              if spec_item:
#                  grade = self.env['config.abrasion'].search([('name','=','Grade B')])
#                  self.update({'kind_of_material':grade.id})
#          return {
#                     'domain':{
#                         'kind_of_material':[(('id','in',grading.ids))]
#                 },}  
#      
    #To set corresponding 'Task id'
    @api.depends('name')
    def _compute_task_id(self):
        for sieve in self :
            task = self.env['project.task'].search([('name','=',sieve.name)])
            sieve.update({
                'task_id' : task.id})
            
            
            
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
    def sas_action_submit(self):
        user = self.env['res.users'].browse(self.env.uid)
        if (self.submitted_by):
            self.write({'state': 'submit',
                        'tested_by': user.id,
                        'tested_date': datetime.today(),
                        'designation_submitted': self.submitted_by.partner_id.id,
                        'date_submit': datetime.today()})
        
    # Confirm Button Action
    @api.multi
    def sas_action_confirm(self):
        user = self.env['res.users'].browse(self.env.uid)
        self.write({'state': 'confirm',
                    'checked_by': user.id,
                    'checked_date': datetime.today()})

    # verify Button Action
    @api.multi
    def sas_action_verify(self):
        self.write({'state': 'verify'})

    # Approve Button Action
    @api.multi
    def sas_action_approve(self):
        user = self.env['res.users'].browse(self.env.uid)
        if not self.sievetest_date:
            self.write({'sievetest_date': date.today()})
        self.write({'state': 'approved',
                    'attested_by': user.id,
                    'attested_date': datetime.today(),
                    'sievetest_date': date.today()})

    # Confirm cancel Action
    @api.multi
    def sas_action_cancel(self):
        self.write({'state': 'cancelled'})

    # Reset Button that can only be activated when
    # approved by the Branch Lead Technician.
    # This Button will delete the results as this
    # intends to repeat the test performed.
    @api.multi
    def sas_action_reset(self):
        orders = self.filtered(lambda s: s.state in ['cancelled'])
        return orders.write({
            'state': 'draft',
        })

    # Calculate wash_loss - auto-computed
    # as (100-(weight_after_wash * oven_dry_weight/100))
    # Eg: (100-(20*30\100)) = 94)
    @api.depends('weight_after_wash', 'oven_dry_weight')
    def compute_wash_loss(self):
        for sieve in self :
            weight_after_wash = sieve.weight_after_wash
            oven_dry_weight = sieve.oven_dry_weight
            if weight_after_wash and oven_dry_weight:
                wash = (100-(sieve.weight_after_wash / sieve.oven_dry_weight*100))
                sieve.update({'wash_loss': wash,
                             })

    # Calculate moisture_content - auto-computed as
    # ((original_weight_wet - oven_dry_weight)/(original_weight_wet*100))
    # Eg: ((80-30)/(80*100)) = 0.01)
    @api.depends('original_weight_wet', 'oven_dry_weight')
    def compute_moisture_content(self):
        for sieve in self :
            original_weight_wet = sieve.original_weight_wet
            oven_dry_weight = sieve.oven_dry_weight
            if original_weight_wet and oven_dry_weight:
                moisture = ((sieve.original_weight_wet - sieve.oven_dry_weight)
                            / (sieve.original_weight_wet*100))
                sieve.update({'moisture_content': moisture,
                             })
    
    
    # auto-populated field and associated to the Sampled By field
    # date/time when the Sample was Submitted
    @api.onchange('sample_by')
    def _onchange_sampled_by(self):
        sample_by = self.sample_by
        if sample_by:
            self.designation_sampled = sample_by.partner_id.id
            self.date_performed = datetime.today()
    
    @api.onchange('submitted_by')
    def _onchange_submitted_by(self):
        submitted_by = self.submitted_by
        if submitted_by:
            self.designation_submitted = submitted_by.partner_id.id
#             self.date_submit = datetime.today()


    # To get the value of sieve_size and specification from soil
    #  aggregate specification configuration table
    @api.model
    def create(self, vals):
        item_no = vals.get('spec_item_no')
        kind_of_material = self.env['config.material'].search([('spec_item_no','=',item_no)])
        
        material = self.env['config.material'].search([('name','=',kind_of_material.name)])
        material_id = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material.id)],limit=1)
        if (vals.get('sample_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', vals['sample_by'])])
            vals['designation_sampled'] = res_user.partner_id.id
            vals['date_performed'] = datetime.today()
        result = super(SieveAnalysis, self).create(vals)
        analysis_line = self.env['skit.sieve.analysis.line']
        if material_id.grading :
            specification_ids = self.env['skit.soil.aggregate.specification'].search([('name','=',material_id.name),('grading','=',material_id.grading.id)])
             
        else:
            specification_ids = self.env['skit.soil.aggregate.specification'].search([('name','=',material_id.name)])
        if item_no :    
         
            for specific_id in specification_ids :     
                max = specific_id.max_value_range
                min = specific_id.min_value_range
                specification="-"
                if min and max :
                    specification = str(min) + "-" + str(max)
                elif max :
                    specification = str(max)
                elif min :
                    specification = str(min)
                # Create new line for Soil Analysis based on
                # Kind of Material and Specification
                analysis = analysis_line.create({
                                            'analysis_id': int(result['id']),
                                            'specification': specification,
                                            'sieve_size': specific_id.sieve_size})
        return result
 
    # write method for above create method
    @api.multi
    def write(self, values):
        item_no = values.get('spec_item_no')
        kind_of_material = self.env['config.material'].search([('spec_item_no','=',item_no)])
        material = self.env['config.material'].search([('name','=',kind_of_material.name)],limit=1)
        material_id = self.env['skit.soil.aggregate.specification'].search([('kind_of_material','=',material.id)],limit=1)
        if (values.get('sample_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', values['sample_by'])])
            values['designation_sampled'] = res_user.partner_id.id
            values['date_performed'] = datetime.today()
        result = super(SieveAnalysis, self).write(values)
        analysis_line = self.env['skit.sieve.analysis.line']
        analysislines = self.env['skit.sieve.analysis.line'].search([
                        ('analysis_id', '=', self.id)])
        if item_no :
            if analysislines:
                        # Delete Existing records
                analysislines.unlink()
        if material_id.grading :
            specification_ids = self.env['skit.soil.aggregate.specification'].search([('name','=',material_id.name),('grading','=',material_id.grading.id)])
             
        else:
            specification_ids = self.env['skit.soil.aggregate.specification'].search([('name','=',material_id.name)])
         
        for specific_id in specification_ids :    
            max = specific_id.max_value_range
            min = specific_id.min_value_range
            specification="-"
            if min == max and max :
                specification =str(max)
            elif min and max :
                specification = str(min) + "-" + str(max)
            elif max :
                specification = str(max)
            elif min :
                specification = str(min)
            # Create new line for Soil Analysis based on
            # Kind of Material and Specification
            if item_no :
                analysis = analysis_line.create({
                                    'analysis_id': self.id ,
                                    'specification': specification,
                                    'sieve_size': specific_id.sieve_size})
     
        return result


class SkitSieveAnalysisLine(models.Model):
    _name = 'skit.sieve.analysis.line'
    _description = 'Sieve Analysis Tab'

    analysis_id = fields.Many2one('skit.sieve.analysis')
    sieve_size = fields.Char(string="Sieve Size(inc)")
    wt_retained = fields.Float("Weight Retained(gms)")
    percent_of_retained = fields.Integer("% Retained",
                                       compute='compute_percent_of_retained')
    percent_of_passing = fields.Float("% Passing",
                                      compute='compute_percent_of_passing')
    specification = fields.Char("Specification")

    # Calculate percent_of_retained - auto - computed as
    # (wt_retained /oven_dry_weight*100)
    # Eg: (500/2*100) = 2.5)
    @api.depends('wt_retained', 'analysis_id.oven_dry_weight')
    def compute_percent_of_retained(self):
        for sieve in self:
            wt_retained = sieve.wt_retained
            oven = sieve.analysis_id.oven_dry_weight
            if wt_retained and oven:
                retained = (wt_retained / oven * 100)
                sieve.update({'percent_of_retained': retained})

    # Calculate percent_of_passing - auto-computed as (100-percent_of_retained)
    # Eg: (500/2*100) = 2.5)
    @api.depends('percent_of_retained')
    def compute_percent_of_passing(self):
        for values in self:
            percent_of_retained = values.percent_of_retained
            passing_percent = (100-percent_of_retained)
            values.update({'percent_of_passing': passing_percent})
