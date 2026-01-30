import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class HrHospitalPatient(models.Model):
    _inherit = 'res.partner'

    is_hrh_patient = fields.Boolean(
        string="Is Patient",
        default=True,
    )

    hrh_patient_birthday = fields.Date(
        string="Data of Birth",
    )

    hrh_patient_gender = fields.Selection(
        string="Gender",
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ]
    )

    hrh_patient_card_number = fields.Char(
        string="Card number",
    )
