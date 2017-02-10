# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo import SUPERUSER_ID


class User(models.Model):

    _inherit = ['res.users']

    trainee_ids = fields.One2many('magestoretraining.trainee', 'user_id', string='Related employees')

    @api.multi
    def write(self, vals):
        """ When renaming admin user, we want its new name propagated to its related employees """
        result = super(User, self).write(vals)
        Trainee = self.env['magestoretraining.trainee']
        if vals.get('name'):
            for user in self.filtered(lambda user: user.id == SUPERUSER_ID):
                trainees = Trainee.search([('user_id', '=', user.id)])
                trainees.write({'name': vals['name']})
        return result

    @api.multi
    def _get_related_trainees(self):
        self.ensure_one()
        ctx = dict(self.env.context)
        if 'thread_model' in ctx:
            ctx['thread_model'] = 'magestoretraining.trainee'
        return self.env['magestoretraining.trainee'].with_context(ctx).search([('user_id', '=', self.id)])

    # @api.multi
    # def message_post(self, **kwargs):
    #     """ Redirect the posting of message on res.users to the related employees.
    #         This is done because when giving the context of Chatter on the
    #         various mailboxes, we do not have access to the current partner_id.
    #     """
    #     self.ensure_one()
    #     if kwargs.get('message_type') == 'email':
    #         return super(User, self).message_post(**kwargs)
    #     message_id = None
    #     trainees = self._get_related_trainees()
    #     if not trainees:  # no employee: fall back on previous behavior
    #         return super(User, self).message_post(**kwargs)
    #     for trainee in trainees:
    #         message_id = trainee.message_post(**kwargs)
    #     return message_id
