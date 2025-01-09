from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoomFeature(models.Model):
    _name = 'hotel.management.room.feature'
    _description = 'Room Feature'

    name = fields.Char(string='Feature Name', required=True)

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing:
                raise ValidationError(f"The feature name '{record.name}' already exists.")

    _sql_constraints = [
        ('unique_feature_name', 'UNIQUE(name)', 'Feature name must be unique!'),
    ]