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

class CondominiumPropertyCharge(models.Model):
    _name = "condominium.property.charge"
    _description = "Condominium Property Charge"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]

    name = fields.Char(compute="_compute_name", store=True)
    bill_id = fields.Many2one("condominium.bill", required=True)
    property_id = fields.Many2one("condominium.property", required=True)
    property_name = fields.Char(related="property_id.name", store=True)
    amount = fields.Float(required=True)
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )

    state = fields.Selection(
        [
            ("unpaid", "Pending"),
            ("paid", "Paid"),
            ("overdue", "Overdue"),
        ],
        default="unpaid",
        string="Payment Status",
    )

    payment_date = fields.Date(string="Payment Date")
    payment_method = fields.Char(string="Payment Method")
    due_date = fields.Date(string="Due Date")

    detail_lines = fields.One2many(
        "condominium.property.charge.detail",
        "property_charge_id",
        string="Detail Lines",
    )

    @api.depends("bill_id.name", "property_name")
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.property_name} - {rec.bill_id.name}"

    def action_mark_as_paid(self):
        for rec in self:
            rec.write(
                {
                    "state": "paid",
                    "payment_date": fields.Date.today(),
                }
            )

    def action_mark_as_overdue(self):
        for rec in self:
            rec.write({"state": "overdue", "payment_date": False})
    
    def action_mark_as_unpaid(self):
        for rec in self:
            rec.write({"state": "unpaid", "payment_date": False})


class CondominiumUnitChargeDetail(models.Model):
    _name = "condominium.property.charge.detail"
    _description = "Detail of Property Charge"

    property_charge_id = fields.Many2one("condominium.property.charge")
    description = fields.Char()
    amount = fields.Float()