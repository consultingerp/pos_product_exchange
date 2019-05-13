from odoo import models, fields, api, _

class ReportStockInventory(models.AbstractModel):
    _name = 'report.stock.report_inventory'
    
    def get_attribute_data(self, rec):
        result = []
        for rec in self.env['stock.inventory'].browse(rec):
            positive_qty = nagtive_qty = 0.0
            for line in rec.line_ids:
                if line.product_qty <= 0:
                    nagtive_qty += line.product_qty
                else:
                    positive_qty += line.product_qty
            result.append({'positive_qty': positive_qty, 'nagtive_qty': nagtive_qty})
#         for attribute_rec in order_id.product_attrib_ids:
#             attribute_vals = {}
#             if attribute_rec.product_id.id == product_id.id:
#                 attribute_vals.update({
#                     'attribute': attribute_rec.attrib_id.name,
#                     'value': attribute_rec.value
#                     })
#                 result.append(attribute_vals)
        return result
    
    @api.model
    def get_report_values(self, docids, data=None):
        report_inventory = self.env['ir.actions.report']._get_report_from_name('stock.report_inventory')
        stock_inventory_ids = self.env['stock.inventory'].browse(docids)
        return {
            'doc_ids': self.ids,
            'doc_model': report_inventory.model,
            'docs': stock_inventory_ids,
            'data': data,
            'get_attribute_data': self.get_attribute_data(docids),
        }
