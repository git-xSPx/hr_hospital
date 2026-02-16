from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Disease Report Wizard'

    # Filters
    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Doctors')
    disease_ids = fields.Many2many('hr.hospital.disease', string='Diseases')
    country_ids = fields.Many2many('res.country', string='Countries of Citizenship')

    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)

    report_type = fields.Selection([
        ('detail', 'Detailed'),
        ('summary', 'Summary')
    ], string='Report Type', default='detail', required=True)

    group_by = fields.Selection([
        ('doctor_id', 'Doctor'),
        ('disease_id', 'Disease'),
        ('country', 'Country')
    ], string='Group By', default='disease_id')

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start > record.date_end:
                raise ValidationError(_("Start date cannot be later than end date!"))

    def action_generate_report(self):
        self.ensure_one()

        # Base filter
        domain = [
            ('visit_id.actual_date', '>=', self.date_start),
            ('visit_id.actual_date', '<=', self.date_end),
        ]

        # Add selected filters
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        if self.country_ids:
            domain.append(('visit_id.patient_id.country_id', 'in', self.country_ids.ids))

        # Return action
        action = {
            'name': _('Disease Report Results'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.medical.diagnosis',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
            'context': {'expand': 1},
        }

        # Adding grouping
        if self.group_by:
            group_field = self.group_by
            if group_field == 'country':
                group_field = 'visit_id.patient_id.country_id'
            action['context'].update({'group_by': group_field})

        return action