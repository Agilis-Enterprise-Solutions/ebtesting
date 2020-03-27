# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models


class report_soil_aggregate_document(models.AbstractModel):
    _name = 'report.skit_project.report_soil_aggregate_document'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.soil.aggregate']
        for docid in docids:
            docs = model.search([('id', '=', docid)])
            analysis = self.env['sieve.analysis.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            consistency = self.env['soil.consistency.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            compaction = self.env['soil.compaction.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            abrasion = self.env['soil.abrasion.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            penetration = self.env['soil.penetration.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': docs,
               'docs_line1': analysis,
               'docs_line2': consistency,
               'docs_line3': compaction,
               'docs_line4': abrasion,
               'docs_line5': penetration}

class report_soil_aggregate_document_advance(models.AbstractModel):
    _name = 'report.skit_project.report_soil_aggregate_document_advance'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['skit.soil.aggregate']
        for docid in docids:
            docs = model.search([('id', '=', docid)])
            analysis = self.env['sieve.analysis.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            consistency = self.env['soil.consistency.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            compaction = self.env['soil.compaction.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            abrasion = self.env['soil.abrasion.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            penetration = self.env['soil.penetration.tab'].search([
                                            ('aggregate_id', '=', docs.id)])
            return {
               'doc_ids': docids,
               'doc_model': model,
               'data': data,
               'docs': docs,
               'docs_line1': analysis,
               'docs_line2': consistency,
               'docs_line3': compaction,
               'docs_line4': abrasion,
               'docs_line5': penetration}