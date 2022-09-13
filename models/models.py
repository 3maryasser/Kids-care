from odoo import models,fields,api
import logging
from datetime import date
import math
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class Registers(models.Model):
    _inherit = "sale.order"
    child_name = fields.Char()
    age_of_entering = fields.Date()
    is_has_relative = fields.Boolean()
    occup = fields.Char()
    re_add = fields.Char()
    re_num = fields.Integer(default="+249")

    relation_between = fields.Selection(selection=[("sta","Stable"),("sep","Separation"),("imm","Immigration"),("fa","Father dead"),("mo","mother dead")])
    fa_num = fields.Integer(default="+249")
    mo_num = fields.Integer(default="+249")
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

    




class Students(models.Model):
    _inherit = "res.partner"
    house_num = fields.Char()
    age = fields.Integer(compute="age_count",store=True)
    birth_date = fields.Date(string="Date of Birth")
    gender = fields.Selection(selection=[("male","Male"),("female","Female")])
    is_child = fields.Boolean(default=True)
    stage = fields.Selection(selection=[("a","Kids"),("buds","Buds"),("first","First Level"),("second","Second Level")],default="a")

    @api.depends("birth_date")
    def age_count(self):
        for rec in self:
            today = date.today()
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year
            else:
                rec.age = 0
    
    @api.depends("stage")
    def action_buds(self):
        if self.age >= 2:
            self.stage = 'buds'
        else:
            raise UserError("this child is too small to enter kindergaten")

    @api.depends("stage")
    def action_level_one(self):
        if self.age >= 4:
            self.stage = 'first'
        else:
            raise UserError("this child can,t go to next level")

    @api.depends("stage")
    def action_level_two(self):
        if self.age >= 5:
            self.stage = 'second'
        else:
            raise UserError("this child can,t go to next level")

    @api.depends("stage")
    def action_reset(self):
        self.stage = 'a'

        

class Classes(models.Model):
    _name = "kids.class"
    name = fields.Char()
    # st_seasons = fields.Many2one("res.partner")

class Costs(models.Model):
    _inherit = "product.template"
    info = fields.Html()
    

class Invoices(models.Model):
    _inherit = "account.move"
    
class Bills(models.Model):
    _inherit = "account.move"
    # vendor = fields.Many2one("res.partner")