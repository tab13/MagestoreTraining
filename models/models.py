# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class training_module(models.Model):
#     _name = 'training_module.training_module'

#     name = fields.Char()
#     value = fields.Integer()do
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
