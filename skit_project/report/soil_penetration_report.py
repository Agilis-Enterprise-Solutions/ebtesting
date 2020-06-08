# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models


class report_soil_penetration_document(models.AbstractModel):
    _name = 'report.skit_project.report_soil_penetration_document'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.soil.penetration']
        datas = []
#         values = []
#         vertical = []
#         vertical2=[]
        x3=0
        x4=0
        for penet_id in docids:
            penetration = model.search([('id', '=', penet_id)])
            blow10 = self.env['skit.penetration.line.blow10'].search([
                                    ('penetration_id', '=', penetration.id)])
            blow30 = self.env['skit.penetration.line.blow30'].search([
                                    ('penetration_id', '=', penetration.id)])
            blow65 = self.env['skit.penetration.line.blow65'].search([
                                    ('penetration_id', '=', penetration.id)])
            b10_max_value = 0
            mdd =penetration.mdd
            omc=round((mdd *0.95),1)
            density_10 = round(penetration.dry_density_10,1)
            density_30 = round(penetration.dry_density_30,1)
            density_65 = round(penetration.dry_density_65,1)
            if mdd:

                if blow10:
                    for b10 in blow10:
                        if b10.std_cbr > b10_max_value:
                            b10_max_value = b10.std_cbr
                    datas.append({
                        "labels": density_10,
                        "vertical":density_10,
                        "vertical1":density_10,
                        "horizontal": mdd,
                        "horizontal1": omc,
                        "value": b10_max_value})
    
                # Get Max value of CBR in Blow30
                if blow30:
                    b30_max_value = 0
                    for b30 in blow30:
                        if b30.std_cbr > b30_max_value:
                            b30_max_value = b30.std_cbr
                    datas.append({"labels":density_30,
                                 "vertical":density_10,
                                 "vertical1":density_10,
                                 "horizontal": mdd,
                                 "horizontal1":omc,
                                 "value": b30_max_value,
                                  })
    
                # Get Max value of CBR in Blow65
                if blow65:
                    b65_max_value = 0
                    for b65 in blow65:
                        if b65.std_cbr > b65_max_value:
                            b65_max_value = b65.std_cbr
                    datas.append({"labels": density_65,
                                "vertical":density_10,
                                "vertical1":density_10,
                                "horizontal": mdd,
                                "horizontal1":omc,
                                "value": b65_max_value,
                                  })
                    
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
                
            
                if density_10 <=  omc <= density_30 or density_10 >=  omc >= density_30:
                    x1=b10_max_value
                    y1=density_10
                    x2=b30_max_value
                    y2 =density_30
                    if y1==y2 or x1==x2:
                        x4=0
                    else:
                        straight_y =omc
                        m=round((y2-y1)/(x2-x1),5)
                        b=round((y1-m*x1),3)
                        x4= (straight_y-b)/m
                   
             
                elif  density_30 <= omc <= density_65 or density_30 >= omc >= density_65:
                    x1=b30_max_value
                    y1=density_30
                    x2=b65_max_value
                    y2 =density_65
                    if y1==y2 or x1==x2:
                        x4=0
                    else:
                        straight_y =omc
                        m=round((y2-y1)/(x2-x1),5)
                        b=round((y1-m*x1),3)
                        x4= (straight_y-b)/m
    
                    
                datas.append({
                            "vertical":density_10,
                            "vertical1":density_10,
                            "value": x3,
                              })
                datas.append({
                              "vertical":density_30,
                              "vertical1":density_10,
                              "value": x3,
                              })
                datas.append({
                              "vertical":density_65,
                              "vertical1":density_10,
                              "value": x3,
                              })
                datas.append({
                              "vertical1":density_10,
                              "value": x4,
                              })
                datas.append({
                              "vertical1":density_30,
                              "value": x4,
                              })
                datas.append({
                              "vertical1":density_65,
                              "value": x4,
                              })
    
            else:
                if blow10:
                    for b10 in blow10:
                        if b10.std_cbr > b10_max_value:
                            b10_max_value = b10.std_cbr
                            datas.append({"value": round(penetration.dry_density_10, 1),
                             "labels": b10_max_value})

            # Get Max value of CBR in Blow30
                if blow30:
                    b30_max_value = 0
                    for b30 in blow30:
                        if b30.std_cbr > b30_max_value:
                            b30_max_value = b30.std_cbr
                    datas.append({"value": round(penetration.dry_density_30, 1),
                                  "labels": b30_max_value,
                                  })
                # Get Max value of CBR in Blow65
                if blow65:
                    b65_max_value = 0
                    for b65 in blow65:
                        if b65.std_cbr > b65_max_value:
                            b65_max_value = b65.std_cbr
                    datas.append({"value": round(penetration.dry_density_65, 1),
                                  "labels": b65_max_value,
                                  })
                    
            if len(datas) >= 1:
                datas.append({"xaxis": "CBR VALUE %@ 100 % = "+str(penetration.cbr_100_per)+"% @ 95%  = " +str(penetration.cbr_99_per)+" % : Swell (%) =" +str(penetration.swell)})
                
            
            
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': penetration,
               'docs_line': blow10,
               'blow_30': blow30,
               'blow_65': blow65,
               'graph': datas,
               
            }

class report_soil_penetration_document_advance(models.AbstractModel):
    _name = 'report.skit_project.report_soil_penetration_document_advance'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.soil.penetration']
        datas = []
        x3=0
        x4=0
        for penet_id in docids:
            penetration = model.search([('id', '=', penet_id)])
            blow10 = self.env['skit.penetration.line.blow10'].search([
                                    ('penetration_id', '=', penetration.id)])
            blow30 = self.env['skit.penetration.line.blow30'].search([
                                    ('penetration_id', '=', penetration.id)])
            blow65 = self.env['skit.penetration.line.blow65'].search([
                                    ('penetration_id', '=', penetration.id)])
            b10_max_value = 0
            mdd =penetration.mdd
            omc=round((mdd *0.95),1)
            density_10 = round(penetration.dry_density_10,1)
            density_30 = round(penetration.dry_density_30,1)
            density_65 = round(penetration.dry_density_65,1)
            if mdd:

                if blow10:
                    for b10 in blow10:
                        if b10.std_cbr > b10_max_value:
                            b10_max_value = b10.std_cbr
                    datas.append({
                        "labels": density_10,
                        "vertical":density_10,
                        "vertical1":density_10,
                        "horizontal": mdd,
                        "horizontal1": omc,
                        "value": b10_max_value})
    
                # Get Max value of CBR in Blow30
                if blow30:
                    b30_max_value = 0
                    for b30 in blow30:
                        if b30.std_cbr > b30_max_value:
                            b30_max_value = b30.std_cbr
                    datas.append({"labels":density_30,
                                 "vertical":density_10,
                                 "vertical1":density_10,
                                 "horizontal": mdd,
                                 "horizontal1":omc,
                                 "value": b30_max_value,
                                  })
    
                # Get Max value of CBR in Blow65
                if blow65:
                    b65_max_value = 0
                    for b65 in blow65:
                        if b65.std_cbr > b65_max_value:
                            b65_max_value = b65.std_cbr
                    datas.append({"labels": density_65,
                                "vertical":density_10,
                                "vertical1":density_10,
                                "horizontal": mdd,
                                "horizontal1":omc,
                                "value": b65_max_value,
                                  })
                    
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
                
            
                if density_10 <=  omc <= density_30 or density_10 >=  omc >= density_30:
                    x1=b10_max_value
                    y1=density_10
                    x2=b30_max_value
                    y2 =density_30
                    if y1==y2 or x1==x2:
                        x4=0
                    else:
                        straight_y =omc
                        m=round((y2-y1)/(x2-x1),5)
                        b=round((y1-m*x1),3)
                        x4= (straight_y-b)/m
                   
             
                elif  density_30 <= omc <= density_65 or density_30 >= omc >= density_65:
                    x1=b30_max_value
                    y1=density_30
                    x2=b65_max_value
                    y2 =density_65
                    if y1==y2 or x1==x2:
                        x4=0
                    else:
                        straight_y =omc
                        m=round((y2-y1)/(x2-x1),5)
                        b=round((y1-m*x1),3)
                        x4= (straight_y-b)/m
    
                    
                datas.append({
                            "vertical":density_10,
                            "vertical1":density_10,
                            "value": x3,
                              })
                datas.append({
                              "vertical":density_30,
                              "vertical1":density_10,
                              "value": x3,
                              })
                datas.append({
                              "vertical":density_65,
                              "vertical1":density_10,
                              "value": x3,
                              })
                datas.append({
                              "vertical1":density_10,
                              "value": x4,
                              })
                datas.append({
                              "vertical1":density_30,
                              "value": x4,
                              })
                datas.append({
                              "vertical1":density_65,
                              "value": x4,
                              })
    
            else:
                if blow10:
                    for b10 in blow10:
                        if b10.std_cbr > b10_max_value:
                            b10_max_value = b10.std_cbr
                            datas.append({"value": round(penetration.dry_density_10, 1),
                             "labels": b10_max_value})

            # Get Max value of CBR in Blow30
                if blow30:
                    b30_max_value = 0
                    for b30 in blow30:
                        if b30.std_cbr > b30_max_value:
                            b30_max_value = b30.std_cbr
                    datas.append({"value": round(penetration.dry_density_30, 1),
                                  "labels": b30_max_value,
                                  })
                # Get Max value of CBR in Blow65
                if blow65:
                    b65_max_value = 0
                    for b65 in blow65:
                        if b65.std_cbr > b65_max_value:
                            b65_max_value = b65.std_cbr
                    datas.append({"value": round(penetration.dry_density_65, 1),
                                  "labels": b65_max_value,
                                  })
            if len(datas) >= 1:
                datas.append({"xaxis": "CBR VALUE %@ 100 % = "+str(penetration.cbr_100_per)+"% @ 95%  = " +str(penetration.cbr_99_per)+" % : Swell (%) =" +str(penetration.swell)})
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': penetration,
               'docs_line': blow10,
               'blow_30': blow30,
               'blow_65': blow65,
               'graph': datas,
            }

