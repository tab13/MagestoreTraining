# -*- coding: utf-8 -*-

from odoo import models, fields, api


class missionmodel(models.Model):
    _name = 'magestoretraining.mission'

    name = fields.Char(string="Mission Name", required=True)
    description = fields.Text()
    time_start = fields.Date()
    execution_time = fields.Float(string="Excution Time", required=True)
    mentor_id = fields.Many2many('magestoretraining.mentor', string="Mentor")
    task_id = fields.Many2many('magestoretraining.task', string="Task")
    stage = fields.Selection([
        ('To do', 'Todo'),
        ('Doing', 'Doing'),
        ('Done', 'Done'),
    ], string='status')
    attachment_number = fields.Integer(compute='_get_attachment_number', string="Number of Attachments")
    # course_ids = fields.One2many('magestoretraining.training', 'mission_document_id', "Documents")
    # document_ids = fields.One2many('ir.attachment', compute='_compute_document_ids', string="Applications")
    # documents_count = fields.Integer(compute='_compute_document_ids', string="Documents")
    # task_document_id = fields.Many2one('magestoretraining.task', string="Document")

    @api.multi
    def _get_attachment_number(self):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'magestoretraining.mission'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count']) for res in read_group_res)
        for record in self:
            record.attachment_number = attach_data.get(record.id, 0)

    # def _compute_document_ids(self):
    #     courses = self.mapped('course_ids').filtered(lambda self: not self.emp_id)
    #     coures_to_mission = dict((course.id, course.mission_document_id.id) for course in courses)
    #     attachments = self.env['ir.attachment'].search([
    #         '|',
    #         '&', ('res_model', '=', 'magestoretraining.mission'), ('res_id', 'in', self.ids),
    #         '&', ('res_model', '=', 'magestoretraining.training'), ('res_id', 'in', courses.ids)])
    #     result = dict.fromkeys(self.ids, self.env['ir.attachment'])
    #     for attachment in attachments:
    #         if attachment.res_model == 'magestoretraining.training':
    #             result[coures_to_mission[attachment.res_id]] |= attachment
    #         else:
    #             result[attachment.res_id] |= attachment
    #
    #     for mission in self:
    #         mission.document_ids = result[mission.id]
    #         mission.documents_count = len(mission.document_ids)

    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        action['search_view_id'] = (
            self.env.ref('magestoretraining.attachment_view_search_magestore_training_mission_document').id,)
        action['view'] = {
            'type': 'ir.actions.act_window_close'
        }
        return action

    # @api.multi
    # def action_get_attachment_tree_view(self):
    #     action = self.env.ref('base.action_attachment').read()[0]
    #     action['context'] = {
    #         'default_res_model': self._name,
    #         'default_res_id': self.ids[0]
    #     }
    #     action['search_view_id'] = (self.env.ref('magestoretraining.ir_attachment_view_search_inherit_magestore_training_mission_document').id,)
    #     action['domain'] = ['|', '&', ('res_model', '=', 'magestoretraining.mission'), ('res_id', 'in', self.ids), '&',
    #                         ('res_model', '=', 'magestoretraining.training'), ('res_id', 'in', self.mapped('course_ids').ids)]
    #     return action