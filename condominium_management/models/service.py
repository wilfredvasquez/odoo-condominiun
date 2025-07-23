from odoo import models, fields


class CondominiumService(models.Model):
    _name = "condominium.service"
    _description = "Servicio o Gasto Común"

    name = fields.Char(required=True)
    description = fields.Text()
    default_amount = fields.Float()
    active = fields.Boolean(default=True)
    condominium_id = fields.Many2one("condominium.condominium")
