# -*- coding: utf-8 -*-
{
    'name': "jt_product_attributeset",


    'summary': "Attribute set",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_attribute_set_views.xml',
        'views/product_attribute_views.xml',
        'views/product_template_views.xml',
    ],

}
