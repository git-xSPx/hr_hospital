import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class HrHospitalDoctor(models.Model):
    _inherit = 'res.partner'

    is_hrh_doctor = fields.Boolean(
        string="Is Doctor",
        store=True,
        # default=True,
    )

    hrh_doctor_specialty = fields.Char(
        string="Specialty",
    )

    hrh_senior_doctor_id = fields.Many2one(
        'res.partner',
        string="Attending Doctor",
        domain=[('is_hrh_doctor', '=', True)],
        help="The chief doctor or mentor for this doctor"
    )