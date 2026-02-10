from odoo import models, fields


class Disease(models.Model):
    """Model to manage diseases with hierarchical structure and medical data."""
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Name', required=True)

    # Hierarchy (Simple version as requested)
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Disease',
        ondelete='cascade'
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases'
    )

    # Medical codes and classifications
    icd10_code = fields.Char(
        string='ICD-10 Code',
        size=10,
        help='International Statistical Classification of Diseases'
    )

    danger_level = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        string='Danger Level',
        default='low'
    )

    is_contagious = fields.Boolean(
        string='Contagious',
        help='Check if the disease is infectious'
    )

    symptoms = fields.Text(string='Symptoms')

    # Regional data
    country_ids = fields.Many2many(
        comodel_name='res.country',
        relation='disease_res_country_rel',
        column1='disease_id',
        column2='country_id',
        string='Spread Regions'
    )