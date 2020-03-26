# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models,_
from odoo.exceptions import UserError

class report_soil_consistency_document(models.AbstractModel):
    _name = 'report.skit_project.report_soil_consistency_document'
   
    @api.model
    def _get_report_values(self, docids, data=None):
        datas=[]
        model = self.env['skit.soil.consistency']
        for consis_id in docids :
            consistency = model.search([('id', '=', consis_id)])
            plastic_limit = self.env['skit.plastic.limit'].search([
                                                ('consistency_id', '=', consistency.id)])
            liquid_limit = self.env['skit.liquid.limit'].search([
                                                ('consistency_id', '=', consistency.id)])
            if liquid_limit :
                for liquid in liquid_limit:
                    datas.append({"value": round(liquid.moisture_content, 2),
                                  "labels": liquid.no_of_blow
                                  })
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': consistency,
               'docs_line' :plastic_limit , 
               'liquid' :liquid_limit,
               'graph':datas
            }   

class report_soil_consistency_document_advance(models.AbstractModel):
    _name = 'report.skit_project.report_soil_consistency_document_advance'
   
    @api.model
    def _get_report_values(self, docids, data=None):
        datas=[]
        model = self.env['skit.soil.consistency']
        for consis_id in docids :
            consistency = model.search([('id', '=', consis_id)])
            plastic_limit = self.env['skit.plastic.limit'].search([
                                                ('consistency_id', '=', consistency.id)])
            liquid_limit = self.env['skit.liquid.limit'].search([
                                                ('consistency_id', '=', consistency.id)])
            if liquid_limit :
                for liquid in liquid_limit:
                    datas.append({"value": round(liquid.moisture_content, 2),
                                  "labels": liquid.no_of_blow
                                  })
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': consistency,
               'docs_line' :plastic_limit , 
               'liquid' :liquid_limit,
               'graph':datas
            }   
            
       
    
            
