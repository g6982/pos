# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models
import logging
from odoo.exceptions import Warning
_logger = logging.getLogger(__name__)



class quickbookTimesheetManualSynchronization(models.TransientModel):
    _name = 'update.question.answer'


    line = fields.One2many(comodel_name='res.security.answer',inverse_name='user_id')

    def update_question_answer(self):
        _logger.info("===========update_question_answer:%r",self.line)
        _logger.info("+++++++++++++++uid+++++++++++:%r",self.env.user)
        usr = self.env.user
        Line = [(5,0,0)]
        for rec in self.line:
            vals = {
                'question_id' : int(rec.question_id.id),
                'answer' : rec.answer,
                'user_id' : usr.id
            }
            Line.append((0, 0, vals))
        usr.line = Line

