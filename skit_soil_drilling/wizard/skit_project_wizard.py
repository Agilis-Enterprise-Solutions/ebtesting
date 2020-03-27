# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _


class skitprojectwizard(models.Model):

    _name = 'skit.project.wizard'
    _description = "Project Wizard"

    name = fields.Char("Project Name", required=True)
    project_id = fields.Many2one('project.project', 'Project')
    user_id = fields.Many2one('res.users', "Project Manager")
    classification = fields.Selection([('project', _('Project'))],
                                      string='Classification',
                                      default='project')
    parent_project_id = fields.Many2one('project.project',
                                        "Parent Project")
    description = fields.Html(string='Description')
    order_id = fields.Many2one('sale.order', 'Order')

    # Create Project Document Button was clicked, a pop-up form will appear for
    # both Laboratory and Soil Drilling  Sale Types. This initiate the creation
    # of a Project in the Project Module once the Create Project is clicked.
    @api.multi
    def create_project_document(self):
        order_id = self.env.context['order_id']
        content = self.env['sale.order.line'].search([
                                        ('order_id', '=', order_id)])
        user_id = self.user_id
        project = self.env['project.project']
        project_task_ids = self.env['project.task.type'].search([('name','in',['Drilling','Laboratory','Geotechnical','Releasing'])])
       
        order = self.env['sale.order'].search([('id', '=', order_id)])
        if not order.project_id :
            project_id = project.create({'name': self.name,
                                         'user_id': user_id.id})
            self.update({'project_id': project_id.id,
                         'order_id': order_id})
            order.update({'project_id': self.project_id.id})
            for project_task in project_task_ids :
                project_task.update({'project_ids': [(4, self.project_id.id)]})
        else :
            for project_task in project_task_ids :
                project_task.update({'project_ids': [(4, order.project_id.id)]})
            
        for values in content:
            lab_no = values.lab_no
            for id in lab_no :
                for value in values.product_id.product_tmpl_id:
#                     product = value.product_tmpl_id
                    for temp_id in value:
                        temp = self.env['product.template'].search([
                                                    ('id', '=', temp_id.id)])
                        quality_test = temp.quality_test_ids
                        for quality_id in quality_test:
                            quality = self.env['skit.test.template'].search([
                                                ('id', '=', quality_id.id)])
                            quality_value = quality.name
                            if quality_value == 'Soil Aggregate':
                                project = self.env['skit.soil.aggregate'].search([
                                                ('name', '=', id.name)])
                                if  not project.project_id :
                                    if self.project_id.id :
                                        project.update({'project_id': self.project_id.id})
                                    else :
                                        project.update({'project_id': order.project_id.id})
                                        
                            if quality_value == 'Soil Compaction':
                                project = self.env['skit.soil.compaction'].search([
                                                ('name', '=', id.name)])
                                if  not project.project_id :
                                    if self.project_id.id :
                                        project.update({'project_id': self.project_id.id})
                                    else :
                                        project.update({'project_id': order.project_id.id})
                            if quality_value == 'Soil Consistency':
                                project = self.env['skit.soil.consistency'].search(
                                                [('name', '=', id.name)])
                                if  not project.project_id :
                                    if self.project_id.id :
                                        project.update({'project_id': self.project_id.id})
                                    else :
                                        project.update({'project_id': order.project_id.id})
                            if quality_value == 'Sieve Analysis':
                                project = self.env['skit.sieve.analysis'].search([
                                                ('name', '=', id.name)])
                                if  not project.project_id :
                                    if self.project_id.id :
                                        project.update({'project_id': self.project_id.id})
                                    else :
                                        project.update({'project_id': order.project_id.id})
                            if quality_value == 'Soil Penetration':
                                project = self.env['skit.soil.penetration'].search(
                                                [('name', '=', id.name)])
                                if  not project.project_id :
                                    if self.project_id.id :
                                        project.update({'project_id': self.project_id.id})
                                    else :
                                        project.update({'project_id': order.project_id.id})
                            if quality_value == 'Soil Abrasion':
                                project = self.env['skit.soil.abrasion'].search([
                                                ('name', '=', id.name)])
                                if  not project.project_id :
                                    if self.project_id.id :
                                        project.update({'project_id': self.project_id.id})
                                    else :
                                        project.update({'project_id': order.project_id.id})
            project_stage_id = self.env['project.task.type'].search([('name','=','Laboratory')])
            
            for value in values.lab_no:
                aggregate = self.env['skit.soil.aggregate'].search([('name','=',value.name)])
                if aggregate :
                    template="Soil Aggregate Test"
                sieve = self.env['skit.sieve.analysis'].search([('name','=',value.name)])
                if sieve :
                    template ="Sieve Analysis / Grading Test"
                compaction = self.env['skit.soil.compaction'].search([('name','=',value.name)])
                if compaction :
                    template ="Soil Compaction Test"
                consistency =self.env['skit.soil.consistency'].search([('name','=',value.name)])
                if consistency :
                    template ="Soil Consistency Test"
                abrasion = self.env['skit.soil.abrasion'].search([('name','=',value.name)])
                if abrasion :
                    template = "Soil Abrasion Test"
                penetration = self.env['skit.soil.penetration'].search([('name','=',value.name)])
                if penetration :
                    template = "Soil Penetration Test"
                
                for name in value:
                    tasks = self.env['project.task'].search([('name','=',name.name)])
                    if not  tasks :
                        task = self.env['project.task'].create({
                                            'id':self.id,
                                            'project_id':order.project_id.id or project_id.id,
                                            'name' : name.name,
                                            'stage_id':project_stage_id.id,
                                            'template_name':template
                                        })

class ProjectTask(models.Model):
    _inherit ="project.task"
    focus_template = fields.Char("Focus")
    template_name = fields.Char("Template")
    
    
    @api.multi
    def action_view_focus(self):
        aggregate = self.env['skit.soil.aggregate'].search([('name','=',self.name)])
        compaction = self.env['skit.soil.compaction'].search([('name','=',self.name)])
        penetration = self.env['skit.soil.penetration'].search([('name','=',self.name)])
        consistency = self.env['skit.soil.consistency'].search([('name','=',self.name)])
        analysis = self.env['skit.sieve.analysis'].search([('name','=',self.name)])
        abrasion = self.env['skit.soil.abrasion'].search([('name','=',self.name)])
        if aggregate :
            result = {
                    'name': 'Soil Aggregate Test',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'skit.soil.aggregate',
                    'res_id': aggregate.id,
                        }
            return result 
        if compaction:
            result = {
                    'name': 'Soil Compaction Test',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'skit.soil.compaction',
                    'res_id': compaction.id,
                        }
            return result 
        if penetration :
            result = {
                    'name': 'Soil Penetration Test',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'skit.soil.penetration',
                    'res_id': penetration.id,
                        }
            return result 
        if consistency :
            result = {
                    'name': 'Soil Consistency Test',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'skit.soil.consistency',
                    'res_id': consistency.id,
                        }
            return result 
        if analysis :
            result = {
                    'name': 'Sieve Analysis Test',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'skit.sieve.analysis',
                    'res_id': analysis.id,
                        }
            return result 
        if abrasion :
            result = {
                    'name': 'Soil Abrasion Test',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'skit.soil.abrasion',
                    'res_id': abrasion.id,
                        }
       
            return result  
            
             
