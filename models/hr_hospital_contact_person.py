from odoo import models, fields


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
