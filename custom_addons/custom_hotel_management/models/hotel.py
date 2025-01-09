
from odoo import api, models, fields

class Hotel(models.Model):
    _inherit = 'hotel.management.hotel'
    search_customer_name = fields.Char(string="Search by Customer Name")
    booking_ids = fields.One2many('hotel.management.booking', 'hotel_id', string="Booking History")
    room_id = fields.Many2one('hotel.management.room', string="Room")

    @api.onchange('search_customer_name')
    def _onchange_booking_info(self):
        booking = False
        if self.search_customer_name:
            # Tìm kiếm gần đúng với customer name
            booking = self.env['hotel.management.booking'].search([
                ('customer_name', 'ilike', self.search_customer_name)
            ], limit=1)

        if booking:
            # Cập nhật các thông tin khi tìm thấy booking
            self.name = booking.hotel_id.name
            self.booking_ids = [(5, 0, 0)] + [(0, 0, {
                'customer_name': booking.customer_name,
                'room_id': booking.room_id.id,
                'check_in_date': booking.check_in_date,
                'check_out_date': booking.check_out_date
            })]
        else:
            # Không tìm thấy, xóa các booking đã có và thông báo
            self.booking_ids = [(5, 0, 0)]
            if not  self.search_customer_name:
                # Nếu không có bất kỳ giá trị tìm kiếm nào, không cần thông báo
                return
            else:
                # Thông báo người dùng nếu không tìm thấy booking
                return {
                    'warning': {
                        'title': 'No Results Found',
                        'message': 'No booking found matching the search criteria.'
                    }
                }
    # @api.onchange('search_booking_reference', 'search_customer_name')
    # def _onchange_booking_info(self):
    #     if self.search_booking_reference:
    #         booking = self.env['hotel.management.booking'].search([('booking_reference', '=', self.search_booking_reference)], limit=1)
    #     elif self.search_customer_name:
    #         booking = self.env['hotel.management.booking'].search([('customer_name', '=', self.search_customer_name)], limit=1)
    #     else:
    #         booking = False
    #
    #     if booking:
    #         self.name = booking.hotel_id.name
    #         self.booking_ids = [(5, 0, 0)] + [(0, 0, {
    #             'customer_name': booking.customer_name,
    #             'room_id': booking.room_id.id,
    #             'check_in_date': booking.check_in_date,
    #             'check_out_date': booking.check_out_date
    #         })]
    #     else:
    #         self.booking_ids = [(5, 0, 0)]
