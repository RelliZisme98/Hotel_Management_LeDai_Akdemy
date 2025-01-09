# from odoo import models, api
# from odoo.exceptions import AccessError
#
# class BookingAccess(models.Model):
#     _inherit = 'hotel.management.booking'
#
#     @api.model
#     def create(self, vals):
#         # Chỉ cho phép Manager tạo booking
#         if not self.env.user.has_group('hotel.group_hotel_manager'):
#             raise AccessError('Only managers can create bookings.')
#         return super(BookingAccess, self).create(vals)
#
#     def write(self, vals):
#         # Chỉ cho phép Manager hủy booking
#         if 'state' in vals and vals['state'] == 'cancelled' and not self.env.user.has_group('hotel.group_hotel_manager'):
#             raise AccessError('Only managers can cancel bookings.')
#         return super(BookingAccess, self).write(vals)