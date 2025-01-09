from odoo import models, fields
class HotelEmployee(models.Model):
    _inherit = 'hr.employee'

    manager_ids = fields.One2many(
        comodel_name="hotel.management.hotel",  # Model liên kết
        inverse_name="manager_id",  # Trường quan hệ trong model liên kết
        string="Hotels Managed")  # Nhãn hiển thị


# class HotelEmployee(models.Model):
#     _inherit = 'hr.employee'
#
#     manager_ids = fields.Many2many(
#         comodel_name="hotel.management.hotel",
#         relation="hotel_employee_rel",
#         column1="employee_id",
#         column2="hotel_id",
#         string="Hotels Managed"
#     )
#
# #
# class HotelEmployee2(models.Model):
#     _inherit = 'hr.employee'
#
#     # Quản lý có thể quản lý nhiều khách sạn
#     manager_hotel_ids = fields.One2many(
#         comodel_name="hotel.management.hotel",
#         inverse_name="manager_id",
#         string="Hotels Managed"
#     )