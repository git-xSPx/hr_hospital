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
        'views/hr_hospital_disease_view.xml',
        'views/hr_hospital_patient_view.xml',
        'views/hr_hospital_doctor_view.xml',
        'views/hr_hospital_visit_view.xml',
        'views/hr_hospital_menus.xml',
    ],
    "demo": [
        'demo/res_partner_demo.xml',
    ],

    'images': [
        'static/description/icon.png'
    ],

}
