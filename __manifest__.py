{
    "name": "Hospital visit",
    "summary": "Odoo module for recording patient visits",
    "version": "19.0.1.3.1",
    "category": "Services",
    "website": "https://github.com/git-xSPx/hr_hospital",
    "author": "Serhii Pidopryhora",
    "license": "GPL-2",

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },


    "data": [
        'security/ir.model.access.csv',
        'data/hr_hospital_disease_data.xml',
    ],
    "demo": [
        'demo/res_partner_demo.xml',
    ],

    "installable": True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

}