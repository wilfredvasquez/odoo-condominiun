from odoo import models, fields


class CondominiumProperty(models.Model):
    _name = "condominium.property"
    _description = "Propiedad de Condominio"

    name = fields.Char(required=True)
    number = fields.Char()
    condominium_id = fields.Many2one("condominium.condominium", required=True)
    owner_id = fields.Many2one("res.partner", string="Propietario")
    tenant_id = fields.Many2one("res.partner", string="Inquilino")
    surface = fields.Float(string="Área (m2)")
    alicuota = fields.Float(string="Alícuota (%)", required=True)
    active = fields.Boolean(default=True)
