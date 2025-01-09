from odoo import models, fields

class Room(models.Model):
    _inherit = 'hotel.management.room'

    size = fields.Float(string="Kích thước phòng (m2)")
    max_people = fields.Integer(string="Số người tối đa")
    smoking_allowed = fields.Selection(
        [('yes', 'Có'), ('no', 'Không')],
        string="Cho hút thuốc",
        default='no'
    )
