from odoo import models,fields,api

class ProductTemplate(models.Model):
    
    _inherit = ['product.template']

    
    flat = fields.Many2one('realtor.flat' ,compute='compute_flat', inverse='flat_inverse',string="Flat")
    flats = fields.One2many('realtor.flat', 'product_id')


    @api.depends('flats')
    def compute_flat(self):
        if len(self.flats) > 0:
            self.flat = self.flats[0]


    def flat_inverse(self):
        if len(self.flats) > 0:
            # delete previous reference
            flat = self.env['realtor.flat'].browse(self.flats[0].id)
            flat.product_id = False
            # set new reference
        self.flat.product_id = self
        self.list_price=self.flat.price
        self.description=self.flat.description
        self.name=self.flat.name
        self.image_1920=self.flat.image

   
   