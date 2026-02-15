from odoo import models, fields

class Country(models.Model):
    _inherit = 'res.country'

    default_lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Default Language',
        help='The main language spoken in this country'
    )