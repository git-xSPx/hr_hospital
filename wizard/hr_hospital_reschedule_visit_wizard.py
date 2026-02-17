from datetime import datetime, time
from odoo import models, fields, api
from odoo.exceptions import UserError


class RescheduleVisitWizard(models.TransientModel):
    """Wizard to reschedule a patient visit to another date or doctor."""
    _name = 'hr.hospital.reschedule.visit.wizard'
    _description = 'Reschedule Visit Wizard'

    # Current visit info
    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Visit to Reschedule',
        # readonly=True
        required=True,
        domain="[('state', '=', 'scheduled')]"
    )

    # New appointment details
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
    )
    new_date = fields.Date(
        required=True
    )
    new_time = fields.Float(
        required=True,
        help='Time in float format (e.g., 14.5 for 14:30)'
    )

    reason = fields.Text(
        string='Reason for Rescheduling',
        required=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if (active_id
                and self.env.context.get('active_model') == 'hr.hospital.visit'):
            visit = self.env['hr.hospital.visit'].browse(active_id)
            # Default values from the current visit
            res.update({
                'visit_id': active_id,
                'new_doctor_id': visit.doctor_id.id,
                'new_date': visit.planned_date,
            })

            if 'new_time' in fields_list and hasattr(visit, 'planned_time'):
                res['new_time'] = visit.planned_time

        return res

    def action_reschedule(self):
        """Cancel old visit and create a new one."""
        self.ensure_one()
        old_visit = self.visit_id

        if not old_visit:
            raise UserError(
                self.env._("No active visit found to reschedule.")
            )

        # Archive or cancel the old visit
        old_visit.write({
            'state': 'cancelled',
        })

        hour = int(self.new_time)
        minute = int(round((self.new_time - hour) * 60))
        combined_datetime = datetime.combine(self.new_date, time(hour, minute))

        # Create a new visit record
        new_visit = self.env['hr.hospital.visit'].create({
            'patient_id': old_visit.patient_id.id,
            'doctor_id': self.new_doctor_id.id or old_visit.doctor_id.id,
            'planned_date': combined_datetime,
            'state': 'scheduled',
        })

        # Return action to open the newly created visit
        return {
            'name': self.env._('New Scheduled Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'res_id': new_visit.id,
            'view_mode': 'form',
            'target': 'current',
        }
