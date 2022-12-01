{
    'name': 'Property Management',
    'version': '15.0.1.0.0',
    'sequence': -10,
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/property_menu_views.xml',
        'views/property_views.xml',
        'views/register_district.xml',
        'views/register_region.xml',
        'views/register_province.xml',
        'report/report.xml',
        'report/report_template.xml',
        'views/stock_picking_veiw.xml',
    ],
    'application': True,
    'installable': True
}
