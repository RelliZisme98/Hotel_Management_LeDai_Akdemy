from odoo import models, fields, api
from datetime import date
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError
from odoo import exceptions


class Booking(models.Model):
    _name = 'hotel.management.booking'
    _description = 'Booking Management'

    name = fields.Char(string='Booking Reference', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('booking.sequence'))
    customer_name = fields.Char(string='Customer Name', required=True)

    booking_date = fields.Date(string='Booking Date', default=fields.Date.today)
    hotel_id = fields.Many2one('hotel.management.hotel', string='Hotel', required=True)
    room_type = fields.Selection([('single', 'Single Bed'), ('double', 'Double Bed')], string='Room Type', required=True)
    room_id = fields.Many2one('hotel.management.room', string='Room', domain="[('hotel_id', '=', hotel_id), ('bed_type', '=', room_type), ('state', '=', 'available')]", required=True)
    check_in_date = fields.Date(string='Check-in Date', required=True)
    check_out_date = fields.Date(string='Check-out Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')], string='Booking Status', default='draft')

    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for record in self:
            if record.check_in_date > record.check_out_date:
                raise ValidationError('Check-out date must be after check-in date!')

    # đảm bảo không đặt phòng đã được đặt trong khoảng thời gian khác:
    @api.constrains('check_in_date', 'check_out_date', 'room_id')
    def _check_room_availability(self):
        for record in self:
            overlapping_bookings = self.env['hotel.management.booking'].search([
                ('room_id', '=', record.room_id.id),
                ('state', '=', 'confirmed'),
                ('check_in_date', '<', record.check_out_date),
                ('check_out_date', '>', record.check_in_date),
                ('id', '!=', record.id),
            ])
            if overlapping_bookings:
                raise exceptions.ValidationError(
                    f"Room {record.room_id.name} is already booked for the selected dates."
                )
 # ensures the validity of the booking dates
    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for record in self:
            if record.check_in_date > record.check_out_date:
                raise ValidationError('Check-out date must be after check-in date!')
            if record.check_in_date < fields.Date.today():
                raise ValidationError('Check-in date cannot be in the past!')
            if record.check_out_date < fields.Date.today():
                raise ValidationError('Check-out date cannot be in the past!')

    # Không cho phép đặt phòng nếu trạng thái phòng không phải là 'available':
    @api.constrains('room_id')
    def _check_room_state(self):
        for record in self:
            if record.room_id.state != 'available':
                raise ValidationError(
                    f"Room {record.room_id.name} is not available for booking."
                )
 # Đảm bảo không đặt phòng đang bảo trì:
    @api.model
    def create(self, vals):
        room = self.env['hotel.management.room'].browse(vals.get('room_id'))
        if room.state == 'maintenance':
            raise ValidationError(f"Room {room.name} is under maintenance and cannot be booked.")
        return super(Booking, self).create(vals)
    
# Đảm bảo khi booking được confirm thì trạng thái của phòng cũng được cập nhật:

    def confirm_booking(self):
        for record in self:
            _logger.info('Booking confirmed: %s by user %s', record.name, self.env.user.name)
            record.state = 'confirmed'
            record.room_id.state = 'booked'
    
            # Create a booking history record
            self.env['hotel.booking.history'].create({
                'customer_name': record.customer_name,
                'hotel_id': record.hotel_id.id,
                'room_id': record.room_id.id,
                'check_in_date': record.check_in_date,
                'check_out_date': record.check_out_date,
                'state': 'confirmed',
            })


    def cancel_booking(self):
        for record in self:
            _logger.info('Booking cancelled: %s by user %s', record.name, self.env.user.name)
            record.state = 'cancelled'
            record.room_id.state = 'available'  # Update room status to 'available'