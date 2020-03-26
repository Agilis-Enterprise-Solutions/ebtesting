# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    journal_id = fields.Many2one('account.journal', "Payment Mode" ,domain="['|',('type', '=', 'bank'),('type', '=', 'cash')]")
    sale_type = fields.Selection([
                                ('laboratory', _('Laboratory')),
                                ('soil drilling', _('Soil Drilling'))],
                                string='Sale Type',
                                default='laboratory')
    branch_id = fields.Many2one('config.branch', 'Branch')
    isassociate_project = fields.Boolean('Associated to a Project',
                                         default=False)
    no_of_boreholes = fields.Integer("No.of Boreholes", default=1)
    depth = fields.Float("Depth", digits=dp.get_precision('Product Price'))
    intervals = fields.Float("Interval", digits=dp.get_precision('Account')
                             )
    scope_note = fields.Text("Scope of Work")
    task_no_ids = fields.One2many('skit.task', 'order_id', "Task numbers",
                                  states={'cancel': [('readonly', True)],
                                          'done': [('readonly', True)]},
                                  copy=True, auto_join=True)
    project_id = fields.Many2one('project.project', readonly=True)

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        # Change Sales Order document sequence from SO to JO
        res['name'] = vals['name'].replace('SO', 'JO')
        order_lines = self.order_line
        for line in order_lines:
            test_desired = line.product_id.soil_test_type1
            line.create({'test_desired':test_desired})
        if (vals.get('task_no_ids')):
            user = self.env['res.users'].browse(self.env.uid)
            order_id = self.id
            project_task = self.env['project.task']
            project_wizard = self.env['skit.project.wizard'].search([
                                ('order_id', '=', order_id)])
            task_no = self.env['skit.task'].search([
                                ('order_id', '=', order_id)])
            for task in task_no:
                if not task.task_id:
                    # create new Task for corresponding project
                    new_task = project_task.create({
                                    'name': task.task_name,
                                    'project_id': project_wizard.project_id.id,
                                    'user_id': user.id})
                    # update task id in skit.task table
                    task.write({'task_id': new_task.id})
        return res

    @api.multi
    def write(self, vals):
        result = super(SaleOrder, self).write(vals)
        order_lines = self.order_line
        for line in order_lines:
            test_desired = line.product_id.soil_test_type1
            line.write({'test_desired':test_desired})
        if (vals.get('task_no_ids')):
            user = self.env['res.users'].browse(self.env.uid)
            order_id = self.id
            project_task = self.env['project.task']
            project_wizard = self.env['skit.project.wizard'].search([
                                        ('order_id', '=', order_id)])
            task_no = self.env['skit.task'].search([
                                        ('order_id', '=', order_id)])
            for task in task_no:
                if not task.task_id:
                    # create new Task for corresponding project
                    new_task = project_task.create({
                                    'name': task.task_name,
                                    'project_id': project_wizard.project_id.id,
                                    'user_id': user.id})
                    # update task id in skit.task table
                    task.write({'task_id': new_task.id})
                else:
                    old_task = task.task_id
                    # Task name update
                    old_task.write({'name': task.task_name})
        return result

    # This initiate the creation of a Project in the Project Module once the
    # create Project document is clicked.
    @api.multi
    def project_document(self):
        for line in self.order_line:
            if not line.lab_no:
                raise UserError(_('Generate Lab Number before Creation of Project document '))
        return {
            'name': _('Project from Sales'),
            'view_type': 'form',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_model': 'skit.project.wizard',
            'view_id': self.env.ref('skit_soil_drilling.skit_project_wizard_form').ids,
            'target': 'new',
            'context': {
                    'order_id': self.id,'default_name':self.mapped('project_id').name
                }
        }

    @api.onchange('branch_id')
    def _onchange_branch(self):
        pricelist = self.env['ir.config_parameter'].sudo().get_param('sale.sale_pricelist_setting')
        if  pricelist=="fixed" :
              raise UserError(_('Before creating Job Order. Go to Configuration -->Settings -->Enable (Multiple Sales Prices per Product)'))
        else :
            if self.branch_id:
                for line in self.order_line:
                    if line.lab_no:
                        raise UserError(_('Already Lab no. generated for this order.'))
                self.pricelist_id = False
                return {
                    'domain': {'pricelist_id': [
                        ('branch_id', '=', self.branch_id.id)]}}
                
          
    
    @api.multi
    def generate_lab_no(self):
        ''' Generate lab number for each test template selected in sale order line corresponds to  
        selected  product  and create corresponding test  template in project (laboratory menu)'''
        for line in self.order_line:
            date = datetime.strftime(line.date, '%y%m%d')
            branch = self.branch_id.branch_code
            if not line.lab_no :
                for value in line.product_id.product_tmpl_id:
                    temp = self.env['product.template'].search([
                                        ('id', '=', value.id)])
                    if not temp.quality_test_ids :
                         raise UserError(_(' Selected  Product  must contain atleast one Test Template to Generate LAB No.'))
                        
                    for test in temp.quality_test_ids :
                        self.env.cr.execute("""
                        select max(sl.seq_no) from sale_order so
                        inner join sale_order_line sl on so.id = sl.order_id
                        where so.branch_id = (%s) and sl.date = (%s)
                        """, (self.branch_id.id, line.date))
                        sql = self.env.cr.dictfetchall()
                        max_seqno = sql[0].get('max')
                        if (max_seqno == None):
                            max_seqno = 0
                        seq = int(max_seqno) + 1
                        seqno = str(seq)
                        seq_no = seqno.zfill(4)
                        lab_num ='LR'+branch+'-'+date+'-'+ seq_no
                        line.update({'seq_no': seq_no,
                                 })
                        lab_id = self.env['laboratory.number'].create({ 
                                                        'name':lab_num})   
                        line.update({ 'lab_no' : [(4,lab_id.id)]})
                        name = test.name
                        if name == 'Soil Aggregate':
                            project = self.env['skit.soil.aggregate'].create({
                                    'name': lab_num,
                                    })
                        if name == 'Soil Compaction':
                            project = self.env['skit.soil.compaction'].create({
                                    'name': lab_num,
                                    })
                        if name == 'Soil Consistency':
                            project = self.env['skit.soil.consistency'].create({
                                    'name': lab_num,
                                    })
                        if name == 'Sieve Analysis':
                            project = self.env['skit.sieve.analysis'].create({
                                    'name': lab_num,
                                    })
                        if name == 'Soil Penetration':
                            project = self.env['skit.soil.penetration'].create({
                                    'name': lab_num,
                                    })
                        if name == 'Soil Abrasion':
                            project = self.env['skit.soil.abrasion'].create({
                                    'name': lab_num,
                                    }) 
                                        
    
                  

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date = fields.Date(string="Date")
    test_desired = fields.Selection([
        ('selective_test', 'Specific Test'),
        ('quality_test', 'Quality Test')],
        'Test Desired')
    section = fields.Selection([
        ('concrete','Concrete'),
        ('steel','Steel'),
        ('chemical','Chemical'),
        ('soil','Soil')],'Section')  
    lab_no = fields.Many2many('laboratory.number',string="Lab No.")
    seq_no = fields.Char('Seq_no')

    # Set test_desired value while change product_id
    @api.onchange('product_id')
    def _onchange_product_set_testdesired(self):
        testdesired = self.product_id.soil_test_type1
        kind_of_material = self.product_id.kind_of_material
        self.test_desired = testdesired
        self.section = kind_of_material
        
    # filters the product based on lab work and test desired
    @api.onchange('sequence')
    def onchange_sequence(self):
        service = self.env['product.product'].search([('type','=','service'),('lab_work','=',True)])
        return {
                    'domain':{
                    'product_id':[(('id', 'in', service.ids))],
               },}  

class SkitTask(models.Model):
    _name = 'skit.task'

    order_id = fields.Many2one('sale.order', 'Sale Order')
    task_no = fields.Integer(string="Task Number")
    task_name = fields.Char(string="Task Name")
    task_id = fields.Many2one('project.task', 'Task')
    
    
class laboratory(models.Model):
    _name = 'laboratory.number'
    _description = 'Laboratory Number'
    
    name = fields.Char("Lab_no")
