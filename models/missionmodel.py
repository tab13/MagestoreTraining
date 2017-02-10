# -*- coding: utf-8 -*-

from odoo import models, fields, api


class missionmodel(models.Model):
    _name = 'magestoretraining.mission'

    name = fields.Char(string="Mission Name", required=True)
    description = fields.Text()
    time_start = fields.Date()
    execution_time = fields.Float(string="Excution Time", required=True)
    trainee_id = fields.Many2many('magestoretraining.trainee', string="Trainee")
    mentor_id = fields.Many2many('magestoretraining.mentor', string="Mentor")
    task_id = fields.Many2many('magestoretraining.task', string="Task")
    document_id = fields.Many2many('magestoretraining.document', string="Document")
    stage = fields.Selection([
        ('To do', 'Todo'),
        ('Doing', 'Doing'),
        ('Done', 'Done'),
    ], string='status')
