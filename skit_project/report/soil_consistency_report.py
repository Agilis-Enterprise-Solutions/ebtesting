# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models,_
from odoo.exceptions import UserError

class report_soil_consistency_document(models.AbstractModel):
    _name = 'report.skit_project.report_soil_consistency_document'
   
    @api.model
    def _get_report_values(self, docids, data=None):
        datas=[]
        yaxis=[]
        xaxis=[]
        x1=0
        model = self.env['skit.soil.consistency']
        for consis_id in docids :
            consistency = model.search([('id', '=', consis_id)])
            plastic_limit = self.env['skit.plastic.limit'].search([
                                                ('consistency_id', '=', consistency.id)])
            liquid_limit = self.env['skit.liquid.limit'].search([
                                                ('consistency_id', '=', consistency.id)])
            limit=0
            if liquid_limit :
                for liquid in liquid_limit:
                    xaxis.append(round(liquid.moisture_content, 2))
                    yaxis.append(liquid.no_of_blow)
                if len(xaxis) >=3 and len(yaxis) >=3:
                    x1=xaxis[0]
                    x2=xaxis[1]
                    x3=xaxis[2]
                    y1= yaxis[0]
                    y2=yaxis[1]
                    y3=yaxis[2]
                    xaxis.sort(reverse=True)
                    if  y1 <= consistency.plastic_limit <= y2 or y1 >= consistency.plastic_limit >= y2:
                        if y1==y2 or x1==x2:
                            limit=0
                        else:
                            straight_y =consistency.plastic_limit
                            m=round((y2-y1)/(x2-x1),5)
                            b=round((y1-m*x1),3)
                            limit= round(((straight_y-b)/m),2)
                            
                    elif y2 <= consistency.plastic_limit <= y3 or y2 >= consistency.plastic_limit >= y3:
                        if y2==y3 or x2==x3:
                            limit=0
                        else:
                            straight_y =consistency.plastic_limit
                            m=round((y3-y2)/(x3-x2),5)
                            b=round((y2-m*x2),3)
                            limit= round(((straight_y-b)/m),2)
                    for liquid in liquid_limit:  
                        datas.append({"labels": round(liquid.moisture_content, 2),
                                  "value": liquid.no_of_blow, 
                                  "horizontal":limit,
                                  "vertical":x1})
                    
                    
            datas.append({ "value":consistency.plastic_limit,
                       "vertical":x1,})
            datas.append({ "value":consistency.plastic_limit,
                       "vertical":xaxis[0]})
            print(datas)
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
        yaxis=[]
        xaxis=[]
        x1=0
        model = self.env['skit.soil.consistency']
        for consis_id in docids :
            consistency = model.search([('id', '=', consis_id)])
            plastic_limit = self.env['skit.plastic.limit'].search([
                                                ('consistency_id', '=', consistency.id)])
            liquid_limit = self.env['skit.liquid.limit'].search([
                                                ('consistency_id', '=', consistency.id)])
            limit=0
            if liquid_limit :
                for liquid in liquid_limit:
                    xaxis.append(round(liquid.moisture_content, 2))
                    yaxis.append(liquid.no_of_blow)
                if len(xaxis) >=3 and len(yaxis) >=3:
                    x1=xaxis[0]
                    x2=xaxis[1]
                    x3=xaxis[2]
                    y1= yaxis[0]
                    y2=yaxis[1]
                    y3=yaxis[2]
                    xaxis.sort(reverse=True)
                    if  y1 <= consistency.plastic_limit <= y2 or y1 >= consistency.plastic_limit >= y2:
                        if y1==y2 or x1==x2:
                            limit=0
                        else:
                            straight_y =consistency.plastic_limit
                            m=round((y2-y1)/(x2-x1),5)
                            b=round((y1-m*x1),3)
                            limit= round(((straight_y-b)/m),2)
                            
                    elif y2 <= consistency.plastic_limit <= y3 or y2 >= consistency.plastic_limit >= y3:
                        if y2==y3 or x2==x3:
                            limit=0
                        else:
                            straight_y =consistency.plastic_limit
                            m=round((y3-y2)/(x3-x2),5)
                            b=round((y2-m*x2),3)
                            limit= round(((straight_y-b)/m),2)
                    for liquid in liquid_limit:  
                        datas.append({"labels": round(liquid.moisture_content, 2),
                                  "value": liquid.no_of_blow, 
                                  "horizontal":limit,
                                  "vertical":x1})
                    
                    
            datas.append({ "value":consistency.plastic_limit,
                       "vertical":x1,})
            datas.append({ "value":consistency.plastic_limit,
                       "vertical":xaxis[0]})
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': consistency,
               'docs_line' :plastic_limit , 
               'liquid' :liquid_limit,
               'graph':datas
            }   
            
       
    
            
