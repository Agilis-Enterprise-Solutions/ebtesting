# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from datetime import datetime, date
from odoo.exceptions import UserError
import json


class SoilPenetration(models.Model):
    _name = "skit.soil.penetration"
    _description = "Soil Penetration Test"

    name = fields.Char(string="Lab Result No:")
    penetration_test_date = fields.Date("Date")
    project_id = fields.Many2one('project.project', "Project Name")
    location_id = fields.Many2one('skit.location')
    sample_identify = fields.Char(string="Sample Identification")
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
                             default='draft', track_visibility='onchange')
    tested_by = fields.Many2one('res.users', "Tested By", readonly=True)
    tested_date = fields.Datetime("Tested Date", readonly=True, copy=False)
    checked_by = fields.Many2one('res.users', "Checked By", readonly=True)
    checked_date = fields.Datetime("Checked Date", readonly=True, copy=False)
    witnessed_by = fields.Many2many('res.partner',string="Witnessed By",domain="[('is_company','=',False)]")
    witnessed_date = fields.Datetime("Witnessed Date")
    attested_by = fields.Many2one('res.users', "Attested By", readonly=True)
    attested_date = fields.Datetime("Attested Date", readonly=True, copy=False)
    penetration_line_blow10_ids = fields.One2many(
                                                'skit.penetration.line.blow10',
                                                'penetration_id')
    penetration_line_blow30_ids = fields.One2many(
                                                'skit.penetration.line.blow30',
                                                'penetration_id')
    penetration_line_blow65_ids = fields.One2many(
                                                'skit.penetration.line.blow65',
                                                'penetration_id')
    wt_of_cylindersoil_10 = fields.Integer("Wt.of Cyl. + Soil gms")
    wt_of_cylinder_10 = fields.Integer("Wt. of Cylinder gms")
    wt_of_soil_10 = fields.Integer("Wt. of Soil gms",
                                   compute='compute_wt_of_soil_10')
    wet_density_10 = fields.Float("Wet Density g/cc",
                                  compute='compute_wet_density_10',
                                  digits=(12, 3))
    can_number_10 = fields.Char("Can No")
    wt_of_can_wet_soil_10 = fields.Float("Wt. of Can + Wet Soil gms")
    wt_of_can_dry_soil_10 = fields.Float("Wt. of Can + Dry Soil gms")
    moisture_loss_10 = fields.Float("Moisture Loss gms",
                                    compute='compute_moisture_loss_10')
    wt_of_can_10 = fields.Float("Wt. of Can gms")
    wt_of_dry_soil_10 = fields.Float("Wt. of Dry Soil gms",
                                     compute='compute_wt_dry_soil_10')
    moisture_content_10 = fields.Float("Moisture Content   %",
                                       compute='compute_moisture_content_10')
    dry_density_10 = fields.Float("Dry Density  gms",
                                  compute='compute_dry_density_10')
    vol_of_cylinder_10 = fields.Integer("Vol. of Cylinder cc")
    task_id = fields.Integer("Task", compute='_compute_task_id')
    wt_of_cylindersoil_30 = fields.Integer("Wt.of Cyl. + Soil gms")
    wt_of_cylinder_30 = fields.Integer("Wt. of Cylinder gms")
    wt_of_soil_30 = fields.Integer("Wt. of Soil gms",
                                   compute='compute_wt_of_soil_30')
    wet_density_30 = fields.Float("Wet Density g/cc",
                                  compute='compute_wet_density_30',
                                  digits=(12, 3))
    can_number_30 = fields.Char("Can No")
    wt_of_can_wet_soil_30 = fields.Float("Wt. of Can + Wet Soil gms")
    wt_of_can_dry_soil_30 = fields.Float("Wt. of Can + Dry Soil gms")
    moisture_loss_30 = fields.Float("Moisture Loss gms",
                                    compute='compute_moisture_loss_30')
    wt_of_can_30 = fields.Float("Wt. of Can gms")
    wt_of_dry_soil_30 = fields.Float("Wt. of Dry Soil gms",
                                     compute='compute_wt_dry_soil_30')
    moisture_content_30 = fields.Float("Moisture Content   %",
                                       compute='compute_moisture_content_30')
    dry_density_30 = fields.Float("Dry Density  gms",
                                  compute='compute_dry_density_30')
    vol_of_cylinder_30 = fields.Integer("Vol. of Cylinder cc")

    wt_of_cylindersoil_65 = fields.Integer("Wt.of Cyl. + Soil gms")
    wt_of_cylinder_65 = fields.Integer("Wt. of Cylinder gms")
    wt_of_soil_65 = fields.Integer("Wt. of Soil gms",
                                   compute='compute_wt_of_soil_65')
    wet_density_65 = fields.Float("Wet Density g/cc",
                                  compute='compute_wet_density_65',
                                  digits=(12, 3))
    can_number_65 = fields.Char("Can No")
    wt_of_can_wet_soil_65 = fields.Float("Wt. of Can + Wet Soil gms")
    wt_of_can_dry_soil_65 = fields.Float("Wt. of Can + Dry Soil gms")
    moisture_loss_65 = fields.Float("Moisture Loss gms",
                                    compute='compute_moisture_loss_65')
    wt_of_can_65 = fields.Float("Wt. of Can gms")
    wt_of_dry_soil_65 = fields.Float("Wt. of Dry Soil gms",
                                     compute='compute_wt_dry_soil_65')
    moisture_content_65 = fields.Float("Moisture Content   %",
                                       compute='compute_moisture_content_65')
    dry_density_65 = fields.Float("Dry Density  gms",
                                  compute='compute_dry_density_65')
    vol_of_cylinder_65 = fields.Integer("Vol. of Cylinder cc")
    mdd = fields.Float(string="MDD", digits=(12, 3))
    omc = fields.Float(string="OMC")
    cbr_100_per = fields.Float(string="CBR VALUE % @ 100",readonly=True)
    cbr_99_per = fields.Float(string="CBR VALUE % @ 99",readonly=True)
    swell = fields.Float(string="Swell(%)", digits=(12, 3))
    penetration_line_graph = fields.Text(compute='_penetration_line_graph')
    grade_check = fields.Boolean("check")
    grade = fields.Many2one("config.abrasion",String="Grade")

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
            grade = kind_of_material.grading
            if grade :
                material.update({'grade_check' :True})
            else :
                material.update({'grade_check' :False})
        return {
                    'domain':{
                    'grade':[(('id', 'in', grade.ids))],
               },}      
    
    @api.one
    def _penetration_line_graph(self):
        self.penetration_line_graph = json.dumps(self.get_line_graph_datas())

    @api.multi
    def get_line_graph_datas(self):
        datas = []
        vertical=[]
        horizontal=[]
        xmin = [0]
        xmax = [0]
        ymin = 0
        ymax = 0
        blow10 = self.env['skit.penetration.line.blow10'].search([
            ('penetration_id', '=', self.id)])
        blow30 = self.env['skit.penetration.line.blow30'].search([
            ('penetration_id', '=', self.id)])
        blow65 = self.env['skit.penetration.line.blow65'].search([
            ('penetration_id', '=', self.id)])
        xlabel = "CBR VALUE %@ 100 % ="+str(self.cbr_100_per)+" % @ 95% =" + str(
            self.cbr_99_per)+"% : Swell (%) = "+str(self.swell)
        # Get Max value of CBR in Blow10
        b10_max_value = 0
        if self.penetration_line_blow10_ids:
            for b10 in blow10:
                if b10.std_cbr > b10_max_value:
                    b10_max_value = b10.std_cbr
            datas.append({"value": round(self.dry_density_10, 1),
                          "labels": [b10_max_value, xlabel],
                          "yaxis": "Dry Density(g/cc)"})
            horizontal.append({"valuess":b10_max_value})
            vertical.append({"value": round(self.dry_density_10, 1)})

        # Get Max value of CBR in Blow30
        b30_max_value = 0
        if self.penetration_line_blow30_ids:
            for b30 in blow30:
                if b30.std_cbr > b30_max_value:
                    b30_max_value = b30.std_cbr
            datas.append({"value": round(self.dry_density_30, 1),
                          "labels": [b30_max_value, xlabel],
                          "yaxis": "Dry Density(g/cc)"})
            horizontal.append({"valuess":b30_max_value})
            vertical.append({"value": round(self.dry_density_30, 1)})
        # Get Max value of CBR in Blow65
        b65_max_value = 0
        if self.penetration_line_blow65_ids:
            for b65 in blow65:
                if b65.std_cbr > b65_max_value:
                    b65_max_value = b65.std_cbr
            datas.append({"value": round(self.dry_density_65, 1),
                          "labels": [b65_max_value, xlabel],
                          "yaxis": "Dry Density(g/cc)"})
            horizontal.append({"valuess":b65_max_value})
            vertical.append({"value": round(self.dry_density_65, 1)})
            
            
        if len(datas) >= 1:
            ymaxval = max(datas, key=lambda x: x['value'])
            yminval = min(datas, key=lambda x: x['value'])
            ymin = yminval.get('value') - 0.1
            ymax = ymaxval.get('value') + 1

            xmaxval = max(datas, key=lambda x: x['labels'])
            xminval = min(datas, key=lambda x: x['labels'])
            xmin = xminval.get('labels')
            xmax = xmaxval.get('labels')
        mdd=self.mdd
        mdd2 = round((mdd *0.95),1)
        density_10 = round(self.dry_density_10,1)
        density_30 = round(self.dry_density_30,1)
        density_65 = round(self.dry_density_65,1)
        x3=0
        x4=0
        
        if density_10 <= mdd <= density_30 or density_10 >= mdd >= density_30:
           
            x1=b10_max_value
            y1=density_10
            x2=b30_max_value
            y2 =density_30
            if y1==y2 or x1==x2:
                x3=0
            else:
                straight_y =mdd
                m=round((y2-y1)/(x2-x1),5)
                b=round((y1-m*x1),3)
                x3= (straight_y-b)/m
            
        elif  density_30 <= mdd <= density_65 or density_30 >= mdd >= density_65:
            x1=b30_max_value
            y1=density_30
            x2=b65_max_value
            y2 =density_65
            if y1==y2 or x1==x2:
                x3=0
            else:
                straight_y =mdd
                m=round((y2-y1)/(x2-x1),5)
                b=round((y1-m*x1),3)
                x3= (straight_y-b)/m
            
        
        if density_10 <=  mdd2 <= density_30 or density_10 >=  mdd2 >= density_30:
            x1=b10_max_value
            y1=density_10
            x2=b30_max_value
            y2 =density_30
            if y1==y2 or x1==x2:
                x4=0
            else:
                straight_y =mdd2
                m=round((y2-y1)/(x2-x1),5)
                b=round((y1-m*x1),3)
                x4= (straight_y-b)/m
           
         
        elif  density_30 <= mdd2 <= density_65 or density_30 >= mdd2 >= density_65:
            x1=b30_max_value
            y1=density_30
            x2=b65_max_value
            y2 =density_65
            if y1==y2 or x1==x2:
                x4=0
            else:
                straight_y =mdd2
                m=round((y2-y1)/(x2-x1),5)
                b=round((y1-m*x1),3)
                x4= (straight_y-b)/m
        
       
       
        self.write({'cbr_100_per':round(x3,2),
                      'cbr_99_per':round(x4,2),})
        
        
       
        
        return [{'values':datas,
                 'horizontal':horizontal,
                 'v1_value':x3 ,
                 'v2_value':x4 ,
                 'vertical':vertical,
                 'h1_value': mdd,
                 'h2_value':mdd2,
                 'y_val': [ymin, ymax],
                 'x_val': [xmin[0], xmax[0]+1],
                 'title': "MDD ="+str(self.mdd)+" OMC ="+str(self.omc)+" %",
                 'id': self.id}]
        

    # Calculate Weight of Soil - auto-computed as
    # (Weight of Cylinder + Soil) - (Weight of Cylinder)
    # Eg : (11715 - 7060 = 4655)
    @api.depends('wt_of_cylindersoil_10', 'wt_of_cylinder_10')
    def compute_wt_of_soil_10(self):
        for penetration in self:
            soil = penetration.wt_of_cylindersoil_10
            cylinder = penetration.wt_of_cylinder_10
            if soil and cylinder:
                total = (soil-cylinder)
                penetration.update({'wt_of_soil_10': total})

    # Calculate Wet Density - auto-computed as
    # (Weight of Soil) /( Volume of Cylinder)
    # Eg : (4655 / 2238 = 2.080)
    @api.depends('wt_of_soil_10', 'vol_of_cylinder_10')
    def compute_wet_density_10(self):
        for penetration in self:
            soil_wt = penetration.wt_of_soil_10
            vol = penetration.vol_of_cylinder_10
            if soil_wt and vol:
                wet = (soil_wt/vol)
                penetration.update({'wet_density_10': wet})

    # Calculate Moisture Loss - auto-computed as
    # (Weight of Can + Wet Soil) -(Weight of Can + Dry Soil)
    # Eg : (251-240 = 11.00)
    @api.depends('wt_of_can_wet_soil_10', 'wt_of_can_dry_soil_10')
    def compute_moisture_loss_10(self):
        for penetration in self:
            wet_soil = penetration.wt_of_can_wet_soil_10
            dry_soil = penetration.wt_of_can_dry_soil_10
            if wet_soil and dry_soil:
                moisture = (wet_soil-dry_soil)
                penetration.update({'moisture_loss_10': moisture})

    # Calculate  Weight of Dry Soil - auto-computed as
    # (Weight of Can + Dry Soil) -(Weight of Can)
    # Eg : (240 - 18.81 = 221.19)
    @api.depends('wt_of_can_dry_soil_10', 'wt_of_can_10')
    def compute_wt_dry_soil_10(self):
        for penetration in self:
            dry_soil = penetration.wt_of_can_dry_soil_10
            wt_can = penetration.wt_of_can_10
            if dry_soil and wt_can:
                dry_soil = (dry_soil-wt_can)
                penetration.update({'wt_of_dry_soil_10': dry_soil})

    # Calculate  Moisture Content - auto-computed as
    # (Moisture Loss) /Weight of Dry Soil)*100
    # Eg :( (11.00 /221.19 )*100= 4.973)
    @api.depends('wt_of_dry_soil_10', 'moisture_loss_10')
    def compute_moisture_content_10(self):
        for penetration in self:
            dry_soil = penetration.wt_of_dry_soil_10
            loss = penetration.moisture_loss_10
            if dry_soil and loss:
                content = (loss/dry_soil*100)
                penetration.update({'moisture_content_10': content})

    # Calculate  Dry Density- auto-computed as
    # (Wet Density) /(100 + moisture Content)*100
    # Eg : (2.080 /(100+4.973)*100 = 1.98)
    @api.depends('wet_density_10', 'moisture_content_10')
    def compute_dry_density_10(self):
        for penetration in self:
            wet = penetration.wet_density_10
            content = penetration.moisture_content_10
            if wet and content:
                dry = (wet/(100+content)*100)
                penetration.update({'dry_density_10': dry})

    # Calculate Weight of Soil - auto-computed as
    # (Weight of Cylinder + Soil) - (Weight of Cylinder)
    # Eg : (11715 - 7060 = 4655)
    @api.depends('wt_of_cylindersoil_30', 'wt_of_cylinder_30')
    def compute_wt_of_soil_30(self):
        for penetration in self:
            soil = penetration.wt_of_cylindersoil_30
            cylinder = penetration.wt_of_cylinder_30
            if soil and cylinder:
                total = (soil-cylinder)
                penetration.update({'wt_of_soil_30': total})

    # Calculate Wet Density - auto-computed as
    # (Weight of Soil) /( Volume of Cylinder)
    # Eg : (4655 / 2238 = 2.080)
    @api.depends('wt_of_soil_30', 'vol_of_cylinder_30')
    def compute_wet_density_30(self):
        for penetration in self:
            soil_wt = penetration.wt_of_soil_30
            vol = penetration.vol_of_cylinder_30
            if soil_wt and vol:
                wet = (soil_wt/vol)
                penetration.update({'wet_density_30': wet})

    # Calculate Moisture Loss - auto-computed as
    # (Weight of Can + Wet Soil) -(Weight of Can + Dry Soil)
    # Eg : (251-240 = 11.00)
    @api.depends('wt_of_can_wet_soil_30', 'wt_of_can_dry_soil_30')
    def compute_moisture_loss_30(self):
        for penetration in self:
            wet_soil = penetration.wt_of_can_wet_soil_30
            dry_soil = penetration.wt_of_can_dry_soil_30
            if wet_soil and dry_soil:
                moisture = (wet_soil-dry_soil)
                penetration.update({'moisture_loss_30': moisture})

    # Calculate  Weight of Dry Soil - auto-computed as
    # (Weight of Can + Dry Soil) -(Weight of Can)
    # Eg : (240 - 18.81 = 221.19)
    @api.depends('wt_of_can_dry_soil_30', 'wt_of_can_30')
    def compute_wt_dry_soil_30(self):
        for penetration in self:
            dry_soil = penetration.wt_of_can_dry_soil_30
            wt_can = penetration.wt_of_can_30
            if dry_soil and wt_can:
                dry_soil = (dry_soil-wt_can)
                penetration.update({'wt_of_dry_soil_30': dry_soil})

    # Calculate  Moisture Content - auto-computed as
    # (Moisture Loss) /Weight of Dry Soil)*100
    # Eg :( (11.00 /221.19 )*100= 4.973)
    @api.depends('wt_of_dry_soil_30', 'moisture_loss_30')
    def compute_moisture_content_30(self):
        for penetration in self:
            dry_soil = penetration.wt_of_dry_soil_30
            loss = penetration.moisture_loss_30
            if dry_soil and loss:
                content = (loss/dry_soil*100)
                penetration.update({'moisture_content_30': content})

    # Calculate  Dry Density- auto-computed as
    # (Wet Density) /(100 + moisture Content)*100
    # Eg : (2.080 /(100+4.973)*100 = 1.98)
    @api.depends('wet_density_30', 'moisture_content_30')
    def compute_dry_density_30(self):
        for penetration in self:
            wet = penetration.wet_density_30
            content = penetration.moisture_content_30
            if wet and content:
                dry = (wet/(100+content)*100)
                penetration.update({'dry_density_30': dry})

    # Calculate Weight of Soil - auto-computed as
    # (Weight of Cylinder + Soil) - (Weight of Cylinder)
    # Eg : (11715 - 7060 = 4655)
    @api.depends('wt_of_cylindersoil_65', 'wt_of_cylinder_65')
    def compute_wt_of_soil_65(self):
        for penetration in self:
            soil = penetration.wt_of_cylindersoil_65
            cylinder = penetration.wt_of_cylinder_65
            if soil and cylinder:
                total = (soil-cylinder)
                penetration.update({'wt_of_soil_65': total})

    # Calculate Wet Density - auto-computed as
    # (Weight of Soil) /( Volume of Cylinder)
    # Eg : (4655 / 2238 = 2.080)
    @api.depends('wt_of_soil_65', 'vol_of_cylinder_65')
    def compute_wet_density_65(self):
        for penetration in self:
            soil_wt = penetration.wt_of_soil_65
            vol = penetration.vol_of_cylinder_65
            if soil_wt and vol:
                wet = (soil_wt/vol)
                penetration.update({'wet_density_65': wet})

    # Calculate Moisture Loss - auto-computed as
    # (Weight of Can + Wet Soil) -(Weight of Can + Dry Soil)
    # Eg : (251-240 = 11.00)
    @api.depends('wt_of_can_wet_soil_65', 'wt_of_can_dry_soil_65')
    def compute_moisture_loss_65(self):
        for penetration in self:
            wet_soil = penetration.wt_of_can_wet_soil_65
            dry_soil = penetration.wt_of_can_dry_soil_65
            if wet_soil and dry_soil:
                moisture = (wet_soil-dry_soil)
                penetration.update({'moisture_loss_65': moisture})

    # Calculate  Weight of Dry Soil - auto-computed as
    # (Weight of Can + Dry Soil) -(Weight of Can)
    # Eg : (240 - 18.81 = 221.19)
    @api.depends('wt_of_can_dry_soil_65', 'wt_of_can_65')
    def compute_wt_dry_soil_65(self):
        for penetration in self:
            dry_soil = penetration.wt_of_can_dry_soil_65
            wt_can = penetration.wt_of_can_65
            if dry_soil and wt_can:
                dry_soil = (dry_soil-wt_can)
                penetration.update({'wt_of_dry_soil_65': dry_soil})

    # Calculate  Moisture Content - auto-computed as
    # (Moisture Loss) /Weight of Dry Soil)*100
    # Eg :( (11.00 /221.19 )*100= 4.973)
    @api.depends('wt_of_dry_soil_65', 'moisture_loss_65')
    def compute_moisture_content_65(self):
        for penetration in self:
            dry_soil = penetration.wt_of_dry_soil_65
            loss = penetration.moisture_loss_65
            if dry_soil and loss:
                content = (loss/dry_soil*100)
                penetration.update({'moisture_content_65': content})

    # Calculate  Dry Density- auto-computed as
    # (Wet Density) /(100 + moisture Content)*100
    # Eg : (2.080 /(100+4.973)*100 = 1.98)
    @api.depends('wet_density_65', 'moisture_content_65')
    def compute_dry_density_65(self):
        for penetration in self:
            wet = penetration.wet_density_65
            content = penetration.moisture_content_65
            if wet and content:
                dry = (wet/(100+content)*100)
                penetration.update({'dry_density_65': dry})

    @api.depends('name')
    def _compute_task_id(self):
        task = self.env['project.task'].search([('name', '=', self.name)])
        self.update({
            'task_id': task.id})

    @api.model
    def create(self, vals):
        vals['state'] = "draft"
        if (vals.get('sampled_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', vals['sampled_by'])])
            vals['designation_sampled'] = res_user.partner_id.id
            vals['date_performed'] = datetime.today()
        result = super(SoilPenetration, self).create(vals)
        return result

    @api.multi
    def write(self, values):
        if (values.get('sampled_by')):
            res_user = self.env['res.users'].search([
                            ('id', '=', values['sampled_by'])])
            values['designation_sampled'] = res_user.partner_id.id
            values['date_performed'] = datetime.today()
        result = super(SoilPenetration, self).write(values)
        return result

    # Submit Button Action
    @api.multi
    def pt_action_submit(self):
        user = self.env['res.users'].browse(self.env.uid)
        if (self.submitted_by):
            self.write({'state': 'submit',
                        'tested_by': user.id,
                        'tested_date': datetime.today(),
                        'designation_submitted': self.submitted_by.partner_id.id,
                        'date_submit': datetime.today()
                        })
    # Confirm Button Action
    @api.multi
    def pt_action_confirm(self):
        user = self.env['res.users'].browse(self.env.uid)
        self.write({'state': 'confirm',
                    'checked_by': user.id,
                    'checked_date': datetime.today()})

    # Verify Button Action
    @api.multi
    def pt_action_verify(self):
        self.write({'state': 'verify',
                    })

    # The Approved Button will appear when the test
    #  results were verified completely
    @api.multi
    def pt_action_approve(self):
        user = self.env['res.users'].browse(self.env.uid)
        if not self.penetration_test_date:
            self.write({'penetration_test_date': date.today()})
        self.write({'state': 'approved',
                    'attested_by': user.id,
                    'attested_date': datetime.today(),
                    })

    # Cancelled Button Action
    @api.multi
    def pt_action_cancel(self):
        self.write({'state': 'cancelled'})

    # Reset Button that can only be activated when approved
    # by the Branch Lead Technician.
    # This Button will delete the results as this
    # intends to repeat the test performed.
    @api.multi
    def pt_action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancelled'])
        return orders.write({
            'state': 'draft'})

    # auto-populated field and associated to the Sampled By field
    # date/time when the Sample was Submitted
    @api.onchange('sampled_by')
    def _onchange_sampled_by(self):
        sampled_by = self.sampled_by
        if sampled_by:
            self.designation_sampled = sampled_by.partner_id.id
            self.date_performed = datetime.today()


class SkitPenetrationLineBlow10(models.Model):
    _name = "skit.penetration.line.blow10"
    _description = "Soil Penetration Line Blows10"

    penetration_id = fields.Many2one('skit.soil.penetration')
    penetration = fields.Float(" (mm) ")
    load_tlr = fields.Integer(" TLR ")
    load_load = fields.Float("Load", compute='compute_load')
    std_std = fields.Float("Standard")
    std_cbr = fields.Integer("CBR", compute='compute_std_cbr')

    # Calculate Load - auto-computed as
    # (TLR*0.1321)
    # Eg: (475*0.1321=62.75)

    @api.depends('load_tlr')
    def compute_load(self):
        for penetration in self:
            penet = penetration.penetration
#             if penet == 2.50 or penet == 5.00:
            tlr = penetration.load_tlr
            if tlr:
                load = (tlr*3.031)
                penetration.update({'load_load': load})

    # Calculate CBR - auto-computed as
    # (Load/Standard)*100
    # Eg: (62.75/70.63)*100=86
    @api.depends('load_load', 'std_std')
    def compute_std_cbr(self):
        for penetration in self:
            load = penetration.load_load
            std = penetration.std_std
            if load and std:
                cbr = (load/std)*100
                cbr = round(cbr)
                penetration.update({'std_cbr': cbr})


class SkitPenetrationLineBlow30(models.Model):
    _name = "skit.penetration.line.blow30"
    _description = "Soil Penetration Line Blows30"

    penetration_id = fields.Many2one('skit.soil.penetration')
    penetration = fields.Float(" (mm) ")
    load_tlr = fields.Integer("TLR")
    load_load = fields.Float("Load", compute='compute_load')
    std_std = fields.Float("Standard")
    std_cbr = fields.Integer("CBR", compute='compute_std_cbr')

    # Calculate Load - auto-computed as
    # (TLR*0.1321)
    # Eg: (475*0.1321=62.75)
    @api.depends('load_tlr')
    def compute_load(self):
        for penetration in self:
            penet = penetration.penetration
#             if penet == 2.50 or penet == 5.00:
            tlr = penetration.load_tlr
            if tlr:
                load = (tlr*3.031)
                penetration.update({'load_load': load})

    # Calculate CBR - auto-computed as
    # (Load/Standard)*100
    # Eg: (62.75/70.63)*100=86
    @api.depends('load_load', 'std_std')
    def compute_std_cbr(self):
        for penetration in self:
            load = penetration.load_load
            std = penetration.std_std
            if load and std:
                cbr = (load/std)*100
                cbr = round(cbr)
                penetration.update({'std_cbr': cbr})


class SkitPenetrationLineBlow65(models.Model):
    _name = "skit.penetration.line.blow65"
    _description = "Soil Penetration Line Blows65"

    penetration_id = fields.Many2one('skit.soil.penetration')
    penetration = fields.Float(" (mm) ")
    load_tlr = fields.Integer("TLR")
    load_load = fields.Float("Load", compute='compute_load')
    std_std = fields.Float("Standard")
    std_cbr = fields.Integer("CBR", compute='compute_std_cbr')

    # Calculate Load - auto-computed as
    # (TLR*0.1321)
    # Eg: (475*0.1321=62.75)
    @api.depends('load_tlr')
    def compute_load(self):
        for penetration in self:
            penet = penetration.penetration
#             if penet == 2.50 or penet == 5.00:
            tlr = penetration.load_tlr
            if tlr:
                load = (tlr*3.031)
                penetration.update({'load_load': load})
    # Calculate CBR - auto-computed as
    # (Load/Standard)*100
    # Eg: (62.75/70.63)*100=86

    @api.depends('load_load', 'std_std')
    def compute_std_cbr(self):
        for penetration in self:
            load = penetration.load_load
            std = penetration.std_std
            if load and std:
                cbr = (load/std)*100
                cbr = round(cbr)
                penetration.update({'std_cbr': cbr})
