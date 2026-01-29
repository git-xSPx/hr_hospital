import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit to doctor'

    active = fields.Boolean(
        default=True, )

    visit_date = fields.Datetime(
        string="Visit Date",
        default=fields.Datetime.today(),
    )

    res_partner_patient_id = fields.Many2one(
        comodel_name='res.partner',
        string="Patient",
        domain=[('is_hrh_patient', '=', True)]
    )

    res_partner_doctor_id = fields.Many2one(
        comodel_name='res.partner',
        string="Doctor",
        domain=[('is_hrh_doctor', '=', True)]
    )

    hr_hospital_disease_id = fields.Many2one(
        comodel_name='hr.hospital',
        string="Disease",
    )

    description = fields.Text()