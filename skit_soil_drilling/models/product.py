from odoo import models, fields,api


class product(models.Model):

    _inherit = "product.template"

    lab_work = fields.Boolean('Lab Work', default=False)
    soil_test_type = fields.Selection([
        ('lab', 'Laboratory Options'),
        ('soil', 'Soil Drilling')], 'Function')
    soil_test_type1 = fields.Selection([
        ('quality_test', 'Quality Test'),
        ('selective_test', 'Selective test')], 'Test Type')

    quality_test_ids = fields.Many2many('skit.test.template',
                                        string='Test Template')
    selective_test_id = fields.Many2one('skit.test.template',
                                        string='Test Template')
    kind_of_material = fields.Selection([
        ('concrete','Concrete'),
        ('steel','Steel'),
        ('chemical','Chemical'),
        ('soil','Soil')],'Kind of material')  
    branch_name = fields.Many2one('config.branch','Branch')
   
    @api.onchange('quality_test_ids')
    def onchange_test_template(self):
        test = len(self.quality_test_ids)
        if test == 1 :
            self.update({
                'soil_test_type1' : 'selective_test'})
        elif test > 1 :
            self.update({
                'soil_test_type1' : 'quality_test'})
        elif test == 0 :
            self.update({
                'soil_test_type1' : ''})
class productproduct(models.Model):
    _inherit = "product.product"
    
    @api.onchange('quality_test_ids')
    def onchange_test_template(self):
        test = len(self.quality_test_ids)
        if test == 1 :
            self.update({
                'soil_test_type1' : 'selective_test'})
        elif test > 1 :
            self.update({
                'soil_test_type1' : 'quality_test'})
        elif test == 0 :
            self.update({
                'soil_test_type1' : ''})