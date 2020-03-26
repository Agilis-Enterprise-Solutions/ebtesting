# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models


class report_soil_abrasion_document(models.AbstractModel):
    _name = 'report.skit_project.report_soil_abrasion_document'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.soil.abrasion']
        for abrasion_id in docids:
            soil_abrasion = model.search([('id', '=', abrasion_id)])
            abrasion = self.env['skit.abrasion'].search([
                ('abrasion_id', '=', soil_abrasion.id)])
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': soil_abrasion,
               'docs_line': abrasion}

class report_soil_abrasion_document_advance(models.AbstractModel):
    _name = 'report.skit_project.report_soil_abrasion_document_advance'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.soil.abrasion']
        for abrasion_id in docids:
            soil_abrasion = model.search([('id', '=', abrasion_id)])
            abrasion = self.env['skit.abrasion'].search([
                ('abrasion_id', '=', soil_abrasion.id)])
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': soil_abrasion,
               'docs_line': abrasion}
