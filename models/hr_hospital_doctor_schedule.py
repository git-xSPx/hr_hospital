from odoo import models, fields


class DoctorSchedule(models.Model):
    """Model to manage doctor's working hours and events."""
    _name = 'hr.hospital.doctor.schedule'
    _description = 'Doctor Schedule'
    _order = 'work_date, hour_from'

    # Relation to doctor
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        required=True,
        domain="[('specialty_id', '!=', False)]",
        ondelete='cascade'
    )

    # Date and Weekday information
    day_of_week = fields.Selection(
        selection=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday'),
        ],
        string='Day of Week'
    )
    work_date = fields.Date(
        string='Specific Date',
        help='Specific date for this schedule entry'
    )

    # Working hours (Float is standard for time in Odoo)
    hour_from = fields.Float(
        string='Start Time',
        help='Work start hour (e.g., 8.5 for 08:30)'
    )
    hour_to = fields.Float(
        string='End Time',
        help='Work end hour (e.g., 17.0 for 17:00)'
    )

    # Type of schedule entry
    schedule_type = fields.Selection(
        selection=[
            ('work', 'Working Day'),
            ('vacation', 'Vacation'),
            ('sick', 'Sick Leave'),
            ('conference', 'Conference'),
        ],
        string='Type',
        default='work',
        required=True
    )

    notes = fields.Char()

    _sql_constraints = [
        ('check_hours',
         'CHECK(hour_to > hour_from)',
         'The end time must be later than the start time!')
    ]
