# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools, _
from odoo.modules.module import get_module_resource
from odoo.exceptions import ValidationError


class Mentor(models.Model):
    _name = "magestoretraining.mentor"
    _order = 'name_related'
    _inherits = {'resource.resource': "resource_id"}
    _inherit = ['mail.thread']

    _mail_post_access = 'read'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    # we need a related field in order to be able to sort the employee by name
    name_related = fields.Char(related='resource_id.name', string="Resource Name", readonly=True, store=True)
    # name = fields.Char(string='Mentor Name')
    department_id = fields.Many2one('hr.department', string='Department')
    employee_id = fields.Many2one('hr.employee', string='Related Employee')
    address_id = fields.Many2one('res.partner', string='Working Address')
    work_phone = fields.Char('Work Phone')
    mobile_phone = fields.Char('Work Mobile')
    work_email = fields.Char('Work Email')
    work_location = fields.Char('Work Location')
    notes = fields.Text('Notes')
    resource_id = fields.Many2one('resource.resource', string='Resource',
                                  ondelete='cascade', required=True, auto_join=True)
    job_id = fields.Many2one('hr.job', string='Job Title')

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Photo", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True,
                                 help="Medium-sized photo of the employee. It is automatically "
                                      "resized as a 128x128px image, with aspect ratio preserved. "
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized photo", attachment=True,
                                help="Small-sized photo of the employee. It is automatically "
                                     "resized as a 64x64px image, with aspect ratio preserved. "
                                     "Use this field anywhere a small image is required.")

    # @api.onchange('address_id')
    # def _onchange_address(self):
    #     self.work_phone = self.address_id.phone
    #     self.mobile_phone = self.address_id.mobile

    @api.onchange('company_id')
    def _onchange_company(self):
        address = self.company_id.partner_id.address_get(['default'])
        self.address_id = address['default'] if address else False

    @api.onchange('department_id')
    def _onchange_department(self):
        self.parent_id = self.department_id.manager_id

    @api.onchange('employee_id')
    def _onchange_user(self):
        # self.work_email = self.user_id.email
        # self.name = self.user_id.name
        # self.image = self.user_id.image
        # self.work_phone = self.user_id.phone
        # self.mobile_phone = self.user_id.mobile
        # self.work_location = self.parent_id.work_location
        self.work_email = self.employee_id.work_email
        self.name = self.employee_id.name
        self.image = self.employee_id.image
        self.work_phone = self.employee_id.work_phone
        self.mobile_phone = self.employee_id.mobile_phone
        self.work_location = self.employee_id.work_location

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(Mentor, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(Mentor, self).write(vals)

    @api.multi
    def unlink(self):
        resources = self.mapped('resource_id')
        super(Mentor, self).unlink()
        return resources.unlink()

    @api.multi
    def action_follow(self):
        """ Wrapper because message_subscribe_users take a user_ids=None
            that receive the context without the wrapper.
        """
        return self.message_subscribe_users()

    @api.multi
    def action_unfollow(self):
        """ Wrapper because message_unsubscribe_users take a user_ids=None
            that receive the context without the wrapper.
        """
        return self.message_unsubscribe_users()

    @api.model
    def _message_get_auto_subscribe_fields(self, updated_fields, auto_follow_fields=None):
        """ Overwrite of the original method to always follow user_id field,
            even when not track_visibility so that a user will follow it's employee
        """
        if auto_follow_fields is None:
            auto_follow_fields = ['user_id']
        user_field_lst = []
        for name, field in self._fields.items():
            if name in auto_follow_fields and name in updated_fields and field.comodel_name == 'res.users':
                user_field_lst.append(name)
        return user_field_lst

    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids):
        # Do not notify user it has been marked as follower of its employee.
        return
