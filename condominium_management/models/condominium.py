from odoo import models, fields


class Condominium(models.Model):
    _name = "condominium.condominium"
    _description = "Condominium"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    rif = fields.Char(string="RIF", required=True)
    code = fields.Char()
    admin_id = fields.Many2one("res.partner", string="Administrador")
    address = fields.Text()
    phone = fields.Char()
    email = fields.Char()
    image = fields.Image(string="Logo del Condominio")
    active = fields.Boolean(default=True)

    property_ids = fields.One2many(
        "condominium.property", "condominium_id", string="Propiedades"
    )
    employee_ids = fields.One2many(
        "condominium.employee", "condominium_id", string="Empleados"
    )
    service_ids = fields.One2many(
        "condominium.service", "condominium_id", string="Servicios"
    )
