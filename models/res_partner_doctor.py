import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class HrHospitalDoctor(models.Model):
    _inherit = 'res.partner'

    is_hrh_doctor = fields.Boolean(
        string="Is Doctor",
        default=True,
    )

    hrh_doctor_specialty = fields.Char(
        string="Specialty",
    )
