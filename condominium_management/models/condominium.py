from odoo import models, fields, api


class Condominium(models.Model):
    _name = "condominium.condominium"
    _description = "Condominium"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin", "avatar.mixin"]

    name = fields.Char(required=True)
    rif = fields.Char(string="RIF", required=True)
    code = fields.Char()
    admin_id = fields.Many2one("res.partner", string="Administrador")
    address = fields.Text()
    phone = fields.Char()
    email = fields.Char()
    active = fields.Boolean(default=True)

    # Campo HTML para instrucciones de pago personalizables
    payment_instructions = fields.Html(
        string="Instrucciones de Pago",
        help="Instrucciones de pago que aparecerán en el recibo",
    )

    property_ids = fields.One2many(
        "condominium.property", "condominium_id", string="Propiedades"
    )
    employee_ids = fields.One2many(
        "condominium.employee", "condominium_id", string="Empleados"
    )
    service_ids = fields.One2many(
        "condominium.service", "condominium_id", string="Servicios"
    )

    @api.depends("name", "image_1920")
    def _compute_avatar_1920(self):
        super()._compute_avatar_1920()
