from odoo import api, fields, models, _

class ProductAttributeSet(models.Model):
    _name = 'product.attribute.set'
    _description = 'Product Attribute Set'

    name = fields.Char('Name', required=True, translate=True)
    attribute_id = fields.Many2one('product.attribute', string="Attribute", ondelete='cascade', required=True, index=True,)

    attribute_value_ids = fields.Many2many('product.attribute.value', string='Attribute values', domain="[('attribute_id', '=', attribute_id)]",)

    product_template_ids = fields.One2many('product.template', compute='_compute_product_template_ids', string='Product Templates')
    number_related_products = fields.Integer(compute='_compute_number_related_products')
    
    @api.depends('attribute_value_ids')
    def _compute_product_template_ids(self):
        for pas in self:
            templates = self.env['product.template.attribute.line'].search([('attribute_set_ids', 'in', pas.id)]).product_tmpl_id
            pas.product_template_ids = templates

    @api.depends('product_template_ids')
    def _compute_number_related_products(self):
        for pas in self:
            pas.number_related_products = len(pas.product_template_ids)            


    @api.onchange('attribute_id')
    def _onchange_attribute_id(self):
        self.attribute_value_ids = self.attribute_value_ids.filtered(lambda pav: pav.attribute_id == self.attribute_id)


    def ensure_attribute_set(self):
        for pas in self:
            for template in pas.product_template_ids:
                for ptal in template.attribute_line_ids:
                    ptal.ensure_attribute_set()


    def write(self, vals):
        res = super().write(vals)
        self.ensure_attribute_set()
        return res

    def action_open_related_products(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _("Related Products"),
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.product_template_ids.ids)],
        }        
