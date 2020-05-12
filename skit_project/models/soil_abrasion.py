# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, date


class SoilAbrasion(models.Model):
    _name = "skit.soil.abrasion"
    _description = "Soil Abrasion Test"

    name = fields.Char(string="Lab Result No:")
    abrasion_test_date = fields.Date("Date")
    project_id = fields.Many2one('project.project', "Project Name")
    location_id = fields.Many2one('skit.location')
    sample_identify = fields.Char(string="Sample Identification")
#     kind_of_material = fields.Many2one('config.material' ,string = 'Kind of Material')
    qty_rep = fields.Char(string="Quantity Represented")
    supplied_by = fields.Many2one('res.users', "Supplied By")
    sampled_by = fields.Many2one('res.users', "Sampled By")
    submitted_by = fields.Many2one('res.users', "Submitted By")
    contractor = fields.Many2one('res.partner',string="Contrator",domain="[('is_company','=',True)]")
    original_source = fields.Char(string="Original Source")
    supplied_at = fields.Char(string="Supplied At")
    spec_item_no = fields.Char(string="Spec's Item No.")
    proposed_use = fields.Text(string="Proposed Use")
    designation_sampled = fields.Many2one('res.partner', "Designation",
                                          readonly=True)
    designation_submitted = fields.Many2one('res.partner', "Designation",
                                            readonly=True)
    date_performed = fields.Datetime(string="Date", readonly=True)
    date_submit = fields.Datetime(string="Date", readonly=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('submit', 'Submit'),
                              ('confirm', 'Confirm'),
                              ('verify', 'Verify'),
                              ('approved', 'Approved'),
                              ('cancelled', 'Cancelled')], string='Status',
                             readonly=True, copy=False, index=True,
                             track_visibility='onchange',
                             default='draft')
    tested_by = fields.Many2one('res.users', "Tested By", readonly=True)
    tested_date = fields.Datetime("Tested Date", readonly=True, copy=False)
    checked_by = fields.Many2one('res.users', "Checked By", readonly=True)
    checked_date = fields.Datetime("Checked Date", readonly=True, copy=False)
    witnessed_by = fields.Many2many('res.partner',string="Witnessed By",domain="[('is_company','=',False)]")
    witnessed_date = fields.Datetime("Witnessed Date")
    attested_by = fields.Many2one('res.users', "Attested By", readonly=True)
    attested_date = fields.Datetime("Attested Date", readonly=True, copy=False)
    grading_use = fields.Many2one('config.abrasion', "Grading Used")
    no_of_sphere = fields.Integer("B.No.of Spheres")
    dry_wt_retained = fields.Integer("C.Dry Weight Retained on Sieve No. 12")
    dry_wt_passing = fields.Integer("D.Dry Weight Passing on Sieve No. 12")
    abrasion_loss = fields.Float("E.Abrasion Loss (%)",
                                 compute='compute_abrasion_loss')
    abrasion_line_ids = fields.One2many('skit.abrasion', 'abrasion_id',
                                        "Abrasion")
    total = fields.Float("Total", compute="compute_total_val")
    task_id = fields.Integer("Task" ,compute='compute_task_id')
    grade_check = fields.Boolean("check")
    grade = fields.Many2one("config.abrasion",String="Grade")
    
    @api.model
    def default_material(self):
       value =  self.env['config.material'].search([('name', '=', 'EMBANKMENT')], limit=1).id
       if value :
           return value
       else :
        return 
    kind_of_material = fields.Many2one('config.material' ,string = 'Kind of Material' ,default = default_material)  
    
    @api.onchange('kind_of_material')
    def onchange_kind_of_material(self):
        for material in self:
            kind_of_material = material.kind_of_material
            material.update({ 'spec_item_no' : kind_of_material.spec_item_no.name})
            grade = kind_of_material.grading
            if grade :
                material.update({'grade_check' :True})
            else:
                material.update({'grade_check' :False})
        return {
                    'domain':{
                    'grade':[(('id', 'in', grade.ids))],
               },}      
    
    #To set corresponding 'Task id'
    @api.depends('name')
    def compute_task_id(self):
        for abrasion in self :
            task = self.env['project.task'].search([('name','=',abrasion.name)])
            abrasion.update({
                'task_id' : task.id})

    # Submit Button Action
    @api.multi
    def ab_action_submit(self):
        user = self.env['res.users'].browse(self.env.uid)
        if (self.submitted_by):
            self.write({'state': 'submit',
                        'tested_by': user.id,
                        'tested_date': datetime.today(),
                        'designation_submitted': self.submitted_by.partner_id.id,
                        'date_submit': datetime.today()})

    # Confirm Button Action
    @api.multi
    def ab_action_confirm(self):
        user = self.env['res.users'].browse(self.env.uid)
        self.write({'state': 'confirm',
                    'checked_by': user.id,
                    'checked_date': datetime.today()})

    # Verify Button Action
    @api.multi
    def ab_action_verify(self):
        self.write({'state': 'verify'})

    # The Approved Button will appear when the test results were
    # verified completely
    @api.multi
    def ab_action_approve(self):
        user = self.env['res.users'].browse(self.env.uid)
        if not self.abrasion_test_date:
            self.write({'abrasion_test_date': date.today()})
        self.write({'state': 'approved',
                    'attested_by': user.id,
                    'attested_date': datetime.today(),
                    })

    # Cancelled Button Action
    @api.multi
    def ab_action_cancel(self):
        self.write({'state': 'cancelled'})

    # Reset Button that can only be activated when approved by
    # the Branch Lead Technician.
    # This Button will delete the results as this intends to
    # repeat the test performed.
    @api.multi
    def ab_action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancelled'])
        return orders.write({
            'state': 'draft',
        })

    # Abrasion Loss (%) is an auto-computed as
    # [Dry Weight Passing Sieve No. 12 / Total Weight *100]
    @api.depends('dry_wt_passing', 'total')
    def compute_abrasion_loss(self):
        for abrasion in self:
            wt_passing = abrasion.dry_wt_passing
            total = abrasion.total
            if wt_passing and total:
                abrasion_loss = (wt_passing / total * 100)
                abrasion.update({'abrasion_loss': abrasion_loss})

    # Sum of Total Weight
    @api.depends('abrasion_line_ids')
    def compute_total_val(self):
        for abrasion in self:
            total = sum([line.weight for line in abrasion.abrasion_line_ids])
            abrasion.update({'total': total})

    # Update No.of Sphere
    @api.onchange('grading_use')
    def onchange_grading_use(self):
        grading_use = self.grading_use
        grading = self.env['config.abrasion'].search([
                    ('id', '=', grading_use.id)], limit=1)
        no_of_sphere = grading.no_of_sphere
        self.update({'no_of_sphere': no_of_sphere})

    # auto-populated field and associated to the Sampled By field
    # date/time when the Sample was Submitted
    @api.onchange('sampled_by')
    def _onchange_sampled_by(self):
        sampled_by = self.sampled_by
        if sampled_by:
            self.designation_sampled = sampled_by.partner_id.id
            self.date_performed = datetime.today()

    @api.model
    def create(self, vals):
        abrasion = self.env['skit.abrasion']
        grading_used = vals.get('grading_use')
        if (vals.get('grading_use')):
            grading = self.env['config.abrasion'].search([
                    ('id', '=', grading_used)], limit=1)
            vals['no_of_sphere'] = grading.no_of_sphere
        if (vals.get('sampled_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', vals['sampled_by'])])
            vals['designation_sampled'] = res_user.partner_id.id
            vals['date_performed'] = datetime.today()
        result = super(SoilAbrasion, self).create(vals)
        if (vals.get('grading_use')):
            grading = vals['grading_use']
            config_soil = self.env['config.soil.abrasion'].search([
                                ('grading', '=', grading)])
            for config in config_soil:
                passing = config.passing
                retained_on = config.retained_on
                # Create new line for Soil Abrasion based on Grading
                abrasion_line = abrasion.create({
                            'abrasion_id': int(result['id']),
                            'passing': passing,
                            'retained': retained_on})
        return result

    @api.multi
    def write(self, values):
        grading_used = values.get('grading_use')
        if (values.get('grading_use')):
            grading = self.env['config.abrasion'].search([
                    ('id', '=', grading_used)], limit=1)
            values['no_of_sphere'] = grading.no_of_sphere
        if (values.get('sampled_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', values['sampled_by'])])
            values['designation_sampled'] = res_user.partner_id.id
            values['date_performed'] = datetime.today()
        result = super(SoilAbrasion, self).write(values)
        abrasion = self.env['skit.abrasion']
        if (values.get('grading_use')):
                grading = values['grading_use']
                config_soil = self.env['config.soil.abrasion'].search([
                                    ('grading', '=', grading)])
                abrasionlines = self.env['skit.abrasion'].search([
                                    ('abrasion_id', '=', self.id)])
                if abrasionlines:
                    # Delete Existing record
                    abrasionlines.unlink()
                for config in config_soil:
                    passing = config.name
                    retained_on = config.retained_on
                    # Create new line for Soil Abrasion based on Grading
                    abrasion_line = abrasion.create({
                            'abrasion_id': self.id,
                            'passing': passing,
                            'retained': retained_on})
        return result


class SKitAbrasion(models.Model):
    _name = "skit.abrasion"
    _description = "Abrasion Table"

    abrasion_id = fields.Many2one('skit.soil.abrasion')
    passing = fields.Char("PASSING Sieve Size")
    retained = fields.Char("RETAINED Sieve Size")
    weight = fields.Float("Weight Grams")
