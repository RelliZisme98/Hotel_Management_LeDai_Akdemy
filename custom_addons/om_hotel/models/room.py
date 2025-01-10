from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime
import logging
_logger = logging.getLogger(__name__)

class Room(models.Model):
    _name = 'hotel.management.room'
    _description = 'Room Management'

    name = fields.Char(string='Room Number', required=True)
    hotel_id = fields.Many2one('hotel.management.hotel', string='Hotel', required=True, ondelete='cascade')
    address = fields.Char(string='Hotel Address', related='hotel_id.address', store=True, readonly=True)
    bed_type = fields.Selection([('single', 'Single Bed'), ('double', 'Double Bed')], string='Bed Type', required=True)
    price = fields.Float(string='Room Price', required=True)
    feature_ids = fields.Many2many('hotel.management.room.feature', string='Room Features')
    state = fields.Selection([('available', 'Available'), ('booked', 'Booked'),('maintenance', 'Under Maintenance')], string='Room Status', default='available')
    last_rented_date = fields.Date(string='Last Rented Date', default=fields.Date.today)

    @api.model
    def write(self, vals):
        if 'state' in vals and vals['state'] == 'booked':
            vals['last_rented_date'] = fields.Date.today()
        return super(Room, self).write(vals)

    @api.constrains('bed_type')
    def _check_bed_type(self):
        valid_bed_types = ['single', 'double']
        for record in self:
            if record.bed_type not in valid_bed_types:
                raise ValidationError('Invalid bed type: %s' % record.bed_type)

    _sql_constraints = [
        ('unique_room_per_hotel', 'UNIQUE(name, hotel_id)', 'Room number must be unique within a hotel!'),
    ]

    @api.model
    def notify_unrented_rooms(self):
        _logger.info("Starting the notification process for unrented rooms.")
        seven_days_ago = fields.Date.today() - timedelta(days=7)
        unrented_rooms = self.search([
            ('state', '=', 'available'),
            ('last_rented_date', '<=', seven_days_ago)
        ])
        # if unrented_rooms:
        #     mail_template = self.env.ref('hotel_management.unrented_room_email_template')
        #     for room in unrented_rooms:
        #         if room.hotel_id.manager_id.email:
        #             _logger.info(f"Sending email for room: {room.name}")
        #             mail_template.with_context(
        #                 room_name=room.name,
        #                 hotel_name=room.hotel_id.name,
        #                 manager_email=room.hotel_id.manager_id. email
        #             ).send_mail(room.id, force_send=True)
        # else:
        #     _logger.info("No unrented rooms found.")
        # if unrented_rooms:
        #     for room in unrented_rooms:
        #         _logger.info(f"Processing notification for room: {room.name}")
        #         # Lấy email template
        #         template = self.env.ref('hotel_management.email_template_unrented_room', raise_if_not_found=False)
        #         if template:
        #             template.send_mail(room.id, force_send=True)
        #             _logger.info(f"Email notification sent for room: {room.name}")
        #         else:
        #             _logger.warning("Email template not found.")
        # else:
        #     _logger.info("No unrented rooms found.")
        # _logger.info(f"Seven days ago: {seven_days_ago}")
        # _logger.info(f"Rooms found matching criteria: {len(unrented_rooms)}")
        if unrented_rooms:
            for room in unrented_rooms:
                message = f"Room '{room.name}' in hotel '{room.hotel_id.name}' has not been rented for over a week."
                _logger.info(f"Notifying manager for room: {room.name}")
                if room.hotel_id.manager_id.user_id:
                    partner = room.hotel_id.manager_id.user_id.partner_id  # Lấy partner từ user_id
                    _logger.info(f"Partner found: {partner.name}, sending message...")
                    partner.message_post(
                        subject="Unrented Room Notification",
                        body=message,
                        message_type="notification",
                    )
                    _logger.info(f"Notification sent for room: {room.name}")
                else:
                    _logger.warning(f"Room {room.name} has no manager to notify.")
                _logger.info(f"Access attempt logged for room: {room.name}")
        else:
            _logger.info("No unrented rooms found.")
