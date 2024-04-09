import logging
from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)



class ProductAttribute(models.Model):
    _inherit = "product.attribute"  

    number_related_attribute_sets = fields.Integer(compute='_compute_number_related_attribute_sets', string='Number Related Attribute Sets')

    attribute_set_ids = fields.One2many('product.attribute.set', 'attribute_id', string='Attribute Set')

    @api.depends('attribute_set_ids')
    def _compute_number_related_attribute_sets(self):
        for pa in self:
            pa.number_related_attribute_sets = len(pa.attribute_set_ids)

    def action_open_related_attribute_sets(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _("Related Attribute Sets"),
            'res_model': 'product.attribute.set',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.attribute_set_ids.ids)],
            'context': {
                'default_attribute_id': self.id
            }
        }

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    
    attribute_set_ids = fields.Many2many('product.attribute.set', string='Attribute sets', domain="[('attribute_id', '=', attribute_id)]", ondelete='restrict')


class ProductTemplateAttributeLine(models.Model):
    _inherit = 'product.template.attribute.line'   

    attribute_set_type = fields.Selection([
        ('default', 'Default'),
        ('set', 'Attribute Set only'),
        ('mixed', 'Mixed'),
    ], string='Attribute Set Type', default='default', required=True)

    attribute_set_ids = fields.Many2many('product.attribute.set', string='Attribute sets', domain="[('attribute_id', '=', attribute_id)]", ondelete='restrict')

    @api.onchange('attribute_set_type')
    def _onchange_attribute_set_type(self):
        for ptal in self:
            if ptal.attribute_set_type == 'default':
                ptal.attribute_set_ids = [(5,0,0)]
            ptal.ensure_attribute_set()


    @api.onchange('attribute_set_ids')
    def _onchange_attribute_set_ids(self):
        for ptal in self:
            ptal.ensure_attribute_set()

    def ensure_attribute_set(self):
        for ptal in self:
            if ptal.attribute_set_type in ['set','mixed']:
                template = ptal.product_tmpl_id
                _logger.info("Template: %s", template.name)
                for attribute_set in ptal.attribute_set_ids:
                    _logger.info("Attribute set: %s", attribute_set.name)                
                    for value in attribute_set.attribute_value_ids:
                        _logger.info("Attribute value %s", value.name) 
                        if value not in ptal.value_ids:
                            _logger.info(" -> does not exist yet, adding ...")
                            ptal.value_ids = [(4, value.id)]
                        else:
                            _logger.info(" -> found")
                if ptal.attribute_set_type == 'set':
                    for value in ptal.value_ids:
                        if value not in ptal.attribute_set_ids.attribute_value_ids:
                            _logger.info("Attribute value %s : removing", value.name) 
                            ptal.value_ids = [(3, value.id)]

