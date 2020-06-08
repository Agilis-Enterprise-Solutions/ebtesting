# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, date
import json


class SoilCompaction(models.Model):
    _name = "skit.soil.compaction"
    _description = "Soil Compaction Test"

    name = fields.Char(string="Lab Result No:")
    campact_test_date = fields.Date("Date")
    project_id = fields.Many2one('project.project', "Project Name")
    location_id = fields.Many2one('skit.location')
    contractor = fields.Many2one('res.partner',string="Contrator",domain="[('is_company','=',True)]")
    sample_identify = fields.Char(string="Sample Identification")
    kind_of_material = fields.Many2one('config.material',
                                       string='Kind of Material')
    test_date = fields.Date("Date Tested")
    sampled_by = fields.Many2one('res.users', "Sampled By")
    submitted_by = fields.Many2one('res.users', "Submitted By")
    original_source = fields.Char(string="Original Source")
    tec_tested_by = fields.Many2one('res.users', "Tested By")
    spec_item_no = fields.Char(string="Spec's Item No.")
    designation_sampled = fields.Many2one('res.partner', "Designation",
                                          readonly=True)
    designation_submitted = fields.Many2one('res.partner', "Designation",
                                            readonly=True)
    date_performed = fields.Datetime(string="Date", readonly=True)
    date_submit = fields.Datetime(string="Date", readonly=True)
    aashto = fields.Char("AASHTO")
    method_used = fields.Char("Method Used")
    weight_of_rammer = fields.Char("Weight of Rammer")
    no_of_layer = fields.Integer("No of Layers")
    blow_of_layer = fields.Integer("Blows / Layers")
    weight_of_mold = fields.Float("Weight of Mold  gm")
    volume_of_mold = fields.Float("Volume of Mold  cc")
    max_dry_density = fields.Float("Maximum Dry Density gm/cc",readonly=True)
    optimum_moisture_content = fields.Float("Optimum Moisture Content %",readonly=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('submit', 'Submit'),
                              ('confirm', 'Confirm'),
                              ('verify', 'Verify'),
                              ('approved', 'Approved'),
                              ('cancelled', 'Cancelled')], string='Status',
                             readonly=True, copy=False, index=True,
                             default='draft', track_visibility='onchange')
    moisture_content_ids = fields.One2many('skit.compaction.moisture',
                                           'compaction_id',
                                           "Moisture Contents")
    density_ids = fields.One2many('skit.compaction.density',
                                  'compaction_id', "Density")
    tested_by = fields.Many2one('res.users', "Tested By", readonly=True)
    tested_date = fields.Datetime("Tested Date", readonly=True, copy=False)
    checked_by = fields.Many2one('res.users', "Checked By", readonly=True)
    checked_date = fields.Datetime("Checked Date", readonly=True, copy=False)
    witnessed_by = fields.Many2many('res.partner',string="Witnessed By",domain="[('is_company','=',False)]")
    witnessed_date = fields.Datetime("Witnessed Date")
    attested_by = fields.Many2one('res.users', "Attested By", readonly=True)
    attested_date = fields.Datetime("Attested Date", readonly=True, copy=False)
    task_id = fields.Integer("Task", compute='_compute_task_id')
    compaction_parabolic_graph = fields.Text(string="GRAPH",
                                             compute='_compaction_graph')
    grade_check = fields.Boolean("check")
    grade = fields.Many2one("config.abrasion",String="Grade")
    
    
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
    


    @api.one
    def _compaction_graph(self):
        self.compaction_parabolic_graph = json.dumps(
                                                self.get_line_graph_datas())

    @api.multi
    def get_line_graph_datas(self):
        moisture_content = []
        datas = []
        xmax = [0]
        ymin = 0
        ymax = 0
        vertical=[]
        horizontal=[]
        vertical1=[]
        value=[]
        v1_value=0
        h1_value=0
        if self.optimum_moisture_content:
            omc = "="+str(round(self.optimum_moisture_content,2))
        else:
            omc = ""
        for moisture in self.moisture_content_ids:
            moisture_content.append({
                                'key': moisture.moisture_can_no,
                                'value': round(moisture.moisture_content, 2)
                                })
        for density in self.density_ids:
            for moisture in moisture_content:
                if(density.moisture_can_no == moisture['key']):
                    datas.append({"value": density.dry_density,
                                  "labels": [moisture['value'],
                                             "Moisture Content %"+omc],
                                  "yaxis": "Dry Density(g/cc)",
                                  "moisture": moisture['value']
                                  })
                    vertical.append({'value': density.dry_density})
                    horizontal.append({'valuess':moisture['value']})
                    value.append({"value": density.dry_density,
                                  "labels": moisture['value'],
                        })
                    vertical1.append(density.dry_density)
        if len(datas) >= 1:
            ymaxval = max(datas, key=lambda x: x['value'])
            yminval = min(datas, key=lambda x: x['value'])
            ymin = yminval.get('value')
            ymax = ymaxval.get('value') + 1
            xmaxval = max(datas, key=lambda x: x['labels'])
            xmax = xmaxval.get('labels')
            
            

        
        if len(vertical1) >=2:
            vertical1.sort(reverse=True)
            value1 =vertical1[0]
            value2 = vertical1[1]
            h1_value =(value1+value2)/1.98
            
            if value1 > h1_value :
                 h1_value =value1
                
            v1=[]
           
            for x in value:
                if x['value'] == value1:
                    v1.append(x['labels'])
                   
                elif x['value']== value2:
                    v1.append(x['labels'])
                    
                      
            val1=v1[0]
            val2=v1[1] 
            v1_value =  (val1 + val2)/1.95
        dry_density=round((self.max_dry_density),2)
        self.write({'max_dry_density': h1_value,
                    'optimum_moisture_content':v1_value})
#         print(datas)
#         print(v1_value)
#         print(horizontal)
#         print(h1_value)
#         print(vertical)
        return [{'values': sorted(datas, key=lambda k: k['moisture']),
                 'y_val': [ymin, ymax],
                 'x_val': [0, xmax[0]+1],
                 'title':"Maximum Dry Density = "+str(dry_density),
                'id': self.id,
                'vertical':vertical,
                'v1_value':v1_value,
                'horizontal':horizontal,
                'h1_value':h1_value,
                }]

    # Submit Button Action
    @api.multi
    def sc_action_submit(self):
        user = self.env['res.users'].browse(self.env.uid)
        if (self.submitted_by):
            self.write({'state': 'submit',
                        'tec_tested_by': user.id,
                        'test_date': date.today(),
                        'tested_by': user.id,
                        'tested_date': datetime.today(),
                        'designation_submitted': self.submitted_by.partner_id.id,
                        'date_submit': datetime.today()
                        })

    # Confirm Button Action
    @api.multi
    def sc_action_confirm(self):
        user = self.env['res.users'].browse(self.env.uid)
        self.write({'state': 'confirm',
                    'checked_by': user.id,
                    'checked_date': datetime.today()})

    # Verify Button Action
    @api.multi
    def sc_action_verify(self):
        self.write({'state': 'verify',
                    })

    # The Approved Button will appear when the test results were
    # verified completely.
    @api.multi
    def sc_action_approve(self):
        user = self.env['res.users'].browse(self.env.uid)
        if not self.campact_test_date:
            self.write({'campact_test_date': date.today()})

        self.write({'state': 'approved',
                    'attested_by': user.id,
                    'attested_date': datetime.today(),
                    })

    # Cancelled Button Action
    @api.multi
    def sc_action_cancel(self):
        self.write({'state': 'cancelled'})

    # Reset Button that can only be activated when approved
    # by the Branch Lead Technician.
    # This Button will delete the results as this intends to repeat
    # the test performed.
    @api.multi
    def sc_action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancelled'])
        return orders.write({
            'state': 'draft',
        })

    # auto-populated field and associated to the Sampled By field
    # date/time when the Sample was Submitted
    @api.onchange('sampled_by')
    def _onchange_sampled_by(self):
        sampled_by = self.sampled_by
        self.designation_sampled = sampled_by.partner_id.id
        self.date_performed = datetime.today()

    # To set corresponding 'Task id'
    @api.depends('name')
    def _compute_task_id(self):
        for compaction in self:
            task = self.env['project.task'].search([('name', '=',
                                                     compaction.name)])
            compaction.update({
                'task_id': task.id})

    @api.model
    def create(self, vals):
        if (vals.get('sampled_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', vals['sampled_by'])])
            vals['designation_sampled'] = res_user.partner_id.id
            vals['date_performed'] = datetime.today()
        result = super(SoilCompaction, self).create(vals)
        return result

    @api.multi
    def write(self, values):
        if (values.get('sampled_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', values['sampled_by'])])
            values['designation_sampled'] = res_user.partner_id.id
            values['date_performed'] = datetime.today()
        result = super(SoilCompaction, self).write(values)
        return result


class SkitMoistureContents(models.Model):
    _name = 'skit.compaction.moisture'
    _description = "Compaction Moisture Contents"

    compaction_id = fields.Many2one('skit.soil.compaction')
    determination_no = fields.Integer("Determination No",
                                      compute="_compute_get_number")
    moisture_can_no = fields.Char("Moisture Can No")
    wt_of_can_wetsoil = fields.Float("Wt.of Can + Wet Soil")
    wt_of_can_drysoil = fields.Float("Wt.of Can + Dry Soil")
    wt_of_water = fields.Float("Weight of Water",
                               compute="compute_weight_of_water")
    wt_of_can = fields.Float("Wt.of Can")
    wt_of_drysoil = fields.Float("Wt.of Dry Soil",
                                 compute="compute_weight_drysoil")
    moisture_content = fields.Float("Moisture Content",
                                    compute="compute_moisture_content")

    # Calculate Weight_of_water - auto-computed as
    # (wt_of_can_wetsoil - wt_of_can_drysoil)
    # Eg: (262-250 = 12)
    @api.depends('wt_of_can_wetsoil', 'wt_of_can_drysoil')
    def compute_weight_of_water(self):
        for moisture in self:
            wet_soil = moisture.wt_of_can_wetsoil
            dry_soil = moisture.wt_of_can_drysoil
            wt_of_water = (wet_soil - dry_soil)
            moisture.update({'wt_of_water': wt_of_water})

    # Calculate wt_of_drysoil - auto-computed as (wt_of_can_drysoil -wt_of_can)
    # Eg: (250 -20.50 = 229.50)
    @api.depends('wt_of_can', 'wt_of_can_drysoil')
    def compute_weight_drysoil(self):
        for drysoil in self:
            dry_soil = drysoil.wt_of_can_drysoil
            wt_of_can = drysoil.wt_of_can
            wt_of_drysoil = (dry_soil - wt_of_can)
            drysoil.update({'wt_of_drysoil': wt_of_drysoil})

    # Calculate moisture_content - auto-computed as
    # (Weight of Water / Weight of Dry Soil * 100)
    # Eg: (12 / 229.50 * 100 = 5.2)
    @api.depends('wt_of_water', 'wt_of_drysoil')
    def compute_moisture_content(self):
        for moisture_content in self:
            water = moisture_content.wt_of_water
            drysoil = moisture_content.wt_of_drysoil
            if water and drysoil:
                moisture_cont = (water/drysoil*100)
                moisture_content.update({'moisture_content': moisture_cont})

    # Compute line no
    @api.depends('compaction_id')
    def _compute_get_number(self):
        for moisture in self.mapped('compaction_id'):
            determination_no = 1
            for line in moisture.moisture_content_ids:
                line.determination_no = determination_no
                determination_no += 1


class SkitDensity(models.Model):
    _name = 'skit.compaction.density'
    _description = 'Compaction Density'

    compaction_id = fields.Many2one('skit.soil.compaction')
    determination_no = fields.Integer("Determination No",
                                      compute="_compute_get_number")
    moisture_can_no = fields.Char("Moisture Can No")
    wt_of_mold_soil = fields.Float("Wt.of Mold + Soil")
    wt_of_mold = fields.Float("Wt.of Mold", compute='compute_wt_of_mold',
                              readonly=1)
    wt_of_compactsoil = fields.Float("Wt.of Compacted Soil",
                                     compute="compute_weight_of_compactsoil")
    wet_density = fields.Float("Wet Density", compute="compute_wet_density",
                               digits=(12, 3))
    dry_density = fields.Float("Dry Density", compute="compute_dry_density",
                               digits=(12, 3))

    @api.depends('compaction_id.weight_of_mold')
    def compute_wt_of_mold(self):
        for density in self:
            weight = density.compaction_id.weight_of_mold
            density.update({'wt_of_mold': weight})

    # Compute line no
    @api.depends('compaction_id')
    def _compute_get_number(self):
        for density in self.mapped('compaction_id'):
            determination_no = 1
            for line in density.density_ids:
                line.determination_no = determination_no
                determination_no += 1

    # Calculate wt_of_compactsoil - auto-computed as
    # (wt_of_mold_soil - wt_of_mold)
    # Eg: (4990 -3136.50 = 1853.50)
    @api.depends('wt_of_mold_soil', 'wt_of_mold')
    def compute_weight_of_compactsoil(self):
        for density in self:
            wt_of_mold_soil = density.wt_of_mold_soil
            wt_of_mold = density.wt_of_mold
            wt_of_compactsoil = (wt_of_mold_soil - wt_of_mold)
            density.update({'wt_of_compactsoil': wt_of_compactsoil})

    # Calculate wet density - auto-computed as
    # (Wt. of Compacted Soil) / (Volume of Mold) [from Test Summary].
    # Eg: (1853.50 / 902.84 = 2.05)
    @api.depends('wt_of_compactsoil', 'compaction_id.volume_of_mold')
    def compute_wet_density(self):
        for density in self:
            compactsoil = density.wt_of_compactsoil
            mold = density.compaction_id.volume_of_mold
            if compactsoil and mold:
                wet_density = (compactsoil/mold)
                density.update({'wet_density': wet_density})

    # Calculate dry density-auto computed as
    # (Wet Density)/(Moisture Content/100 +1)
    # Eg: (2.05 / (5.23/100+1) = 1.95)
    @api.depends('wet_density', 'compaction_id.moisture_content_ids')
    def compute_dry_density(self):
        for density in self:
            wetdensity = density.wet_density
            density_can_no = density.moisture_can_no
            moisture_content = 0
            val = 0
            for moiturecontent in density.compaction_id.moisture_content_ids:
                if val == 0:
                    if density_can_no == moiturecontent.moisture_can_no:
                        moisture_content = moiturecontent.moisture_content
                        val = 1
            if moisture_content > 0 and wetdensity:
                mois_con = (moisture_content / 100 + 1)
                dry_density = (wetdensity/mois_con)
                density.update({'dry_density': round(dry_density, 3)})
