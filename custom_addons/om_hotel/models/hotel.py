from odoo import models, fields, api


class Hotel(models.Model):
    _name = 'hotel.management.hotel'
    _description = 'Hotel Management'

    name = fields.Char(string='Hotel Name', required=True)
    address = fields.Char(string='Hotel Address', required=True)
    floor_count = fields.Integer(string='Number of Floors', required=True)
    room_count = fields.Integer(string='Number of Rooms', compute='_compute_room_count', store=True)
    room_ids = fields.One2many('hotel.management.room', 'hotel_id', string='Rooms')
    booking_ids = fields.One2many('hotel.management.booking', 'hotel_id', string='Booking History')
    # customer_name = fields.Char(related='booking_ids.customer_name', string='Customer Name', store=True)

    # Trường này sẽ liên kết với nhân viên để chỉ định người quản lý khách sạn, 1 khách sạn có 1 người quản lý
    manager_id = fields.Many2one('hr.employee', string='Manager')
    # Một khách sạn có thể có nhiều nhân viên
    employee_ids = fields.Many2many('hr.employee',  string="Employees")


    # # Admin chỉ định khách sạn cho Manager
    # ref = fields.Char(string='Reference')

    @api.depends('room_ids')
    def _compute_room_count(self):
        for hotel in self:
            hotel.room_count = len(hotel.room_ids)

    _sql_constraints = [
        ('unique_hotel_name', 'unique(name)', 'Hotel Name must be unique!')
    ]
    @api.constrains('floor_count')
    def _onchange_floor_count(self):
        if self.floor_count < 1:
            raise models.ValidationError("Number of floors must be greater than 0.")

