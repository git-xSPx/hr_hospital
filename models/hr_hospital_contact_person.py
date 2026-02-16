from odoo import models, fields, api
from odoo.tools.translate import _


class ContactPerson(models.Model):
    _name = 'hr.hospital.contact.person'
    _description = 'Contact Person'
    _inherit = ['hr.hospital.person']

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Related Patient',
        required=True,
        domain="[('allergies', '!=', False)]",
        help='Select a patient who has allergy information recorded.'
    )

    relationship = fields.Char(
        string='Relationship',
        help='e.g., Parent, Spouse, Guardian'
    )

    @api.depends('last_name', 'first_name')
    def _compute_display_name(self):
        for patient in self:
            name = f"{patient.last_name or ''} {patient.first_name or ''}".strip()
            patient.display_name = name or _("New Contact Person")
