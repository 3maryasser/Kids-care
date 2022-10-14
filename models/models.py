from odoo import models,fields,api
import logging
from datetime import date
import json
import requests

import math
from odoo.exceptions import UserError
from odoo.http import request


_logger = logging.getLogger(__name__)

class Registers(models.Model):
    _inherit = "sale.order"
    child_name = fields.Char()
    age_of_entering = fields.Date()
    is_has_relative = fields.Boolean()
    occup = fields.Char()
    re_add = fields.Char()
    re_num = fields.Char()

    relation_between = fields.Selection(selection=[("sta","Stable"),("sep","Separation"),("imm","Immigration"),("fa","Father dead"),("mo","mother dead")])
    fa_num = fields.Char()
    fa_occup = fields.Char()
    mo_num = fields.Char()
    mo_occup = fields.Char()
    family_members = fields.Integer()
    male = fields.Integer()
    female = fields.Integer()
    arr_child = fields.Char()
    sens_med = fields.Boolean()
    wh_med = fields.Char()
    sens_food = fields.Boolean()
    wh_food = fields.Char()
    food_likes = fields.Char()
    food_dislikes = fields.Char()
    disease = fields.Char()
    behavior = fields.Char()
    scare = fields.Char()
    ex_grmo = fields.Boolean()
    ex_grfa = fields.Boolean()

    @api.depends('partner_id.stage')
    def action_confirm(self):
        sms_url = "http://smss.nilogy.com/app/gateway/gateway.php?sendmessage=1&username=kidscare&password=kids3care54&text="
        for order in  self:
            if order.order_line[0].name == 'Buds':
                if order.partner_id.age >= 2:
                    send_sms_url = sms_url + "السيد ولي أمر الطفل / الطفلة :\n " + order.partner_id.name +" \nروضة كيدس كير الخاصة ترحب بكم في عاملها الدراسي الجديد ونتمنى لطفلكم عاما دراسياً وترفيهيا موفقاً"+ "&numbers=" + order.partner_id.phone + "&sender=KIDS CARE"
                    result = requests.get(send_sms_url)
                    order.partner_id.write({'stage': 'buds'})
                    order.state = 'sale'
                else:
                    raise UserError("this child is too small to enter kindergaten")
            elif order.order_line[0].name == 'First Level':
                if order.partner_id.age >= 4:
                    send_sms_url = sms_url + "السيد ولي أمر الطفل / الطفلة :\n " + order.partner_id.name + " \nروضة كيدس كير الخاصة ترحب بكم في عاملها الدراسي الجديد ونتمنى لطفلكم عاما دراسياً وترفيهيا موفقاً" + "&numbers=" + order.partner_id.phone + "&sender=KIDS CARE"
                    result = requests.get(send_sms_url)
                    order.partner_id.write({'stage': 'first'})
                    order.state = 'sale'
                else:
                    raise UserError("this child can,t go to next level")
            elif order.order_line[0].name == 'Second Level':
                if order.partner_id.age >= 5:
                    send_sms_url = sms_url + "السيد ولي أمر الطفل/الطفلة :" + order.partner_id.name + " \nروضة كيدس كير الخاصة ترحب بكم في عامها الدراسي الجديد ونتمنى لطفلكم عاما دراسياً وترفيهيا موفقاً" + "&numbers=" + order.partner_id.phone + "&sender=KIDS CARE"
                    result = requests.get(send_sms_url)
                    order.partner_id.write({'stage': 'second'})
                    order.state = 'sale'
                else:
                    raise UserError("this child can,t go to next level")
            else:
                raise UserError('something wrong')



            # elif  order.order_line[0] == 'First Level':
            #     order.partner_id.stage == 'first'
            # elif order.order_line[0] == 'Second Level':
            #     order.partner_id.stage == 'second'

    # @api.depends('sale.order.state')
    # def action_confirm(self):
    #     sms_url = "http://smss.nilogy.com/app/gateway/gateway.php?sendmessage=1&username=kidscare&password=kids3care54&text="
    #     for order in self:
    #         if sms_url:
    #             send_sms_url = sms_url+"Hello"+order.partner_id.name+"&numbers="+order.partner_id.phone+"&sender=KIDS CARE"
    #             result = requests.get(send_sms_url)
    #             _logger.error("SMS result = " + str(result.content))
    #             if result:
    #                 return True
    #             else:
    #                 return False
    #         else:
    #             return False
    #             raise UserError("Sms error")
            # raise UserError("hello "+str(order.partner_id.name))

    # @api.depends('partner_id.state')
    # def action_confirm(self):
    #     for order in self:
    #         # order.partner_id.stage = 'Buds'
    #         order.partner_id.write({'stage': Buds})
        # requests.get("http://smss.nilogy.com/app/gateway/gateway.php?sendmessage=1&username=kidscare&password=kids3care54&text=hi&numbers=249966292475&sender=KIDS CARE")








class Students(models.Model):
    _inherit = "res.partner"
    house_num = fields.Char()
    age = fields.Integer(compute="age_count",store=True)
    birth_date = fields.Date(string="Date of Birth")
    gender = fields.Selection(selection=[("male","Male"),("female","Female")],required=True)
    is_child = fields.Boolean(default=True)
    stage = fields.Selection(selection=[("a","Kids"),("buds","Buds"),("first","First Level"),("second","Second Level")],default="a")
    # stage = fields.Many2one('product.template')
    files = fields.Binary(string="upload File", attachment=True)
    @api.depends("birth_date")
    def age_count(self):
        for rec in self:
            today = date.today()
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year
            else:
                rec.age = 0

    # @api.depends("stage")
    # def action_buds(self):
    #     if self.age >= 2:
    #         self.stage = 'buds'
    #     else:
    #         raise UserError("this child is too small to enter kindergaten")

    # @api.depends("stage")
    # def action_level_one(self):
    #     if self.age >= 4:
    #         self.stage = 'first'
    #     else:
    #         raise UserError("this child can,t go to next level")

    # @api.depends("stage")
    # def action_level_two(self):
    #     if self.age >= 5:
    #         self.stage = 'second'
    #     else:
    #         raise UserError("this child can,t go to next level")

    # @api.depends("stage")
    # def action_reset(self):
    #     self.stage = 'a'



# class Classes(models.Model):
#     _name = "kids.class"
#     name = fields.Char()
    # st_seasons = fields.Many2one("res.partner")

class Costs(models.Model):
    _inherit = "product.template"
    info = fields.Html()
class OtherCosts(models.Model):
    _inherit = "product.template"
    isclass = fields.Boolean()

class Invoices(models.Model):
    _inherit = "account.move"

class Bills(models.Model):
    _inherit = "account.move"
    # vendor = fields.Many2one("res.partner")