# -*- coding: utf-8 -*-

from odoo import models, fields, api, registry


class TrainingCourse(models.Model):
    _name = 'magestoretraining.training'
    _inherit = ['mail.thread']

    name = fields.Char('Course Name', required=True)
    date_from = fields.Date(string='Starting Date')
    date_to = fields.Date(string='End Date')
    course_type = fields.Char(string="Course Type")
    description = fields.Text()
    manager = fields.Many2one('hr.employee', string="Manager")
    location = fields.Char(string="Location")
    status = fields.Selection([
        ('initial', "Initial"),
        ('inprogress', "In Progress"),
        ('done', "Done"),
    ])
    quantity = fields.Integer(string="The number of student")
    trainee_id = fields.Many2many('magestoretraining.trainee', string="Trainee")
    mentor_id = fields.Many2many('magestoretraining.mentor', string="Mentor")
    mission_id = fields.Many2many('magestoretraining.mission', string="Mission")
    attachment_number = fields.Integer(compute='_get_attachment_number', string="Number of Attachments")
    # check_test = fields.Boolean('wwwww', compute='_check_access_test')
    # check_access = fields.Boolean('asdasd', compute='_check_access')
    # check_access_mentor = fields.Boolean('asdasddd', compute='_check_access')

    @api.multi
    def _get_attachment_number(self):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'magestoretraining.training'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count']) for res in read_group_res)
        for record in self:
            record.attachment_number = attach_data.get(record.id, 0)

    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        action['search_view_id'] = (
        self.env.ref('magestoretraining.ir_attachment_view_search_inherit_magestore_training_document').id,)
        return action

    @api.multi
    def _check_access(self):
        self.env.cr.execute('select employee_id from magestoretraining_mentor mm,magestoretraining_mentor_magestoretraining_training_rel mmmt where mm.employee_id = %s and mmmt.magestoretraining_mentor_id = mm.id and mmmt.magestoretraining_training_id = %s', (self.env.uid,self.ids[0],))
        right_ment = self.env.cr.fetchone()
        # if right_ment:
        #     self.check_access = right_ment[0]
        # else:
        #     self.check_access = 'nulllll'
        self.env.cr.execute('select employee_id from magestoretraining_mentor mm where mm.employee_id = %s', (self.env.uid,))
        notright_ment = self.env.cr.fetchone()
        # if notright_ment:
        #     self.check_access_mentor = notright_ment[0]
        # else:
        #     self.check_access_mentor = 'nulllllll'
        # if right_ment:
        #     self.check_access = True
        #     self.check_access_mentor = True
        # if right_ment is None and notright_ment:
        #     self.check_access = True
        #     self.check_access_mentor = False
        # if self.env.uid == 1:
        #     self.check_access = False
        #     self.check_access_mentor = True

        # self.env.cr.execute(
        #     'select magestoretraining_mentor_id from magestoretraining_mentor_magestoretraining_training_rel where magestoretraining_training_id = %s',
        #     (self.ids[0],))
        # ment = self.env.cr.fetchone()
        # self.env.cr.execute(
        #     'select magestoretraining_mentor_id from magestoretraining_mentor_magestoretraining_training_rel where magestoretraining_training_id = %s',
        #     (self.ids,))
        # ment = self.env.cr.fetchone()
        # if curr:
        #     self.check_access = 'True'
        # elif ment or self.env.uid == 1:
        #     self.check_access = 'False'
        # else:

class missionmodel(models.Model):
    _name = 'magestoretraining.mission'

    name = fields.Char(string="Mission Name", required=True)
    description = fields.Text()
    # mentor_id = fields.Many2many('res.users', string="Mentor")
    task_id = fields.Many2many('magestoretraining.task', string="Task")
    # task_id = fields.One2many('magestoretraining.task','mission_id',string="Task")


class taskmodel(models.Model):
    _name = 'magestoretraining.task'

    name = fields.Char(string="Task Name", required=True)
    description = fields.Text()
    # mentor_id = fields.Many2many('res.users', string = "Mentor")
    # mission_id = fields.Many2one('magestoretraining.mission', string = "Mission")

# class documentmodel(models.Model):
#
#     _name = 'magestoretraining.document'
#
#     document_name = fields.Char('Document Name', required = True)
