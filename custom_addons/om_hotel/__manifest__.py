{
    "name": "Hotel Management System",
    "author": "Akdemy_Le Chinh Dai",
    "license": "LGPL-3",
    "version": "18.0.1.0",
    'depends': ['base', 'mail', 'hr'],
    'data': [
        # Security
        'security/hotel_security.xml',
        'data/hotel_users.xml',
        'security/hotel_record_rules.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',  # Cron job

        # Views
        'views/hotel_views.xml',
        'views/room_views.xml',
        'views/room_feature_views.xml',
        'views/booking_views.xml',
        # 'views/hotel_employee_views.xml',
        'views/menu.xml',
    ],
    'test': [
        'tests/test_booking_access.py',
    ],
}