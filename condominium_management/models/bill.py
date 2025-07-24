from odoo import models, fields, api


class CondominiumBill(models.Model):
    _name = "condominium.bill"
    _description = "Condominium Bill"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]

    name = fields.Char(compute="_compute_name", store=True)
    condominium_id = fields.Many2one("condominium.condominium", required=True)
    date = fields.Date(required=True, default=fields.Date.today)
    period = fields.Char(help="Example: Jul. 2025")
    due_date = fields.Date(string="Due Date")
    amount = fields.Float(compute="_compute_amount", store=True, readonly=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("calculated", "Amounts Generated"),
            ("done", "Done"),
        ],
        default="draft",
    )

    line_ids = fields.One2many("condominium.bill.line", "bill_id", string="Expenses")
    unit_charge_ids = fields.One2many(
        "condominium.property.charge", "bill_id", string="Unit Charges"
    )

    @api.depends("condominium_id", "date")
    def _compute_name(self):
        for rec in self:
            rec.name = (
                f"Receipt - {rec.date.strftime('%B %Y')}"
            )

    @api.depends("line_ids.total_amount")
    def _compute_amount(self):
        for rec in self:
            rec.amount = sum(line.total_amount for line in rec.line_ids)

    def action_calculate_charges(self):
        for bill in self:
            bill.unit_charge_ids.unlink()
            total_services = bill.line_ids
            units = bill.condominium_id.property_ids.filtered(lambda u: u.alicuota > 0)

            for unit in units:
                total_unit = 0.0
                detail_vals = []
                for line in total_services:
                    if line.how_applied == "fixed":
                        service_share = line.total_amount
                    else:
                        # Calculate by alicuota
                        service_share = line.total_amount * (unit.alicuota / 100)
                    total_unit += service_share
                    detail_vals.append(
                        (
                            0,
                            0,
                            {"description": line.description, "amount": service_share},
                        )
                    )
                self.env["condominium.property.charge"].create(
                    {
                        "bill_id": bill.id,
                        "property_id": unit.id,
                        "amount": total_unit,
                        "due_date": bill.due_date,
                        "detail_lines": detail_vals,
                    }
                )
            bill.state = "calculated"


class CondominiumBillLine(models.Model):
    _name = "condominium.bill.line"
    _description = "Condominium Bill Line"

    bill_id = fields.Many2one("condominium.bill", required=True)
    description = fields.Char()
    how_applied = fields.Selection(
        [("fixed", "Fixed Amount"), ("alicuota", "By alicuota")],
        required=True,
        default="alicuota",
    )
    total_amount = fields.Float(required=True)


class CondominiumPropertyCharge(models.Model):
    _name = "condominium.property.charge"
    _description = "Condominium Property Charge"

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

    def action_mark_as_paid(self):
        for rec in self:
            rec.write(
                {
                    "state": "paid",
                    "payment_date": fields.Date.today(),
                }
            )


class CondominiumUnitChargeDetail(models.Model):
    _name = "condominium.property.charge.detail"
    _description = "Detail of Property Charge"

    property_charge_id = fields.Many2one("condominium.property.charge")
    description = fields.Char()
    amount = fields.Float()
