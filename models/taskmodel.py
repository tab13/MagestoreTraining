# -*- coding: utf-8 -*-

from odoo import models, fields, api


class taskmodel(models.Model):
    _name = 'magestoretraining.task'

    deadline = fields.Date()
    name = fields.Char(string="Task Name", required=True)
    description = fields.Text()
    note = fields.Char(string="Note")
    time_start = fields.Date()
    stage = fields.Selection([
        ('To do', 'Todo'),
        ('Doing', 'Doing'),
        ('Done', 'Done'),
    ], string='status')
    mentor_id = fields.Many2many('magestoretraining.mentor', string="Mentor")
    mission_id = fields.Many2one('magestoretraining.mission', string="Mission")
    document_id = fields.Many2one('magestoretraining.document', string="Document")
    trainee_id = fields.Many2many('magestoretraining.trainee', string="Trainees")
