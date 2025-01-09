{
    'name': 'Custom Hotel Management',
    'version': '18.0.1.0',
    'category': 'Hotel Management',
    'summary': 'Mở rộng chức năng của module quản lý khách sạn',
    'author': 'Akdemy_Le Chinh Dai',
    'license': 'LGPL-3',
    'depends': ['base', 'om_hotel'],  # Kế thừa từ module gốc
    'data': [
        'views/room_views.xml',
        'views/hotel_views.xml',
        'views/booking_history_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
