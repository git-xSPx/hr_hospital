import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Known diseases'

    name = fields.Char()

    active = fields.Boolean(
        default=True, )
    description = fields.Text()