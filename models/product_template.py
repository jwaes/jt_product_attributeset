import logging
from odoo import api, fields, models


_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    # def write(self, vals):
    #     res = super(ProductTemplate, self).write(vals)
    #     changed = False
    #     if 'attribute_line_ids' and 'attribute_line_ids.attribute_set_ids':
    #         template = self
    #         for line in template.attribute_line_ids:
    #             if line.attribute_set_type in ['set','mixed']:
    #                 for attribute_set in line.attribute_set_ids:
    #                     _logger.info("Attribute set: %s", attribute_set.name)                
    #                     for value in attribute_set.attribute_value_ids:
    #                         _logger.info("Attribute value %s", value.name)
    #                         # if value not in template.attribute_line_ids.value_ids:
    #                         #     _logger.info(" -> does not exist yet, adding ...")
    #                         #     line.value_ids = [(4, value.id)]
    #                         #     changed = True
    #                         # else:
    #                             # _logger.info(" -> found")
    #     # if changed:
    #     #     self._create_variant_ids()                                          

    #     return res

