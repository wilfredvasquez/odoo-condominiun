from odoo import models, fields, api


class CondominiumProperty(models.Model):
    _name = "condominium.property"
    _description = "Propiedad de Condominio"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    type = fields.Selection(
        [
            ("apartment", "Apartment"),
            ("commercial", "Commercial"),
            ("other", "Other"),
        ],
        string="Property Type",
        required=True,
    )
    tower = fields.Char(string="Tower")
    floor = fields.Char(string="Floor")
    condominium_id = fields.Many2one("condominium.condominium", required=True)
    owner_id = fields.Many2one("res.partner", string="Owner")
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    surface = fields.Float(string="Surface (m2)")
    alicuota = fields.Float(string="Alícuota (%)", digits=(8, 4), required=True)
    active = fields.Boolean(default=True)
    charge_ids = fields.One2many(
        "condominium.property.charge", "property_id", string="Receipt/Charges"
    )
    total_debt = fields.Float(
        string="Total Debt",
        compute="_compute_total_debt",
        store=True,
    )

    @api.depends("charge_ids.state", "charge_ids.amount")
    def _compute_total_debt(self):
        for rec in self:
            rec.total_debt = sum(
                charge.amount
                for charge in rec.charge_ids
                if charge.state in ["unpaid", "overdue"]
            )