# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools, _
from odoo.modules.module import get_module_resource
from odoo.exceptions import ValidationError


# class Contract(models.Model):
#
#     _inherit = "hr.contract"
#
#     trainee_id = fields.Many2one('magestoretraining.trainee', string="Trainee")


class TrainingContract(models.Model):

    _name = 'magestoretraining.contract'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char('Contract Reference', required=True)
    trainer_id = fields.Many2one('res.company', string='Training Address')
    trainee_id = fields.Many2one('magestoretraining.trainee', string="Trainee")
    training_about = fields.Char('Training About')
    training_content = fields.Text(string="Training Content")
    training_form = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Off-line'),
    ], string='Form Of Training')
    date_start = fields.Date('Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date('End Date')
    working_hours = fields.Many2one('resource.calendar', string='Training Schedule')
    training_address = fields.Char(string='Training Address')
    trainer_right = fields.Text(string='Trainer Right')
    trainer_duty = fields.Text(string='Trainer Duty')
    trainee_right = fields.Text(string='Trainee Right')
    trainee_duty = fields.Text(string='Trainee Duty')
    training_fee = fields.Float('Fee', digits=(16, 2), required=True)
    payment_method = fields.Char('Payment Method')
    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('pending', 'To Renew'),
        ('close', 'Expired'),
    ], string='Status', track_visibility='onchange', help='Status of the contract', default='draft')

    # @api.onchange('employee_id')
    # def _onchange_employee_id(self):
    #     if self.employee_id:
    #         self.job_id = self.employee_id.job_id
    #         self.department_id = self.employee_id.department_id

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        if self.filtered(lambda c: c.date_end and c.date_start > c.date_end):
            raise ValidationError(_('Contract start date must be less than contract end date.'))

    # @api.multi
    # def set_as_pending(self):
    #     return self.write({'state': 'pending'})
    #
    # @api.multi
    # def set_as_close(self):
    #     return self.write({'state': 'close'})
    #
    # @api.multi
    # def _track_subtype(self, init_values):
    #     self.ensure_one()
    #     if 'state' in init_values and self.state == 'pending':
    #         return 'magestoretraining_contract.mt_contract_pending'
    #     elif 'state' in init_values and self.state == 'close':
    #         return 'magestoretraining_contract.mt_contract_close'
    #     return super(TrainingContract, self)._track_subtype(init_values)


class traineemodel(models.Model):

    _name = 'magestoretraining.trainee'
    _inherit = ['mail.thread']

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    image = fields.Binary("Photo", default=_default_image, attachment=True,help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True, help="Medium-sized photo of the employee. It is automatically " "resized as a 128x128px image, with aspect ratio preserved. " "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized photo", attachment=True,help="Small-sized photo of the employee. It is automatically " "resized as a 64x64px image, with aspect ratio preserved. " "Use this field anywhere a small image is required.")
    name = fields.Char(string="Name", required=True)
    # user_id = fields.Many2one('res.users', string='User', help='Related user name for the resource to manage its access.')
    employee_id = fields.Many2one('hr.employee', string='Related Employee')
    email = fields.Char(string="Email")
    mobile_phone = fields.Char(string="Mobile Phone")
    work_phone = fields.Char('Work phone')
    applicant_name = fields.Char(string="Applicant's Name")
    birth_day = fields.Date(string="Birth Day")
    address = fields.Char(string="Address")
    identity = fields.Char(string="Identity Number")
    level = fields.Char(string="Level")
    status = fields.Char(string="Status")
    contract_ids = fields.One2many('magestoretraining.contract', 'trainee_id', string='Contracts')
    contract_id = fields.Many2one('magestoretraining.contract', compute='_compute_contract_id', string='Current Contract', help='Latest contract of the employee')
    contracts_count = fields.Integer(compute='_compute_contracts_count', string='Contracts')

    def _compute_contract_id(self):
        """ get the lastest contract """
        Contract = self.env['magestoretraining.contract']
        for trainee in self:
            trainee.contract_id = Contract.search([('trainee_id', '=', trainee.id)], order='date_start desc',limit=1)

    def _compute_contracts_count(self):
        # read_group as sudo, since contract count is displayed on form view
        contract_data = self.env['magestoretraining.contract'].sudo().read_group([('trainee_id', 'in', self.ids)], ['trainee_id'],
                                                                  ['trainee_id'])
        result = dict((data['trainee_id'][0], data['trainee_id_count']) for data in contract_data)
        for trainee in self:
            trainee.contracts_count = result.get(trainee.id, 0)

    @api.onchange('employee_id')
    def _onchange_trainee(self):
        self.name = self.employee_id.name
        self.email = self.employee_id.work_email
        self.mobile_phone = self.employee_id.mobile_phone
        self.work_phone = self.employee_id.work_phone
        self.birth_day = self.employee_id.birthday
        self.image = self.employee_id.image

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(traineemodel, self).write(vals)

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(traineemodel, self).create(vals)