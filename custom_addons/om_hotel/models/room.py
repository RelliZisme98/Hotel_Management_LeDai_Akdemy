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
        one_week_ago = fields.Date.today() - timedelta(days=7)
        unrented_rooms = self.search([
            ('state', '=', 'available'),
            ('last_rented_date', '<', one_week_ago)
        ])
        if unrented_rooms:
            room_names = ', '.join(unrented_rooms.mapped('name'))
            message = f"The following rooms have not been rented for more than a week: {room_names}. Consider reducing prices."
            self.env['mail.message'].create({
                'subject': 'Unrented Rooms Notification',
                'body': message,
                'message_type': 'notification',
                'subtype_id': self.env.ref('mail.mt_comment').id,
                'partner_ids': self.env.user.partner_id.ids,
            })

            @api.model
            def notify_unrented_rooms(self):
                seven_days_ago = datetime.today() - timedelta(days=7)
                rooms = self.search([
                    ('state', '=', 'available'),
                    ('last_rented_date', '<', seven_days_ago)
                ])

                if rooms:
                    # Example: Send email or notification
                    mail_template = self.env.ref('om_hotel.email_template_unrented_rooms')
                    for room in rooms:
                        mail_template.send_mail(room.id, force_send=True)
                        _logger.info(f"Notification sent for room: {room.name}")
                    return True
                else:
                    _logger.info("No unrented rooms found.")
                    return False

