from odoo import models, fields

class BookingHistory(models.Model):
    _name = 'hotel.booking.history'
    _description = 'Lịch sử đặt phòng'

    booking_reference = fields.Char(string="Mã đặt phòng")
    customer_name = fields.Char(string="Tên khách đặt")
    hotel_id = fields.Many2one('hotel.management.hotel', string="Khách sạn")
    room_id = fields.Many2one('hotel.management.room', string="Phòng")
    check_in_date = fields.Date(string="Ngày Check-in")
    check_out_date = fields.Date(string="Ngày Check-out")
