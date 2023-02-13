from odoo import models,fields,api,exceptions
    
class BuyerFlat(models.Model):

    _name='offer.flat'
    flat = fields.Many2one('realtor.flat' , string = "Flat",required=True)
    buyer = fields.Many2one('res.partner', string = "Offreur",required=True)
    offer=fields.Float(string = "Prix Offre",required=True)

    _sql_constraints = [
                        ('all_unique','UNIQUE(flat,buyer,offer)',"The course title must be unique"),
                       ]

    @api.constrains('offer')
    def check_offer(self):
        for offre in self:
            if offre.offer<0.9*offre.flat.price:
                raise exceptions.ValidationError("the offer must be greater than or equal 90%")