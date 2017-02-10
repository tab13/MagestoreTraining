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
    trainee_id = fields.Many2many('magestoretraining.trainee', string="Trainees")
    attachment_number = fields.Integer(compute='_get_attachment_number', string="Number of Attachments")
    # mission_document_ids = fields.One2many('magestoretraining.mission', 'task_document_id', "Documents")
    # document_ids = fields.One2many('ir.attachment', compute='_compute_document_ids', string="Applications")
    # documents_count = fields.Integer(compute='_compute_document_ids', string="Documents")

    @api.multi
    def _get_attachment_number(self):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'magestoretraining.task'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count']) for res in read_group_res)
        for record in self:
            record.attachment_number = attach_data.get(record.id, 0)

    # def _compute_document_ids(self):
    #     missions = self.mapped('mission_document_ids').filtered(lambda self: not self.emp_id)
    #     mission_to_task = dict((mission.id, mission.task_document_id.id) for mission in missions)
    #     attachments = self.env['ir.attachment'].search([
    #         '|',
    #         '&', ('res_model', '=', 'magestoretraining.task'), ('res_id', 'in', self.ids),
    #         '&', ('res_model', '=', 'magestoretraining.mission'), ('res_id', 'in', missions.ids)])
    #     result = dict.fromkeys(self.ids, self.env['ir.attachment'])
    #     for attachment in attachments:
    #         if attachment.res_model == 'magestoretraining.mission':
    #             result[mission_to_task[attachment.res_id]] |= attachment
    #         else:
    #             result[attachment.res_id] |= attachment
    #
    #     for task in self:
    #         task.document_ids = result[task.id]
    #         task.documents_count = len(task.document_ids)


    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        action['search_view_id'] = (
            self.env.ref('magestoretraining.attachment_view_search_magestore_training_task_document').id,)
        return action
    # @api.multi
    # def action_get_attachment_tree_view(self):
    #     action = self.env.ref('base.action_attachment').read()[0]
    #     action['context'] = {
    #         'default_res_model': self._name,
    #         'default_res_id': self.ids[0]
    #     }
    #     action['search_view_id'] = (
    #     self.env.ref('magestoretraining.ir_attachment_view_search_inherit_magestore_training_mission_document').id,)
    #     action['domain'] = ['|', '&', ('res_model', '=', 'magestoretraining.mission'), ('res_id', 'in', self.ids), '&',
    #                         ('res_model', '=', 'magestoretraining.training'),
    #                         ('res_id', 'in', self.mapped('course_ids').ids)]
    #     return action