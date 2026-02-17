from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Disease(models.Model):
    """Model to manage diseases with full hierarchical structure."""
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    # Enable Odoo hierarchical features
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'  # Show full path in searches
    _order = 'complete_name'

    name = fields.Char(required=True)

    # Special field for fast hierarchy traversal
    parent_path = fields.Char(index=True, unaccent=False)

    complete_name = fields.Char(
        string='Full Name',
        compute='_compute_complete_name',
        recursive=True,
        store=True
    )

    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Category',
        ondelete='cascade',
        index=True
    )

    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Sub-diseases'
    )

    icd10_code = fields.Char(string='ICD-10 Code', size=10)
    danger_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='low')

    is_contagious = fields.Boolean(string='Contagious')
    symptoms = fields.Text()

    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Spread Regions'
    )

    @api.constrains('parent_id')
    def _check_disease_recursion(self):
        if not self._check_recursion():
            raise ValidationError(self.env._("Error! You cannot create recursive hierarchy."))

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for disease in self:
            if disease.parent_id:
                disease.complete_name = f"{disease.parent_id.complete_name} / {disease.name}"
            else:
                disease.complete_name = disease.name
