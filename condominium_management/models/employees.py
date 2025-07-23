from odoo import models, fields


class CondominiumEmployee(models.Model):
    _name = "condominium.employee"
    _description = "Empleado del Condominio"

    name = fields.Char(required=True)
    condominium_id = fields.Many2one("condominium.condominium", required=True)
    job_title = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    hire_date = fields.Date()
    active = fields.Boolean(default=True)
