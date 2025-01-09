from odoo.tests.common import TransactionCase
from odoo import exceptions

class TestBooking(TransactionCase):

    def setUp(self):
        super(TestBooking, self).setUp()

        # Tạo user cho nhóm Manager
        self.manager_user = self.env['res.users'].create({
            'name': 'Manager',
            'login': 'manager',
            'groups_id': [(6, 0, [self.env.ref('hotel.group_hotel_manager').id])]
        })

        # Tạo user cho nhóm Staff
        self.staff_user = self.env['res.users'].create({
            'name': 'Staff',
            'login': 'staff',
            'groups_id': [(6, 0, [self.env.ref('hotel.group_hotel_staff').id])]
        })

    def test_confirm_booking_as_manager(self):
        # Test trường hợp Manager có quyền tạo booking
        with self.env.cr.savepoint():
            self.env = self.env(user=self.manager_user)
            room = self.env['hotel.management.room'].create({'name': 'Room 101'})
            booking = self.env['hotel.management.booking'].create({
                'name': 'Test Booking',
                'check_in_date': '2025-01-01',
                'check_out_date': '2025-01-05',
                'bed_type': 'double',
                'room_id': room.id
            })
            booking.confirm_booking()
            self.assertEqual(booking.state, 'confirmed')

    def test_confirm_booking_as_staff(self):
        # Test trường hợp Staff không được phép tạo booking
        with self.env.cr.savepoint():
            self.env = self.env(user=self.staff_user)
            room = self.env['hotel.management.room'].create({'name': 'Room 102'})
            with self.assertRaises(exceptions.AccessError):
                self.env['hotel.management.booking'].create({
                    'name': 'Unauthorized Booking',
                    'check_in_date': '2025-01-01',
                    'check_out_date': '2025-01-05',
                    'bed_type': 'double',
                    'room_id': room.id
                })

    def test_cancel_booking_as_manager(self):
        # Test Manager có quyền hủy booking
        with self.env.cr.savepoint():
            self.env = self.env(user=self.manager_user)
            room = self.env['hotel.management.room'].create({'name': 'Room 103'})
            booking = self.env['hotel.management.booking'].create({
                'name': 'Test Booking Cancel',
                'check_in_date': '2025-01-01',
                'check_out_date': '2025-01-05',
                'bed_type': 'suite',
                'room_id': room.id
            })
            booking.state = 'confirmed'
            booking.write({'state': 'cancelled'})
            self.assertEqual(booking.state, 'cancelled')

    def test_cancel_booking_as_staff(self):
        # Test Staff không có quyền hủy booking
        with self.env.cr.savepoint():
            self.env = self.env(user=self.staff_user)
            room = self.env['hotel.management.room'].create({'name': 'Room 104'})
            booking = self.env['hotel.management.booking'].create({
                'name': 'Unauthorized Cancel',
                'check_in_date': '2025-01-01',
                'check_out_date': '2025-01-05',
                'bed_type': 'suite',
                'room_id': room.id
            })
            booking.state = 'confirmed'
            with self.assertRaises(exceptions.AccessError):
                booking.write({'state': 'cancelled'})

    def test_room_availability(self):
        # Test không cho phép đặt phòng đã được đặt trước
        with self.env.cr.savepoint():
            self.env = self.env(user=self.manager_user)
            room = self.env['hotel.management.room'].create({'name': 'Room 105'})
            self.env['hotel.management.booking'].create({
                'name': 'First Booking',
                'check_in_date': '2025-01-01',
                'check_out_date': '2025-01-05',
                'bed_type': 'double',
                'room_id': room.id,
                'state': 'confirmed'
            })
            with self.assertRaises(exceptions.ValidationError):
                self.env['hotel.management.booking'].create({
                    'name': 'Overlapping Booking',
                    'check_in_date': '2025-01-04',
                    'check_out_date': '2025-01-06',
                    'bed_type': 'double',
                    'room_id': room.id
                })

    def test_room_under_maintenance(self):
        # Test không cho phép đặt phòng đang bảo trì
        with self.env.cr.savepoint():
            self.env = self.env(user=self.manager_user)
            room = self.env['hotel.management.room'].create({
                'name': 'Room 106',
                'state': 'maintenance'
            })
            with self.assertRaises(exceptions.ValidationError):
                self.env['hotel.management.booking'].create({
                    'name': 'Booking Maintenance Room',
                    'check_in_date': '2025-01-01',
                    'check_out_date': '2025-01-05',
                    'bed_type': 'suite',
                    'room_id': room.id
                })