from odoo import models, fields, api
from odoo import tools, _
from odoo.modules.module import get_module_resource
from odoo.exceptions import ValidationError


class TrainingReview(models.Model):
    _name = 'magestoretraining.review'
    _inherit = ['mail.thread']

    name = fields.Char('Contract Reference', required=True)


class TrainingReviewForm(models.Model):
    _name = 'magestoretraining.reviewform'
    _inherit = ['mail.thread', 'ir.needaction_mixin']


class TrainingReviewResult(models.Model):
    _name = 'magestoretraining.reviewresult'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    trainee_id = fields.Many2one('magestoretraining.trainee', string="Trainee")
