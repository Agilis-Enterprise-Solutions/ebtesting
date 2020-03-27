# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models


class report_sieve_analysis_document(models.AbstractModel):
    _name = 'report.skit_project.report_sieve_analysis_document'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.sieve.analysis']
        for sieve_id in docids:
            sieve = model.search([('id', '=', sieve_id)])
            sieve_line = self.env['skit.sieve.analysis.line'].search([
                                        ('analysis_id', '=', sieve.id)])
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': sieve,
               'docs_line': sieve_line}
            
            
            
class report_sieve_analysis_document_advance(models.AbstractModel):
    _name = 'report.skit_project.report_sieve_analysis_document_advance'

    
    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.sieve.analysis']
        for sieve_id in docids:
            sieve = model.search([('id', '=', sieve_id)])
            sieve_line = self.env['skit.sieve.analysis.line'].search([
                                        ('analysis_id', '=', sieve.id)])
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': sieve,
               'docs_line': sieve_line
               }