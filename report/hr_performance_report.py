# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models, tools
from ..models import hr_performance


class hr_performance_report(models.Model):
    _name = "hr.performance.report"
    _description = "Performance Statistics"
    _auto = False
    # _rec_name = 'date_create'
    # _order = 'date_create desc'

    teller_num = fields.Char(u'柜员号', readonly=True)
    teller_name = fields.Char(u'柜员名', readonly=True)
    role= fields.Char(u'角色', readonly=True)
    # ywzhs=fields.Float(u'业务总耗时(分钟)', readonly=True)
    # ywzl=fields.Integer(u'业务总量', readonly=True)
    # lrhzs= fields.Integer(u'录入汉字数', readonly=True)
    # lrzjs= fields.Integer(u'录入字节数', readonly=True)
    # lrccs= fields.Integer(u'录入差错数', readonly=True)
    # tjyxmh= fields.Integer(u'提交影像模糊', readonly=True)
    # lrcwl=fields.Float(u'录入错误率', readonly=True)
    # lrzql=fields.Float(u'录入正确率', readonly=True)
    # lrdhl=fields.Float(u'录入打回率', readonly=True)
    # shdhs=fields.Integer(u'审核打回数', readonly=True)
    # ythqtdhs=fields.Integer(u'用途和其他审核打回数', readonly=True)
    # rqshdhs=fields.Integer(u'日期审核打回数', readonly=True)
    # jeshdhs=fields.Integer(u'金额审核打回数', readonly=True)
    # skrshdhs=fields.Integer(u'收款人审核打回数', readonly=True)
    # fkrshdhs=fields.Integer(u'付款人审核打回数', readonly=True)
    # bsshdhs=fields.Integer(u'背书审核打回数', readonly=True)
    # shdhl=fields.Float(u'审核打回率', readonly=True)
    # sqdhs=fields.Integer(u'授权打回数', readonly=True)
    # sqdhl=fields.Float(u'授权打回率', readonly=True)
    # pjclsd=fields.Float(u'平均处理速度', readonly=True)
    # pzhs=fields.Float(u'批注耗时', readonly=True)
    
    ywzl_sum = fields.Float(u"求和项:录入业务总量", digits=0)
    lrccs_sum = fields.Float(u"求和项:录入差错数", digits=0)
    tjyxmh_sum = fields.Float(u"求和项:提交影像模糊",  digits=0)
    sywzl_sum = fields.Float(u"求和项:录入业务总量(双中心报表)", digits=0)
    slrccs_sum = fields.Float(u"求和项:录入差错数(双中心报表)", digits=0)
    stjyxmh_sum = fields.Float(u"求和项:提交影像模糊(双中心报表)",  digits=0)   
    #lrzjs_sum=fields.Float(u"求和项:计奖总字节",  digits=0)   
    lrzjs_sum_avg = fields.Float("平均值项:计奖总字节", group_operator="avg", digits=0)
    lrccs_per = fields.Float(u"差错率",  digits=2) 
    lrzql_per = fields.Float(u"正确率",  digits=2) 
    lrdhl_per = fields.Float(u"打回率",  digits=2) 
    
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_performance_report')
        cr.execute("""
            create or replace view hr_performance_report as (
                     select
                     min(s.id) as id,
                     s.role,
                     sum(s.ywzl) as ywzl_sum,
                     sum(s.lrccs) as lrccs_sum,
                     sum(s.tjyxmh) as tjyxmh_sum,
                     sum(a.ywzl) as sywzl_sum,
                     sum(a.lrccs) as slrccs_sum,
                     sum(a.tjyxmh) as stjyxmh_sum,
                     (sum(s.lrzjs)/count(*)) as lrzjs_sum_avg,
                     lrccs_sum/ywzl_sum as lrccs_per,
                     1-lrccs_per as lrzql_per,
                     tjyxmh_sum/ywzl_sum as lrdhl_per
                 from hr_performancereportori s full join hr_performancebranchreportori a on s.role= a.role
                 group by
                     s.role
                
            )
        """)
    

class hr_performance_report_by_group(models.Model):
    _name = "hr.performance.report"
    _description = "Performance Statistics"
    _auto = False
    # _rec_name = 'date_create'
    # _order = 'date_create desc'

    teller_num = fields.Char(u'柜员号', readonly=True)
    teller_name = fields.Char(u'柜员名', readonly=True)
    role= fields.Char(u'角色', readonly=True)

    
    ywzl_sum = fields.Float(u"求和项:录入业务总量", digits=0)
    lrccs_sum = fields.Float(u"求和项:录入差错数", digits=0)
    tjyxmh_sum = fields.Float(u"求和项:提交影像模糊",  digits=0)
    sywzl_sum = fields.Float(u"求和项:录入业务总量(双中心报表)", digits=0)
    slrccs_sum = fields.Float(u"求和项:录入差错数(双中心报表)", digits=0)
    stjyxmh_sum = fields.Float(u"求和项:提交影像模糊(双中心报表)",  digits=0)   
    #lrzjs_sum=fields.Float(u"求和项:计奖总字节",  digits=0)   
    lrzjs_sum_avg = fields.Float("平均值项:计奖总字节", group_operator="avg", digits=0)
    
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_performance_report')
        cr.execute("""
            create or replace view hr_performance_report as (
                     select
                     min(s.id) as id,
                     s.role,
                     sum(s.ywzl) as ywzl_sum,
                     sum(s.lrccs) as lrccs_sum,
                     sum(s.tjyxmh) as tjyxmh_sum,
                     sum(a.ywzl) as sywzl_sum,
                     sum(a.lrccs) as slrccs_sum,
                     sum(a.tjyxmh) as stjyxmh_sum,
                     (sum(s.lrzjs)/count(*)) as lrzjs_sum_avg
                 from hr_performancereportori s full join hr_performancebranchreportori a on s.role= a.role
                 group by
                     s.role
                
            )
        """)    
     # select
                     # min(s.id) as id,
                     # s.teller_num,
                     # s.teller_name,
                     # s.role,
                     # sum(s.ywzl) as ywzl_sum,
                     # sum(s.lrccs) as lrccs_sum,
                     # sum(s.tjyxmh) as tjyxmh_sum
                 # from hr_performancereportori s
                 # group by
                     # s.teller_num,
                     # s.teller_name,
                     # s.role
    
    
    # user_id = fields.Many2one('res.users', 'User', readonly=True)
    # company_id = fields.Many2one('res.company', 'Company', readonly=True)
    # date_create = fields.Datetime('Create Date', readonly=True)
    # date_last_stage_update = fields.Datetime('Last Stage Update', readonly=True)
    # date_closed = fields.Date('Closed', readonly=True)
    # job_id = fields.Many2one('hr.job', 'Applied Job', readonly=True)
    # stage_id = fields.Many2one('hr.recruitment.stage', 'Stage')
    # type_id = fields.Many2one('hr.recruitment.degree', 'Degree')
    # department_id = fields.Many2one('hr.department', 'Department', readonly=True)
    # priority = fields.Selection(hr_recruitment.AVAILABLE_PRIORITIES, 'Appreciation')
    # salary_prop = fields.Float("Salary Proposed", digits=0)
    # salary_prop_avg = fields.Float("Avg. Proposed Salary", group_operator="avg", digits=0)
    # salary_exp = fields.Float("Salary Expected", digits=0)
    # salary_exp_avg = fields.Float("Avg. Expected Salary", group_operator="avg", digits=0)
    # partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    # delay_close = fields.Float('Avg. Delay to Close', digits=(16, 2), readonly=True, group_operator="avg", help="Number of Days to close the project issue")
    # last_stage_id = fields.Many2one('hr.recruitment.stage', 'Last Stage')
    # medium_id = fields.Many2one('utm.medium', 'Medium', readonly=True, help="This is the method of delivery. Ex: Postcard, Email, or Banner Ad")
    # source_id = fields.Many2one('utm.source', 'Source', readonly=True, help="This is the source of the link Ex: Search Engine, another domain, or name of email list")

    # def init(self, cr):
        # tools.drop_view_if_exists(cr, 'hr_recruitment_report')
        # cr.execute("""
            # create or replace view hr_recruitment_report as (
                 # select
                     # min(s.id) as id,
                     # s.create_date as date_create,
                     # date(s.date_closed) as date_closed,
                     # s.date_last_stage_update as date_last_stage_update,
                     # s.partner_id,
                     # s.company_id,
                     # s.user_id,
                     # s.job_id,
                     # s.type_id,
                     # s.department_id,
                     # s.priority,
                     # s.stage_id,
                     # s.last_stage_id,
                     # s.medium_id,
                     # s.source_id,
                     # sum(salary_proposed) as salary_prop,
                     # (sum(salary_proposed)/count(*)) as salary_prop_avg,
                     # sum(salary_expected) as salary_exp,
                     # (sum(salary_expected)/count(*)) as salary_exp_avg,
                     # extract('epoch' from (s.write_date-s.create_date))/(3600*24) as delay_close,
                     # count(*) as nbr
                 # from hr_applicant s
                 # group by
                     # s.date_open,
                     # s.create_date,
                     # s.write_date,
                     # s.date_closed,
                     # s.date_last_stage_update,
                     # s.partner_id,
                     # s.company_id,
                     # s.user_id,
                     # s.stage_id,
                     # s.last_stage_id,
                     # s.type_id,
                     # s.priority,
                     # s.job_id,
                     # s.department_id,
                     # s.medium_id,
                     # s.source_id
            # )
        # """)
