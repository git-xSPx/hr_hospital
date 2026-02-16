{
    "name": "Hospital visit",
    "summary": "Odoo module for recording patient visits",
    "version": "19.0.1.4.1",
    "category": "Human Resources",
    "website": "https://github.com/git-xSPx/hr_hospital",
    "author": "Serhii Pidopryhora, "
    "Odoo Community Association (OCA)",
    "license": "GPL-2",

    'depends': [
        'base',
    ],

    "data": [
        'security/ir.model.access.csv',
        'data/hr_hospital_disease_data.xml',

        # Main models
        'views/hr_hospital_doctor_specialty_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',

        # Depend models
        'views/hr_hospital_contact_person_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_medical_diagnosis_views.xml',
        'views/hr_hospital_doctor_schedule_views.xml',
        'views/hr_hospital_patient_doctor_history_views.xml',

        # Wizards
        'wizard/hr_hospital_disease_report_wizard_view.xml',
        'wizard/hr_hospital_doctor_schedule_wizard_view.xml',
        'wizard/hr_hospital_mass_reassign_doctor_wizard_view.xml',
        'wizard/hr_hospital_patient_card_export_wizard_view.xml',
        'wizard/hr_hospital_reschedule_visit_wizard_view.xml',

        # Menus
        'views/hr_hospital_menus.xml'    ],
    "demo": [
        'demo/hr_hospital_doctor_specialty_demo.xml',
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
        'demo/hr_hospital_medical_diagnosis_demo.xml',
        'demo/hr_hospital_doctor_schedule_demo.xml',
        'demo/hr_hospital_patient_doctor_history_demo.xml',
    ],

    'images': [
        'static/description/icon.png'
    ],

}
