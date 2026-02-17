from datetime import timedelta
from odoo import models, fields


class DoctorScheduleWizard(models.TransientModel):
    """Wizard to mass-generate doctor work schedules."""
    _name = 'hr.hospital.doctor.schedule.wizard'
    _description = 'Doctor Schedule Generation Wizard'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        required=True
    )
    start_week_date = fields.Date(
        string='Start Week (Monday)',
        required=True,
        help='Select any day; the system will find the Monday of that week.'
    )
    weeks_count = fields.Integer(
        string='Number of Weeks',
        default=1,
        required=True
    )
    schedule_type = fields.Selection([
        ('standard', 'Every Week'),
        ('even', 'Even Weeks Only'),
        ('odd', 'Odd Weeks Only')
    ], default='standard', required=True)

    # Days of the week
    mo = fields.Boolean('Mon')
    tu = fields.Boolean('Tue')
    we = fields.Boolean('Wed')
    th = fields.Boolean('Thu')
    fr = fields.Boolean('Fri')
    sa = fields.Boolean('Sat')
    su = fields.Boolean('Sun')

    # Working hours
    start_time = fields.Float('Work Starts', required=True)
    end_time = fields.Float('Work Ends', required=True)
    break_from = fields.Float()
    break_to = fields.Float()

    def action_generate(self):
        """Logic to generate hr.hospital.doctor.schedule records."""
        self.ensure_one()

        # Find the Monday of the starting week
        start_monday = (self.start_week_date
                        - timedelta(days=self.start_week_date.weekday()))
        days_mapping = [
            (self.mo, 0), (self.tu, 1), (self.we, 2),
            (self.th, 3), (self.fr, 4), (self.sa, 5), (self.su, 6)
        ]

        vals_list = []
        for week_idx in range(self.weeks_count):
            current_monday = start_monday + timedelta(weeks=week_idx)
            week_number = current_monday.isocalendar()[1]

            # Filter by Even/Odd week if necessary
            if self.schedule_type == 'even' and week_number % 2 != 0:
                continue
            if self.schedule_type == 'odd' and week_number % 2 == 0:
                continue

            for is_selected, day_index in days_mapping:
                if is_selected:
                    target_date = current_monday + timedelta(day_index)

                    vals_list.append({
                        'doctor_id': self.doctor_id.id,
                        'work_date': target_date,
                        'day_of_week': str(day_index),
                        'hour_from': self.start_time,
                        'hour_to': self.end_time,
                        'schedule_type': 'work',
                    })

        if vals_list:
            # Create all records
            self.env['hr.hospital.doctor.schedule'].create(vals_list)

        return {'type': 'ir.actions.act_window_close'}
