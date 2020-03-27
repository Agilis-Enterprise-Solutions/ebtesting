# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, date
import json


class SoilCompaction(models.Model):
    _name = "skit.soil.consistency"
    _description = "Soil Consistency Test"

    name = fields.Char(string="Lab Result No:")
    consistency_test_date = fields.Date("Date")
    project_id = fields.Many2one('project.project', "Project Name")
    location_id = fields.Many2one('skit.location')
    sample_identify = fields.Char(string="Sample Identification")
    qty_rep = fields.Char(string="Quantity Represented")
    supplied_by = fields.Many2one('res.users', "Supplied By")
    sampled_by = fields.Many2one('res.users', "Sampled By")
    submitted_by = fields.Many2one('res.users', "Submitted By")
    contractor = fields.Many2one('res.users', string="Contractor")
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
                             track_visibility='onchange', default='draft')
    liquid_limit = fields.Float('Liquid Limit (LL)')
    plastic_limit = fields.Float('Plastic Limit (PL)', default=25)
    plasticity_index = fields.Float('Plasticity Index (PI)',
                                    compute="compute_plasticity_index")
    tested_by = fields.Many2one('res.users', "Tested By", readonly=True)
    tested_date = fields.Datetime("Tested Date", readonly=True, copy=False)
    checked_by = fields.Many2one('res.users', "Checked By", readonly=True)
    checked_date = fields.Datetime("Checked Date", readonly=True, copy=False)
    witnessed_by = fields.Many2one('res.users', "Witnessed By")
    witnessed_date = fields.Datetime("Witnessed Date")
    attested_by = fields.Many2one('res.users', "Attested By", readonly=True)
    attested_date = fields.Datetime("Attested Date", readonly=True, copy=False)
    plastic_limit_ids = fields.One2many('skit.plastic.limit', 'consistency_id',
                                        "Plastic limit Ids")
    liquid_limit_ids = fields.One2many('skit.liquid.limit',
                                       'consistency_id', "Liquid limit Ids")
    avg_plastic_limit = fields.Float("Average Plastic Limit",
                                     compute="compute_avg_plastic_limit")
    task_id = fields.Integer("Task", compute='_compute_task_id')
    consistency_line_graph = fields.Text(compute='_consistency_line_graph')

    @api.model
    def default_material(self):
        value = self.env['config.material'].search([
                    ('name', '=', 'EMBANKMENT')], limit=1).id
        if value:
            return value
        else:
            return
    kind_of_material = fields.Many2one('config.material',
                                       string='Kind of Material',
                                       default=default_material)
    @api.onchange('kind_of_material')
    def onchange_kind_of_material(self):
        for material in self:
            kind_of_material = material.kind_of_material
            material.update({ 'spec_item_no' : kind_of_material.spec_item_no.name})

    @api.one
    def _consistency_line_graph(self):
        self.consistency_line_graph = json.dumps(self.get_line_graph_datas())

    @api.multi
    def get_line_graph_datas(self):
        datas = []
        xmin = [0]
        xmax = [0]
        ymin = 0
        ymax = 0
        for liquid in self.liquid_limit_ids:
            datas.append({"value": round(liquid.moisture_content, 2),
                          "labels": [liquid.no_of_blow, "No.of Blows"],
                          "yaxis": "Percent Moisture",
                          "no_of_blow": liquid.no_of_blow})
        if len(datas) >= 1:
            ymaxval = max(datas, key=lambda x: x['value'])
            yminval = min(datas, key=lambda x: x['value'])
            ymin = yminval.get('value')
            ymax = ymaxval.get('value') + 1

            xmaxval = max(datas, key=lambda x: x['labels'])
            xminval = min(datas, key=lambda x: x['labels'])
            xmin = xminval.get('labels')
            xmax = xmaxval.get('labels')
        return [{'values': sorted(datas, key=lambda k: k['no_of_blow']),
                 'y_val': [ymin, ymax],
                 'x_val': [xmin[0], xmax[0]+1],
                 'title': "",
                 'id': self.id}]

    @api.depends('name')
    def _compute_task_id(self):
        for consistency in self:
            task = self.env['project.task'].search([
                                    ('name', '=', consistency.name)])
            consistency.update({'task_id': task.id})

    # Calculate Plasticity Index - auto-computed as
    # (Liquid Limit (LL) - Plastic Limit (PL).)
    # Eg: (40 - 25 = 15)
    @api.depends('liquid_limit', 'plastic_limit')
    def compute_plasticity_index(self):
        for consistency in self:
            liquid_limit = consistency.liquid_limit
            plastic_limit = consistency.plastic_limit
            plasticity_index = (liquid_limit - plastic_limit)
            consistency.update({'plasticity_index': plasticity_index})

    # Calculate  Average Plastic Limit - auto-computed as
    # (% Moisture 1 + % Moisture 2) / 2.
    # (47.62 + 29.62) / 2 = 38.62
    @api.depends('plastic_limit_ids')
    def compute_avg_plastic_limit(self):
        len = 0
        plastic_limit = 0
        for consistency in self:
            for limit in consistency.plastic_limit_ids:
                plastic_limit += limit.moisture_content
                len += 1
            if len >= 1:
                avg_plastic = (plastic_limit / len)
                consistency.update({'avg_plastic_limit': avg_plastic})

    # Submit Button Action
    @api.multi
    def consis_action_submit(self):
        user = self.env['res.users'].browse(self.env.uid)
        if (self.submitted_by):
            self.write({'state': 'submit',
                        'tested_by': user.id,
                        'tested_date': datetime.today(),
                        'designation_submitted': self.submitted_by.partner_id.id,
                        'date_submit': datetime.today()})

    # Confirm Button Action
    @api.multi
    def consis_action_confirm(self):
        user = self.env['res.users'].browse(self.env.uid)
        self.write({'state': 'confirm',
                    'checked_by': user.id,
                    'checked_date': datetime.today()})

    # Verify Button Action
    @api.multi
    def consis_action_verify(self):
        self.write({'state': 'verify',
                    })

    # The Approved Button will appear when the test results
    # were verified completely
    @api.multi
    def consis_action_approve(self):
        user = self.env['res.users'].browse(self.env.uid)
        if not self.consistency_test_date:
            self.write({'consistency_test_date': date.today()})
        self.write({'state': 'approved',
                    'attested_by': user.id,
                    'attested_date': datetime.today(),
                    })

    # Cancelled Button Action
    @api.multi
    def consis_action_cancel(self):
        self.write({'state': 'cancelled'})

    # Reset Button that can only be activated when approved by
    # the Branch Lead Technician.
    # This Button will delete the results as this intends
    # to repeat the test performed.
    @api.multi
    def consis_action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancelled'])
        return orders.write({
            'state': 'draft',
        })

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


class PlasticLimit(models.Model):
    _name = 'skit.plastic.limit'
    _description = 'Plastic Limit'

    consistency_id = fields.Many2one('skit.soil.consistency', 'Consistency')
    trial_no = fields.Integer('TRIAL NO', compute="_compute_get_trial_number")
    dish_no = fields.Char("DISH NO")
    wt_of_dish_wetsoil = fields.Float("Weight of Dish + Wet Soil")
    wt_of_dish_drysoil = fields.Float("Weight of Dish + Dry Soil")
    wt_of_dish = fields.Float("Weight of Dish")
    wt_of_water = fields.Float("Weight of Water (1-2)",
                               compute="compute_wt_of_water")
    wt_of_drysoil = fields.Float("Weight of Dry Soil",
                                 compute="compute_wt_of_drysoil")
    moisture_content = fields.Float("% Moisture(4/5 x 100)",
                                    compute="compute_moisture_percentage")

    # Compute line no
    @api.depends('consistency_id')
    def _compute_get_trial_number(self):
        for plastic in self.mapped('consistency_id'):
            trial_no = 1
            for line in plastic.plastic_limit_ids:
                line.trial_no = trial_no
                trial_no += 1

    # Calculate Weight of water - auto-computed as
    # (Weight of Dish + Wet Soil) � (Weight of Dish + Dry Soil)
    # Eg:(22.16 - 17.85 = 4.31)
    @api.depends('wt_of_dish_wetsoil', 'wt_of_dish_drysoil')
    def compute_wt_of_water(self):
        for plastic in self:
            wet_soil = plastic.wt_of_dish_wetsoil
            dry_soil = plastic.wt_of_dish_drysoil
            wt_of_water = (wet_soil - dry_soil)
            plastic.update({'wt_of_water': wt_of_water})

    # Calculate Weight of Dry Soil - auto-computed as
    # (Weight of Dish + Dry Soil) � (Weight of Dish)
    # Eg : (17.85 - 8.80 = 9.05)
    @api.depends('wt_of_dish_drysoil', 'wt_of_dish')
    def compute_wt_of_drysoil(self):
        for plastic in self:
            dry_soil = plastic.wt_of_dish_drysoil
            wt_of_dish = plastic.wt_of_dish
            wt_of_dry_soil = (dry_soil - wt_of_dish)
            plastic.update({'wt_of_drysoil': wt_of_dry_soil})

    # Calculate  % Moisture (4/5 x 100) - auto-computed as
    # (Weight of Water / Weight of Dry Soil) * 100
    # Eg: (4.31 / 9.05 ) * 100 = 47.62
    @api.depends('wt_of_water', 'wt_of_drysoil')
    def compute_moisture_percentage(self):
        for plastic in self:
            wt_of_water = plastic.wt_of_water
            wt_of_drysoil = plastic.wt_of_drysoil
            if wt_of_water and wt_of_drysoil:
                moisture = (wt_of_water / wt_of_drysoil)
                moisture_content = (moisture * 100)
                plastic.update({'moisture_content': moisture_content})


class LiquidLimit(models.Model):
    _name = 'skit.liquid.limit'
    _description = 'Liquid Limit'

    consistency_id = fields.Many2one('skit.soil.consistency', 'Consistency')
    trial_no = fields.Integer('TRIAL NO', compute="_compute_get_trial_number")
    dish_no = fields.Char("DISH NO")
    no_of_blow_req = fields.Char("No. of Blows Required")
    no_of_blow = fields.Integer("No. of Blows")
    wt_of_dish_wetsoil = fields.Float("Weight of Dish + Wet Soil")
    wt_of_dish_drysoil = fields.Float("Weight of Dish + Dry Soil")
    wt_of_dish = fields.Float("Weight of Dish")
    wt_of_water = fields.Float("Weight of Water (1-2)",
                               compute="compute_wt_of_water")
    wt_of_drysoil = fields.Float("Weight of Dry Soil",
                                 compute="compute_wt_of_drysoil")
    moisture_content = fields.Float("% Moisture(4/5 x 100)",
                                    compute="compute_moisture_percentage")

    # Compute line no
    @api.depends('consistency_id')
    def _compute_get_trial_number(self):
        for liquid in self.mapped('consistency_id'):
            trial_no = 1
            for line in liquid.liquid_limit_ids:
                line.trial_no = trial_no
                trial_no += 1

    # Calculate Weight of water - auto-computed as
    # (Weight of Dish + Wet Soil) � (Weight of Dish + Dry Soil)
    # Eg:(22.79 - 19.76 = 2.95)
    @api.depends('wt_of_dish_wetsoil', 'wt_of_dish_drysoil')
    def compute_wt_of_water(self):
        for liquit in self:
            wet_soil = liquit.wt_of_dish_wetsoil
            dry_soil = liquit.wt_of_dish_drysoil
            wt_of_water = (wet_soil - dry_soil)
            liquit.update({'wt_of_water': wt_of_water})

    # Calculate Weight of Dry Soil - auto-computed as
    # (Weight of Dish + Dry Soil) � (Weight of Dish)
    # Eg : (19.76 - 9.63 = 10.13)
    @api.depends('wt_of_dish_drysoil', 'wt_of_dish')
    def compute_wt_of_drysoil(self):
        for liquit in self:
            dry_soil = liquit.wt_of_dish_drysoil
            wt_of_dish = liquit.wt_of_dish
            wt_of_dry_soil = (dry_soil - wt_of_dish)
            liquit.update({'wt_of_drysoil': wt_of_dry_soil})

    # Calculate  % Moisture (4/5 x 100) - auto-computed as
    # (Weight of Water / Weight of Dry Soil) * 100
    # Eg: (2.95 / 10.13 ) * 100 = 29.12
    @api.depends('wt_of_water', 'wt_of_drysoil')
    def compute_moisture_percentage(self):
        for liquit in self:
            wt_of_water = liquit.wt_of_water
            wt_of_drysoil = liquit.wt_of_drysoil
            if wt_of_water and wt_of_drysoil:
                moisture = (wt_of_water / wt_of_drysoil)
                moisture_content = (moisture * 100)
                liquit.update({'moisture_content': moisture_content})
