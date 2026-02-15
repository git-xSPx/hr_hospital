from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError
from datetime import timedelta


class MedicalDiagnosis(models.Model):
    """Model to store medical diagnoses made during patient visits."""
    _name = 'hr.hospital.medical.diagnosis'
    _description = 'Medical Diagnosis'

    # Relation to the visit (required for cascading deletion)
    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Visit',
        ondelete='cascade',
        domain=lambda self: [
            ('state', '=', 'done'),
            ('actual_date', '>=', fields.Date.today() - timedelta(days=30))
        ],
        help='Only completed visits from the last 30 days are available for selection.',
        required=True
    )

    # Relation to the disease
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        domain="[('is_contagious', '=', True), ('danger_level', 'in', ['high', 'critical'])]",
        required=True
    )

    # Detailed descriptions
    description = fields.Text(string='Diagnosis Description')
    treatment = fields.Html(string='Prescribed Treatment')

    # Approval information
    is_approved = fields.Boolean(
        string='Approved',
        default=False
    )
    approved_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Approved By',
        readonly=True
    )
    approval_date = fields.Datetime(
        string='Approval Date',
        readonly=True
    )

    # Clinical details
    severity = fields.Selection(
        selection=[
            ('light', 'Light'),
            ('medium', 'Medium'),
            ('severe', 'Severe'),
            ('critical', 'Critical'),
        ],
        string='Severity Degree'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_approved'):
                visit = self.env['hr.hospital.visit'].browse(vals.get('visit_id'))
                self._check_approval_permission(vals, visit)
        return super(MedicalDiagnosis, self).create(vals_list)

    def write(self, vals):
        if vals.get('is_approved'):
            for diagnosis in self:
                self._check_approval_permission(vals, diagnosis.visit_id)
        return super(MedicalDiagnosis, self).write(vals)

    def _check_approval_permission(self, vals, visit):
        current_doctor = self.env['hr.hospital.doctor'].search([
            ('user_id', '=', self.env.user.id)
        ], limit=1)

        if not current_doctor:
            raise UserError(_("Only a registered doctor can approve diagnoses!"))

        author_doctor = visit.doctor_id

        if author_doctor.is_intern:
            # If autor is intern, commit approve diagnos can only his mentor
            if not author_doctor.mentor_id:
                raise UserError(_("Intern %s has no mentor. Approval impossible.") % author_doctor.full_name)

            if current_doctor.id != author_doctor.mentor_id.id:
                raise UserError(_(
                    "Only the assigned mentor (%s) can approve diagnoses for intern %s."
                ) % (author_doctor.mentor_id.full_name, author_doctor.full_name))
        else:
            # Autor is full graduate doctor
            if current_doctor.is_intern:
                raise UserError(_("An intern cannot approve a doctor's diagnosis!"))

        vals.update({
            'approved_doctor_id': current_doctor.id,
            'approval_date': fields.Datetime.now(),
        })
