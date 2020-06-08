# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models


class report_soil_compaction_document(models.AbstractModel):
    _name = 'report.skit_project.report_soil_compaction_document'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.soil.compaction']
        moisture_content = []
        datas = []
        data=[]
        values=[]
        value1=[]
        vertical=[]
        for comp_id in docids:
            compaction = model.search([('id', '=', comp_id)])
            moisture = self.env['skit.compaction.moisture'].search([
                                        ('compaction_id', '=', compaction.id)])
            density = self.env['skit.compaction.density'].search([
                                        ('compaction_id', '=', compaction.id)])
            if moisture:
                for moisture_id in moisture:
                    moisture_content.append({
                                'key': moisture_id.moisture_can_no,
                                'value': round(moisture_id.moisture_content, 2)
                                })
            if density:
                for density_id in density:
                    for value in moisture_content:
                        if(density_id.moisture_can_no == value['key']):
                        
                            data.append(value['value'])
                            values.append(round(density_id.dry_density, 2))
                            value1.append({'value': round(density_id.dry_density, 2),
                                         'labels':value['value']})
                values.sort(reverse=True)        
                data.sort(reverse=True) 
                verti =len(data)
                verti-=1
                for x in value1:
                    if x['value']==values[0]:
                        vertical.append(x['labels'])
                    elif x['value']== values[1]:
                        vertical.append(x['labels'])
                    print(vertical)  
                val1=vertical[0]
                val2=vertical[1] 
                v1_value =  (val1 + val2)/1.95  
                for density_id in density:
                    for value in moisture_content:
                        if(density_id.moisture_can_no == value['key']):
                            optimum=round(compaction.optimum_moisture_content,2)
                            datas.append({
                                "value":value['value'] ,
                                "labels": round(density_id.dry_density, 2),
                                "horizontal":values[0],
                                "vertical":values[verti],
                                "xaxis": "Moisture Content%="+str(optimum)
                                })
                datas.append({"value":v1_value,
                              "vertical":values[verti]})
                datas.append({"value":v1_value,
                              "vertical":values[0]})
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': compaction,
               'docs_line': moisture,
               'docs_lines': density,
               'graph': datas}
            
class report_soil_compaction_document_advance(models.AbstractModel):
    _name = 'report.skit_project.report_soil_compaction_document_advance'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.soil.compaction']
        moisture_content = []
        datas = []
        data=[]
        values=[]
        value1=[]
        vertical=[]
        for comp_id in docids:
            compaction = model.search([('id', '=', comp_id)])
            moisture = self.env['skit.compaction.moisture'].search([
                                        ('compaction_id', '=', compaction.id)])
            density = self.env['skit.compaction.density'].search([
                                        ('compaction_id', '=', compaction.id)])
            if moisture:
                for moisture_id in moisture:
                    moisture_content.append({
                                'key': moisture_id.moisture_can_no,
                                'value': round(moisture_id.moisture_content, 2)
                                })
            if density:
                for density_id in density:
                    for value in moisture_content:
                        if(density_id.moisture_can_no == value['key']):
                        
                            data.append(value['value'])
                            values.append(round(density_id.dry_density, 2))
                            value1.append({'value': round(density_id.dry_density, 2),
                                         'labels':value['value']})
                values.sort(reverse=True)        
                data.sort(reverse=True) 
                verti =len(data)
                verti-=1
                for x in value1:
                    if x['value']==values[0]:
                        vertical.append(x['labels'])
                    elif x['value']== values[1]:
                        vertical.append(x['labels'])
                    print(vertical)  
                val1=vertical[0]
                val2=vertical[1] 
                v1_value =  (val1 + val2)/1.95  
                for density_id in density:
                    for value in moisture_content:
                        if(density_id.moisture_can_no == value['key']):
                            optimum=round(compaction.optimum_moisture_content,2)
                            datas.append({
                                "value":value['value'] ,
                                "labels": round(density_id.dry_density, 2),
                                "horizontal":values[0],
                                "vertical":values[verti],
                                "xaxis": "Moisture Content%="+str(optimum)
                                })
                datas.append({"value":v1_value,
                              "vertical":values[verti]})
                datas.append({"value":v1_value,
                              "vertical":values[0]})
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': compaction,
               'docs_line': moisture,
               'docs_lines': density,
               'graph': datas}
