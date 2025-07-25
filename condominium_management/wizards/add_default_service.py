from odoo import models, fields, api

class AddServicesToBillWizard(models.TransientModel):
    _name = "add.services.to.bill.wizard"
    _description = "Agregar servicios por defecto al recibo"

    bill_id = fields.Many2one("condominium.bill", required=True)
    condominium_id = fields.Many2one(
        "condominium.condominium", related="bill_id.condominium_id", store=True
    )
    service_ids = fields.Many2many(
        "condominium.service", 
        string="Servicios a agregar",
        domain="[('condominium_id', '=', condominium_id)]"
    )

    def action_add_services(self):
        for wizard in self:
            for service in wizard.service_ids:
                self.env["condominium.bill.line"].create({
                    "bill_id": wizard.bill_id.id,
                    "description": service.name,
                    "total_amount": service.default_amount,
                    "how_applied": "fixed",  # o "alicuota" si aplica
                })
        return {'type': 'ir.actions.act_window_close'}