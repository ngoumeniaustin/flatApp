from odoo import models,fields,api

class Product(models.Model):
    
    _inherit = ['product.product']
   

    type =fields.Selection(

        [('product','1'),

         ('test2','2')],

        string='Type',default='product')
   