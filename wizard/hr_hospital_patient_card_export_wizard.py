import json
import base64
import csv
import io
from odoo import models, fields, api


class PatientCardExportWizard(models.TransientModel):
    """Wizard to export patient medical data in JSON or CSV format."""
    _name = 'hr.hospital.patient.card.export.wizard'
    _description = 'Patient Card Export Wizard'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        required=True
    )
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')

    include_diagnoses = fields.Boolean(
        default=True
    )
    include_recommendations = fields.Boolean(
        default=True
    )

    lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Report Language'
    )

    export_format = fields.Selection([
        ('json', 'JSON'),
        ('csv', 'CSV')
    ], default='json', required=True)

    # Fields to store the generated file
    file_data = fields.Binary(string='File', readonly=True)
    file_name = fields.Char(readonly=True)

    @api.model
    def default_get(self, fields_list):
        """Set default patient and their language from context."""
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if (active_id
                and self.env.context.get('active_model') == 'hr.hospital.patient'):
            patient = self.env['hr.hospital.patient'].browse(active_id)
            res.update({
                'patient_id': patient.id,
                'lang_id': patient.lang_id.id if patient.lang_id else False,
            })
        return res

    def action_export(self):

        self.ensure_one()

        # Find diagnoses based on filters
        domain = [('visit_id.patient_id', '=', self.patient_id.id)]
        if self.date_from:
            domain.append(('visit_id.actual_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('visit_id.actual_date', '<=', self.date_to))

        diagnoses = self.env['hr.hospital.medical.diagnosis'].search(domain)

        data = []
        for diag in diagnoses:
            item = {
                'date': str(diag.visit_id.actual_date),
                'doctor': diag.visit_id.doctor_id.display_name,
            }
            if self.include_diagnoses:
                item['disease'] = diag.disease_id.name
                item['description'] = diag.description or ""
            if self.include_recommendations:
                item['treatment'] = diag.treatment or ""
            data.append(item)

        # Generate file content
        if self.export_format == 'json':
            content = json.dumps(data, indent=4, ensure_ascii=False)
            self.file_data = base64.b64encode(content.encode('utf-8'))
            self.file_name = f"patient_card_{self.patient_id.last_name}.json"

        elif self.export_format == 'csv':
            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            self.file_data = base64.b64encode(output.getvalue().encode('utf-8'))
            self.file_name = f"patient_card_{self.patient_id.last_name}.csv"

        # Return the wizard form to show the download link
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
