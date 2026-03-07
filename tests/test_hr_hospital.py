from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, AccessError


class TestHrHospital(TransactionCase):
    """Tests for hr_hospital module core logic and constraints."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Doctor = cls.env['hr.hospital.doctor']
        cls.Patient = cls.env['hr.hospital.patient']
        cls.Visit = cls.env['hr.hospital.visit']
        cls.User = cls.env['res.users']

        # 1. Create a basic Doctor
        cls.doctor_1 = cls.Doctor.create({
            'first_name': 'John',
            'last_name': 'Doe',
            'license_number': 'TEST-DOC-001',
        })

        # 2. Create an Intern Doctor
        cls.intern_1 = cls.Doctor.create({
            'first_name': 'Jane',
            'last_name': 'Smith',
            'license_number': 'TEST-INT-001',
            'is_intern': True,
            'mentor_id': cls.doctor_1.id,
        })

        # 3. Create a Patient
        cls.patient_1 = cls.Patient.create({
            'first_name': 'Mark',
            'last_name': 'Twain',
        })

    def test_visit_actual_date_constraint(self):
        """Test that actual_date cannot be earlier than planned_date."""
        planned = datetime.now() + timedelta(days=1)
        visit = self.Visit.create({
            'patient_id': self.patient_1.id,
            'doctor_id': self.doctor_1.id,
            'planned_date': planned,
            'state': 'scheduled',
        })

        # Try to set actual_date earlier than planned_date
        with self.assertRaises(ValidationError):
            visit.actual_date = planned - timedelta(hours=2)

    def test_doctor_mentor_constraint(self):
        """Test that an intern cannot be a mentor for another intern."""
        intern_2 = self.Doctor.create({
            'first_name': 'Bob',
            'last_name': 'Builder',
            'license_number': 'TEST-INT-002',
            'is_intern': True,
        })

        # Try to assign intern_1 as a mentor to intern_2
        with self.assertRaises(ValidationError):
            intern_2.mentor_id = self.intern_1.id

    def test_patient_access_rights(self):
        """Test that a user in Patient group cannot create visits."""
        # Get Patient group and Internal User group (required for login)
        patient_group = self.env.ref('hr_hospital.group_hr_hospital_patient')
        base_user_group = self.env.ref('base.group_user')

        # Create a test user with ONLY the Patient group
        # Create a test user with ONLY the Patient group
        patient_user = self.User.create({
            'name': 'Test Patient User',
            'login': 'test_patient',
            'group_ids': [(6, 0, [patient_group.id, base_user_group.id])]
        })

        # Switch environment to this new patient user
        visit_as_patient = self.Visit.with_user(patient_user)

        # Patient should get AccessError when trying to create a visit
        with self.assertRaises(AccessError):
            visit_as_patient.create({
                'patient_id': self.patient_1.id,
                'doctor_id': self.doctor_1.id,
                'planned_date': datetime.now() + timedelta(days=2),
                'state': 'scheduled',
            })
