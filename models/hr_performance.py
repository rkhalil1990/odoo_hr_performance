# -*- coding: utf-8 -*-

from openerp import api, fields, models, fields
from openerp import _, tools
from openerp.exceptions import UserError, AccessError
from datetime import date, datetime, timedelta
import calendar
import logging


class HrPerformance(models.Model):
    _name = 'hr.performance'
    _description = 'Hr Performance'
    _order = 'id'


class HrPerformanceBonus(models.Model):  # 奖金计算new
    _name = 'hr.performancebonus'
    _description = 'Hr Performance Bonus'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    identity = fields.Char(u'身份')
    quarters = fields.Char(u'岗位')
    quarters_date = fields.Date(u'当前岗位上岗日期')
    group = fields.Char(u'组别')
    role = fields.Char(u'角色')
    role1 = fields.Char(u'角色1')
    ywlx = fields.Char(u'业务类型')
    ywzhs = fields.Float(u'业务总耗时')
    ywzl = fields.Float(u'业务总量')
    hzs = fields.Float(u'汉字数')
    zjs = fields.Float(u'字节数')
    ccs = fields.Float(u'差错数')
    tjyxmh = fields.Float(u'提交影像模糊')
    cwl = fields.Float(u'错误率', digits=(5, 5))
    zql = fields.Float(u'正确率', digits=(7, 7))
    dhl = fields.Float(u'打回率', digits=(5, 5))
    # jbzjs = fields.Float(u'基本字节数')
    gwxs = fields.Float(u'岗位系数')
    zshzjs = fields.Float(u'折算后字节数')
    jjdj = fields.Float(u'计奖单价', digits=(5, 5))
    sskcs = fields.Float(u'速算扣除数')
    khxs = fields.Float(u'考核系数')
    kj = fields.Float(u'扣奖')
    jj = fields.Float(u'奖金')
    ranking = fields.Integer(u'排名')
    ratio = fields.Float(u'整体系数')
    manager_ratio = fields.Float(u'作业经理系数')
    complete_rate = fields.Float(u'完成率')
    complete_changed_rate = fields.Float(u'调整后成率')
    source_from = fields.Char(u'数据来源', readonly=True)
    performancebonustotal_id = fields.Many2one(
        'hr.performancebonustotal', 'Hr Performance Bonus Total', ondelete='cascade')

    # def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False, lazy=True):
    #     res = super(HrPerformanceBonus, self).read_group(cr, uid, domain, fields, groupby, offset, limit=limit, context=context, orderby=orderby, lazy=lazy)
    #     _logger = logging.getLogger(__name__)
    #     gwxs_role_list = (u'录入', u'行号选择', u'行号录入')
    #     lurushenhe_role1_list = (u'A', u'B', u'E', u'F')
    #     source_list = (u'绩效报表', u'双中心绩效报表', u'信用卡报表',u'双中心信用卡报表')
    #     performancelurushenheparameter_datas_ids = self.pool['hr.performancelurushenheparameter'].search(cr, uid, [], context=context)
    #     performancelurushenheparameter_datas = self.pool.get('hr.performancelurushenheparameter').browse(cr, uid, performancelurushenheparameter_datas_ids, context=context)

    #     performancegoal_datas_ids = self.pool['hr.performancegoal'].search(cr, uid, [], context=context)
    #     performancegoal_datas = self.pool.get('hr.performancegoal').browse(cr, uid, performancegoal_datas_ids, context=context)
    #     if 'ywzhs' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['ywzhs'] = 0.0
    #     if 'ywzl' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['ywzl'] = 0.0
    #     if 'hzs' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['hzs'] = 0.0
    #     if 'zjs' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['zjs'] = 0.0
    #     if 'ccs' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['ccs'] = 0.0
    #     if 'tjyxmh' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['tjyxmh'] = 0.0
    #     if 'cwl' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 lines = self.search(cr, uid, line['__domain'], context=context)
    #                 pending_value = 0.0
    #                 for current_account in self.browse(cr, uid, lines, context=context):
    #                     if current_account.cwl != 0.0:
    #                         pending_value = current_account.cwl
    #                         break
    #                 line['cwl'] = pending_value
    #     if 'zql' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 lines = self.search(cr, uid, line['__domain'], context=context)
    #                 pending_value = 0.0
    #                 for current_account in self.browse(cr, uid, lines, context=context):
    #                     if current_account.zql != 0.0:
    #                         pending_value = current_account.zql
    #                         break
    #                 line['zql'] = pending_value
    #     if 'dhl' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 lines = self.search(cr, uid, line['__domain'], context=context)
    #                 pending_value = 0.0
    #                 for current_account in self.browse(cr, uid, lines, context=context):
    #                     if current_account.dhl != 0.0:
    #                         pending_value = current_account.dhl
    #                         break
    #                 line['dhl'] = pending_value
    #     if 'gwxs' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['gwxs'] = 0.0
    #     if 'jjdj' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['jjdj'] = 0.0
    #     if 'sskcs' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['sskcs'] = 0.0
    #     if 'sskcs' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 line['sskcs'] = 0.0
    # if 'jj' in fields:
    #     for line in res:
    #         if '__domain' in line:
    #             lines = self.search(cr, uid, line['__domain'], context=context)
    #             # paramater
    #             cwl = 0.00000
    #             zql = 0.00000
    #             dhl = 0.00000
    #             jjdj, sskcs = 0.0, 0.0
    #             sh_jjdj = 0.0
    #             sh_sskcs = 0.0
    #             # zj
    #             jblr_mul_gwxs_ae = 0.0
    #             jjzzj_bb = 0.0
    #             shywlxj_cy = 0.0

    #             # jj
    #             pending_value = 0.0 # total jj
    #             lrjj_be = 0.0
    #             lrzlj_bk = 0.0
    #             shjj_db = 0.0

    #             datas = self.browse(cr, uid, lines, context=context)
    #             teller_num = datas[0].teller_num
    #             teller_name =datas[0].teller_name
    #             identity = datas[0].identity
    #             quarters = datas[0].quarters
    #             quarters_date = datas[0].quarters_date
    #             group = datas[0].group
    #             role = datas[0].role
    #             role1 = datas[0].role1
    #             # 基础岗位
    #             if role1 != u'专业化岗位':
    #                 # get jblr_mul_gwxs_ae
    #                 for current_account in datas:
    #                     if current_account.ywlx in gwxs_role_list and u'绩效' in current_account.source_from:
    #                         jblr_mul_gwxs_ae += current_account.zshzjs * current_account.gwxs

    #                 # get jjzzj_bb
    #                 except_list=[]
    #                 for plsp in performancelurushenheparameter_datas:
    #                     role_list = [i for i in plsp.role.split(',')]
    #                     except_list.extend(role_list)
    #                     role_set = set(role_list) - set(gwxs_role_list)
    #                     if plsp.quarters == u'录入岗':
    #                         for i in datas:
    #                             if i.ywlx in role_set:
    #                                 jjzzj_bb += i.zshzjs
    #                             cwl = i.cwl if i.cwl != 0.0 else cwl
    #                             zql = i.zql if i.zql != 0.0 else zql
    #                             dhl = i.dhl if i.dhl != 0.0 else dhl
    #                             jjdj = i.jjdj if i.jjdj != 0.0 else jjdj
    #                             sskcs = i.sskcs if i.sskcs != 0.0 else sskcs
    #                     elif plsp.quarters == u'审核岗':
    #                         for i in datas:
    #                             if i.ywlx in role_list:
    #                                 shywlxj_cy += i.zshzjs
    #                                 sh_jjdj = i.jjdj
    #                                 sh_sskcs = i.sskcs
    #                 _logger = logging.getLogger(__name__)

    #                 jjzzj_bb += jblr_mul_gwxs_ae
    #                 lrjj_be = jjzzj_bb * jjdj - sskcs

    #                 for i in performancegoal_datas:
    #                     if i.role == role and  i.role1 == role1:
    #                         zqlxs = (1+(zql-i.zql_goal)*100)
    #                         lhlxs = (1+(i.fql_goal - dhl))
    #                         lrzlj_bk = zqlxs*lhlxs
    #                         lrzlj_bk = (lrzlj_bk - 1) * lrjj_be

    #                 shjj_db = shywlxj_cy * sh_jjdj - sh_sskcs

    #                 for i in datas:
    #                     if i.ywlx not in except_list:
    #                         pending_value += i.zshzjs

    #                 pending_value += lrjj_be + lrzlj_bk + shjj_db

    #             else:
    #                 # 专业化
    #                 # performanceparameter_datas_ids = self.pool['hr.performanceparameter'].search(cr, uid, [('quarters', '=', u'专业化岗位')], context=context)
    #                 # performanceparameter_datas = self.pool.get('hr.performanceparameter').browse(cr, uid, performanceparameter_datas_ids, context=context)
    #                 # standard_trans = u'标准化业务-'
    #                 # for i in datas:
    #                 #     for para in performanceparameter_datas:
    #                 #         role = para.role
    #                 #         if standard_trans in para.role:
    #                 #             role = para.role.replace(standard_trans,'')
    #                 #         if role == i.ywlx:
    #                 #             pending_value += i.zshzjs * para.parameter_valuex
    #                 pending_value = sum([i.zshzjs for i in datas])
    #             line['jj'] = pending_value
    # if 'amount_payed' in fields:
    #     for line in res:
    #         if '__domain' in line:
    #             lines = self.search(cr, uid, line['__domain'], context=context)
    #             payed_value = 0.0
    #             for current_account in self.browse(cr, uid, lines, context=context):
    #                 payed_value += current_account.amount_payed
    #             line['amount_payed'] = payed_value
    # return res


class HrPerformanceBonusTotal(models.Model):  # 奖金计算汇总new
    _name = 'hr.performancebonustotal'
    _description = 'Hr Performance Bonus Total'
    _order = 'id'

    cal_process = fields.Char(u'计算过程')
    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    identity = fields.Char(u'身份')
    quarters = fields.Char(u'岗位')
    quarters_date = fields.Date(u'当前岗位上岗日期')
    group = fields.Char(u'组别')
    role = fields.Char(u'角色')
    role1 = fields.Char(u'角色1')
    zshzjs = fields.Float(u'折算后字节数')
    jblr_mul_gwxs_ae = fields.Float(u'基本录入总字节*岗位系数AE')
    jjzzj_bb = fields.Float(u'计奖总字节BB')
    lrjjdj_bc = fields.Float(u'录入计奖单价BC', digits=(5, 5))
    sskc_bd = fields.Float(u'录入速算扣除数BD')
    lrjj_be = fields.Float(u'录入奖金BE')
    lrzlj_bk = fields.Float(u'录入质量奖BK')
    shywlxj_cy = fields.Float(u'审核业务量小计CY')
    shjjdj_cz = fields.Float(u'审核计奖单价CZ', digits=(5, 5))
    shsskc_da = fields.Float(u'审核速算扣除数DA')
    shjj_db = fields.Float(u'审核奖金DB')
    zyhgwjbzywzshs_dy = fields.Float(u'专业标准折算耗时DY')
    zyhgwbzj_dz = fields.Float(u'专业化岗位标准奖DZ')
    bs = fields.Float(u'补时')
    zyhywbzhs = fields.Float(u'当月专业化业务总标准耗时')
    jbzywzshs = fields.Float(u'兼标准业务折算耗时')
    kj = fields.Float(u'扣奖')
    jj = fields.Float(u'奖金')
    ranking = fields.Integer(u'排名')
    ratio = fields.Float(u'整体系数', digits=(5, 5))
    manager_ratio = fields.Float(u'作业经理系数', digits=(5, 5))
    ywlwclkhywl = fields.Float(u'业务量完成率考核业务量')

    complete_rate = fields.Float(u'完成率', digits=(5, 5))  # 录入复核， 差错外联审核，专业化
    complete_changed_rate = fields.Float(u'调整后成率', digits=(5, 5))
    manual_jj = fields.Float(u'手加减奖金')
    performancebonusdetail_ids = fields.One2many(
        'hr.performancebonus', 'performancebonustotal_id', "performancebonus")
    other_datas = fields.Text(u'其他奖金明细')
# class HrPerformanceBonusTotalDetail(models.Model):  # 奖金计算new
#     _name = 'hr.performancebonustotaldetail'
#     _description = 'Hr Performance Bonus Total Detail'
#     _order = 'id'

#     performancebonustotal_id=fields.Many2one('hr.performancebonustotal', 'Hr Performance Bonus Total', ondelete='cascade', required=True)
#     teller_num = fields.Char(u'柜员号')
#     teller_name = fields.Char(u'柜员名')
#     identity = fields.Char(u'身份')
#     quarters = fields.Char(u'岗位')
#     quarters_date = fields.Date(u'当前岗位上岗日期')
#     group = fields.Char(u'组别')
#     role = fields.Char(u'角色')
#     role1 = fields.Char(u'角色1')
#     ywlx = fields.Char(u'业务类型')
#     ywzhs = fields.Float(u'业务总耗时')
#     ywzl = fields.Float(u'业务总量')
#     hzs = fields.Float(u'汉字数')
#     zjs = fields.Float(u'字节数')
#     ccs = fields.Float(u'差错数')
#     tjyxmh = fields.Float(u'提交影像模糊')
#     cwl = fields.Float(u'错误率', digits=(5, 5))
#     zql = fields.Float(u'正确率', digits=(5, 5))
#     dhl = fields.Float(u'打回率', digits=(5, 5))
#     # jbzjs = fields.Float(u'基本字节数')
#     gwxs = fields.Float(u'岗位系数')
#     zshzjs = fields.Float(u'折算后字节数')
#     jjdj = fields.Float(u'计奖单价', digits=(5, 5))
#     sskcs = fields.Float(u'速算扣除数')
#     khxs = fields.Float(u'考核系数')
#     kj = fields.Float(u'扣奖')
#     jj = fields.Float(u'奖金')
#     ranking = fields.Integer(u'排名')
#     ratio = fields.Float(u'整体系数')
#     manager_ratio = fields.Float(u'作业经理系数')
#     complete_rate = fields.Float(u'完成率')
#     complete_changed_rate = fields.Float(u'调整后成率')
#     source_from = fields.Char(u'数据来源', readonly=True)


class HrPerformanceReportOri(models.Model):  # 总行数据处理中心绩效考核报表
    _name = 'hr.performancereportori'
    _description = 'Hr Performance Report Ori'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    role = fields.Char(u'角色')
    ywzhs = fields.Float(u'业务总耗时(分钟)')
    ywzl = fields.Integer(u'业务总量')
    lrhzs = fields.Integer(u'录入汉字数')
    lrzjs = fields.Integer(u'录入字节数')
    lrccs = fields.Integer(u'录入差错数')
    tjyxmh = fields.Integer(u'提交影像模糊')
    lrcwl = fields.Float(u'录入错误率', digits=(5, 5))
    lrzql = fields.Float(u'录入正确率', digits=(5, 5))
    lrdhl = fields.Float(u'录入打回率', digits=(5, 5))
    shdhs = fields.Integer(u'审核打回数')
    ythqtdhs = fields.Integer(u'用途和其他审核打回数')
    rqshdhs = fields.Integer(u'日期审核打回数')
    jeshdhs = fields.Integer(u'金额审核打回数')
    skrshdhs = fields.Integer(u'收款人审核打回数')
    fkrshdhs = fields.Integer(u'付款人审核打回数')
    bsshdhs = fields.Integer(u'背书审核打回数')
    shdhl = fields.Float(u'审核打回率', digits=(5, 5))
    sqdhs = fields.Integer(u'授权打回数')
    sqdhl = fields.Float(u'授权打回率', digits=(5, 5))
    pjclsd = fields.Float(u'平均处理速度')
    pzhs = fields.Float(u'批注耗时')
    yxdw_zhjh = fields.Float(u'影像定位账户激活')
    yxdw_qt = fields.Float(u'影像定位其他')


class HrPerformanceMobileReportOri(models.Model):  # 信移业务绩效考核报表
    _name = 'hr.performancemobilereportori'
    _description = 'Hr Performance Mobile Report Ori'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    role = fields.Char(u'角色')
    ywzhs = fields.Float(u'业务总耗时(分钟)')
    ywbs = fields.Integer(u'业务笔数')
    zrwxzs = fields.Integer(u'子任务项总数')
    cctwzhs = fields.Float(u'超长业务总耗时（分钟）')
    ccywzl = fields.Integer(u'超长业务总量')
    cczrwxzs = fields.Integer(u'超长子任务项总数')
    lrhzs = fields.Integer(u'录入汉字数')
    lrzjs = fields.Integer(u'录入字节数')
    ccs = fields.Integer(u'差错数')
    tjyxmhs = fields.Integer(u'提交影像模糊数')
    cwl = fields.Float(u'错误率', digits=(5, 5))
    zql = fields.Float(u'正确率', digits=(5, 5))
    yxmhl = fields.Float(u'影像模糊率', digits=(5, 5))
    jjgtg = fields.Integer(u'检件岗(通过)')
    jjgbtg = fields.Integer(u'检件岗(不通过)')
    jjgdqrdbj = fields.Integer(u'检件岗(待确认待补件)')
    dhlxgtg = fields.Integer(u'电话联系岗(通过)')
    dhlxgbtg = fields.Integer(u'电话联系岗(不通过)')
    dhlxgbj = fields.Integer(u'电话联系岗(补件)')
    ccgthqt = fields.Integer(u'差错岗(退回前台)')
    ccgcxtj = fields.Integer(u'差错岗(重新提交)')
    ccgdhlx = fields.Integer(u'差错岗(电话联系)')
    clsd = fields.Float(u'处理速度', digits=(5, 5))


class HrPerformanceBranchReportOri(models.Model):  # 双中心总行数据处理中心绩效考核报表
    _name = 'hr.performancebranchreportori'
    _description = 'Hr Performance Branch Report Ori'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    role = fields.Char(u'角色')
    ywzhs = fields.Float(u'业务总耗时(分钟)')
    ywzl = fields.Integer(u'业务总量')
    lrhzs = fields.Integer(u'录入汉字数')
    lrzjs = fields.Integer(u'录入字节数')
    lrccs = fields.Integer(u'录入差错数')
    tjyxmh = fields.Integer(u'提交影像模糊')
    lrcwl = fields.Float(u'录入错误率', digits=(5, 5))
    lrzql = fields.Float(u'录入正确率', digits=(5, 5))
    lrdhl = fields.Float(u'录入打回率', digits=(5, 5))
    shdhs = fields.Integer(u'审核打回数')
    ythqtdhs = fields.Integer(u'用途和其他审核打回数')
    rqshdhs = fields.Integer(u'日期审核打回数')
    jeshdhs = fields.Integer(u'金额审核打回数')
    skrshdhs = fields.Integer(u'收款人审核打回数')
    fkrshdhs = fields.Integer(u'付款人审核打回数')
    bsshdhs = fields.Integer(u'背书审核打回数')
    shdhl = fields.Float(u'审核打回率', digits=(5, 5))
    yxdw_zhjh = fields.Float(u'影像定位账户激活')
    yxdw_qt = fields.Float(u'影像定位其他')


class HrPerformanceBranchMobileReportOri(models.Model):  # 双中心信移业务绩效考核报表
    _name = 'hr.performancebranchmobilereportori'
    _description = 'Hr Performance Branch Mobile Report Ori'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    role = fields.Char(u'角色')
    ywzhs = fields.Float(u'业务总耗时(分钟)')
    ywbs = fields.Integer(u'业务笔数')
    zrwxzs = fields.Integer(u'子任务项总数')
    lrhzs = fields.Integer(u'录入汉字数')
    lrzjs = fields.Integer(u'录入字节数')
    lrccs = fields.Integer(u'录入差错数')
    tjyxmhs = fields.Integer(u'提交影像模糊数')
    lrcwl = fields.Float(u'录入错误率', digits=(5, 5))
    lrzql = fields.Float(u'录入正确率', digits=(5, 5))
    yxmhl = fields.Float(u'影像模糊率', digits=(5, 5))


class HrPerformanceRoleOri(models.Model):  # 角色表
    _name = 'hr.performanceroleori'
    _description = 'Hr Performance Role Ori'
    _order = 'id'

    work_num = fields.Char(u'工号')
    teller_num = fields.Char(u'柜员号')
    name = fields.Char(u'姓名')
    work_center = fields.Char(u'所属作业中心')
    work_group = fields.Char(u'组别')
    quarters = fields.Char(u'岗位名称')
    role = fields.Char(u'角色')
    role1 = fields.Char(u'角色1')
    need_calculation = fields.Char(u'是否计算')


class HrPerformanceBonusCalculation(models.Model):  # 奖金计算
    _name = 'hr.performancebonuscalculation'
    _description = 'Hr Performance Bonus Calculation'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    identity = fields.Char(u'身份')
    quarters = fields.Char(u'岗位')
    quarters_date = fields.Date(u'当前岗位上岗日期')
    group = fields.Char(u'组别')
    role = fields.Char(u'角色')
    role1 = fields.Char(u'角色1')

    # performancereportori_ids=fields.One2many('hr.performancereportori','performancereportori','performancereportori')


class HrPerformanceSpecialistPortfolioCalculation(models.Model):  # 专业化岗位业务量计算表
    _name = 'hr.performancespecialistportfoliocalculation'
    _description = 'Hr Performance Specialist Portfolio Calculation'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    identity = fields.Char(u'身份')
    quarters = fields.Char(u'岗位')
    quarters_date = fields.Date(u'当前岗位上岗日期')
    group = fields.Char(u'组别')
    role = fields.Char(u'角色')
    role1 = fields.Char(u'角色1')


class HrPerformanceGlobalParameter(models.Model):  # 岗位系数
    _name = 'hr.performanceglobalparameter'
    _description = 'Hr Performance Global Parameter'
    _order = 'id'

    parameter_name = fields.Char(u'参数名称')
    parameter_value = fields.Float(u'参数值')


class HrPerformanceGoal(models.Model):  # 正确放弃系数
    _name = 'hr.performancegoal'
    _description = 'Hr Performance Goal'
    _order = 'id'

    role = fields.Char(u'角色')
    role1 = fields.Char(u'角色1')
    zql_goal = fields.Float(u'正确率目标',  digits=(5, 5))
    fql_goal = fields.Float(u'放弃率目标',  digits=(5, 5))

# TODO: role field require only one


class HrPerformanceParameter(models.Model):  # 计奖参数
    _name = 'hr.performanceparameter'
    _description = 'Hr Performance Parameter'
    _order = 'id'

    quarters = fields.Char(u'岗位')
    jjfs = fields.Selection(
        [('byTime', u'按时'), ('byByte', u'按字节'),
         ('byQuantity', u'按笔数'), ('bySub', u'按子任务项')],
        string=u'计奖方式',
        required=True,
        default='byTime')
    role = fields.Char(u'角色')
    parameter_name = fields.Char(u'参数名称')
    parameter_valuex = fields.Float(u'参数值', digits=(4, 4))

    def __str__():
        return u'计奖参数'


class HrPerformanceLuRuShenHeParameter(models.Model):  # 录入审核计奖参数
    _name = 'hr.performancelurushenheparameter'
    _description = 'Hr Performance LuRu ShenHe Parameter'
    _order = 'id'

    quarters = fields.Char(u'岗位')
    role = fields.Char(u'角色', help=u'使用英语的逗号')
    parameter_name = fields.Char(u'参数名称')
    daily_quantity = fields.Char(u'日均字节/业务量')
    work_day = fields.Float(u'工作日')
    quantity = fields.Char(u'字节/业务量')
    unit_price = fields.Char(u'单价', digits=(5, 5))
    price_add_minus = fields.Char(u'速算扣除')

    # @api.onchange('work_day')
    # def _onchange_work_day(self):
    # for record in self.env['hr.performancelurushenheparameter'].search([]):
    # record.write({'work_day': self.work_day})
    # @api.one
    # @api.depends('daily_quantity')
    # def _compute_quantity(self):
    #     work_day=self.env['hr.performanceglobalparameter'].search([('parameter_name','=','工作日')])
    #     self.quantity=int(self.daily_quantity)*int(work_day.parameter_value)

    # @api.one
    # @api.depends('quarters','quantity','unit_price')
    # def _compute_price_add_minus(self):
    #     if self.quarters==u"录入岗":
    #         if self.quantity==0:
    #             self.price_add_minus=0.00
    #         else:
    #             performancelurushenheparameters=self.env['hr.performancelurushenheparameter'].search([('quarters','=','录入岗')])
    #             l1=[]
    #             for p in performancelurushenheparameters:
    #                 l1.append([p.daily_quantity,p.quantity,p.unit_price])
    #                 self.price_add_minus=p.daily_quantity
    #             l1.sort(lambda x,y:cmp(x[0],y[0]))
    #             if self.daily_quantity==l1[1][0]:
    #                 self.price_add_minus= float(l1[1][1])* float(l1[1][2]-l1[0][2])
    #             else:
    #                 self.price_add_minus=float(l1[1][1]-l1[0][1])* float(l1[2][2]-l1[0][2])+float(l1[2][1]-l1[1][1])* float(l1[2][2]-l1[1][2])
    #     elif self.quarters==u"审核岗":
    #         if self.quantity==0:
    #             self.price_add_minus=0.00
    #         else:
    #             performancelurushenheparameters=self.env['hr.performancelurushenheparameter'].search([('quarters','=','审核岗')])
    #             l1=[]
    #             for p in performancelurushenheparameters:
    #                 l1.append([p.daily_quantity,p.quantity,p.unit_price])
    #             l1.sort(lambda x,y:cmp(x[0],y[0]))
    #             self.price_add_minus= float(l1[1][1])* float(l1[1][2]-l1[0][2])


class HrPerformanceTele(models.Model):  # 电联
    _name = 'hr.performancetele'
    _description = 'Hr Performance Tele'
    _order = 'id'

    teller_name = fields.Char(u'柜员名')
    role = fields.Char(u'角色')
    ywzhs = fields.Float(u'业务总耗时(分钟)')
    ywzl = fields.Integer(u'总业务量')
    hcywl = fields.Integer(u'呼出业务量')
    hrywl = fields.Integer(u'呼入业务量')
    bjywhshywl = fields.Integer(u'补救业务核算后业务量')
    dyhbjywhshywl = fields.Integer(u'待银行补件业务核算后业务量')
    yxdw = fields.Integer(u'影像定位')
    hzlzhjh = fields.Integer(u'核准类账户激活(25)')
    zrwxzs = fields.Integer(u'子任务项总数')
    wjtdhgs = fields.Integer(u'未接通电话个数')
    jtdhgs = fields.Integer(u'接通电话个数')
    jtdhzsc = fields.Integer(u'通话总时长(分钟)')
    thgs = fields.Integer(u'通话个数')
    pjthsc = fields.Integer(u'平均通话时长(分钟)')


class HrPerformanceByStandardOri(models.Model):  # 按标准计奖岗考核
    _name = 'hr.performancebystandardori'
    _description = 'Hr Performance By Standard Ori'
    _order = 'id'

    work_num = fields.Char(u'工号')
    name = fields.Char(u'姓名')
    quarters = fields.Char(u'岗位名称')
    quarters_date = fields.Date(u'当前岗位上岗日期')
    work_center = fields.Char(u'所属作业中心')
    work_group = fields.Char(u'组别')
    kpi = fields.Char(u'当月考评')
    kpi_param = fields.Float(u'得奖系数')
    standard_bonus = fields.Float(u'标准奖金')
    remark = fields.Char(u'备注')


# class HrPerformanceBonusTotal(models.Model):  # 奖金汇总
#     _name = 'hr.performancebonustotal'
#     _description = 'Hr Performance Bonus Total'
#     _order = 'id'

#     teller_num = fields.Char(u'柜员号')
#     work_num = fields.Char(u'工号')
#     teller_name = fields.Char(u'姓名')
#     quarters = fields.Char(u'聘用岗位')
#     role = fields.Char(u'柜员角色')
#     group = fields.Char(u'组别')
#     identity = fields.Char(u'员工身份')
#     jjjsz = fields.Float(u'奖金计算值')
#     qttz = fields.Float(u'其他调整')
#     jxjjxj = fields.Float(u'绩效奖金小计', compute='_compute_jxjjxj', store=True)
#     jljkzj = fields.Float(u'经理加扣总计')
#     jljkbz = fields.Char(u'经理加扣备注')
#     jljkzj = fields.Float(u'经理加扣总计')
#     sfjj = fields.Float(u'实发奖金', compute='_compute_sfjj', store=True)
#     remark = fields.Char(u'备注')
#     yjj = fields.Float(u'原奖金')
#     bc = fields.Float(u'补差', compute='_compute_bc', store=True)

#     @api.depends('jjjsz', 'qttz')
#     def _compute_jxjjxj(self):
#         self.jxjjxj = self.jjjsz+self.qttz

#     @api.depends('jjjsz', 'qttz', 'jljkzj')
#     def _compute_sfjj(self):
#         self.sfjj = self.jjjsz+self.qttz+self.jljkzj

#     @api.depends('jjjsz', 'qttz', 'jljkzj', 'yjj')
#     def _compute_bc(self):
#         self.bc = self.jjjsz+self.qttz+self.jljkzj-self.yjj


# class HrPerformanceBasicAllowance(models.Model):  # 基础补业务量明细表
#     _name = 'hr.performancebasicallowance'
#     _description = 'Hr Performance Basic Allowance'
#     _order = 'id'

#     work_num = fields.Char(u'工号')
#     teller_name = fields.Char(u'姓名')
#     group = fields.Char(u'组别')
#     area = fields.Char(u'区域')
#     role = fields.Char(u'柜员角色')
#     jjywsj1 = fields.Float(u'加减业务时间（作业经理）')
#     jjywsj2 = fields.Float(u'加减业务时间（管理组）')
#     jjywsj3 = fields.Float(u'加减业务时间（调度及流程管理组）')
#     jjywsj4 = fields.Float(u'加减业务时间（人事组）')
#     jjywsj5 = fields.Float(u'加减业务时间（IT行政组）')
#     jjywsjxj = fields.Float(u'加减业务时间小计')
#     mxsbtywl = fields.Float(u'每小时补贴业务量')
#     btywlxj = fields.Float(u'补贴业务量小计')
#     remark = fields.Char(u'备注')


class HrPerformanceProAllowance(models.Model):  # 专业化岗业务量及工时补贴表
    _name = 'hr.performanceproallowance'
    _description = 'Hr Performance Pro Allowance'
    _order = 'id'

    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    quarters = fields.Char(u'岗位')
    role = fields.Char(u'柜员角色')
    group = fields.Char(u'组别')
    ywlx = fields.Char(u'角色')
    ywzl = fields.Float(u'业务总量')
    join_date = fields.Char(u'当月上岗时间')
    minus_date = fields.Char(u'新上岗员工当月应扣发天数')
    # jjywsj1 = fields.Float(u'加减业务时间作业经理')
    # jjywsj2 = fields.Float(u'加减业务时间管理组')
    # jjywsj3 = fields.Float(u'加减业务时间调度及流程管理组')
    # jjywsj4 = fields.Float(u'加减业务时间人事组')
    # jjywsj5 = fields.Float(u'加减业务时间IT行政组')
    # total_time = fields.Float(u'总业务时间')


class HrPerformancePlusMinus(models.Model):  # 基础作业岗工时补贴表-
    _name = 'hr.performanceplusminus'
    _description = 'Hr Performance PlusMinus'
    _order = 'id'

    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    group = fields.Char(u'组别')
    area = fields.Char(u'区域')
    role = fields.Char(u'角色')
    jjywsj1 = fields.Float(u'加减业务时间作业经理')
    jjywsj2 = fields.Float(u'加减业务时间管理组')
    jjywsj3 = fields.Float(u'加减业务时间调度及流程管理组')
    jjywsj4 = fields.Float(u'加减业务时间人事组')
    jjywsj5 = fields.Float(u'加减业务时间IT行政组')
    jjywsjxj = fields.Float(u'加减业务时间小计')
    mxsbtywl = fields.Float(u'每小时补贴业务量')
    btywlxj = fields.Float(u'补贴业务量小计')
    remark = fields.Float(u'备注')


class HrPerformanceProName(models.Model):  # 专业化业务
    _name = 'hr.performanceproname'
    _description = 'Hr Performance Pro Name'
    _order = 'id'

    quarters = fields.Char(u'岗位')
    ywmc = fields.Char(u'业务名称')
    total_time = fields.Float(u'耗时')


class HrPerformanceAttendance(models.Model):  # 考勤
    _name = 'hr.performanceattendance'
    _description = 'Hr Performance Attendance'
    _order = 'id'

    teller_id = fields.Char(u'序号')
    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    sap_num = fields.Char(u'SAP系统工号')
    person_manage_num = fields.Char(u'人员管理系统人员编号')
    department = fields.Char(u'部门')
    quarters = fields.Char(u'聘用岗位')
    role = fields.Char(u'柜员角色')
    group = fields.Char(u'组别')
    manager = fields.Char(u'区域负责人')
    emp_type = fields.Char(u'员工身份')
    enter_date = fields.Char(u'进公司日期')
    leave_date = fields.Char(u'在职情况')
    attendance_basic = fields.Float(u'应出勤')
    attendance_actual = fields.Float(u'出勤日')


class HrPerformanceMemberInfo(models.Model):  # 人员信息导入
    _name = 'hr.performancememberinfo'
    _description = 'Hr Performance Member Information'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    gender = fields.Char(u'性别')
    orgnization = fields.Char(u'机构')
    quarters = fields.Char(u'岗位')
    quarters_date = fields.Char(u'当前岗位上岗日期')
    role = fields.Char(u'柜员角色')
    group = fields.Char(u'组别')
    area_manager = fields.Char(u'区域负责人')
    join_date = fields.Char(u'进中心日期')
    adjusted_join_date = fields.Char(u'调整的进中心日期')
    job_status = fields.Char(u'在职情况')
    leave_date = fields.Char(u'离职日期')
    leave_reason = fields.Char(u'离职原因')
    age = fields.Integer(u'年龄')
    adjusted_working_date = fields.Char(u'调整后的参加工作时间')
    recruite_from = fields.Char(u'招聘来源')
    degree = fields.Char(u'最高教育学历')
    school = fields.Char(u'最高学历毕业院校')
    job_nature = fields.Char(u'岗位性质')
    job_importance = fields.Char(u'岗位重要度')


class HrPerformanceProFixedBonus(models.Model):  # 专业化岗位标准奖金
    _name = 'hr.performanceprofixedbonus'
    _description = 'Hr Performance Pro Fixed Bonus'
    _order = 'id'

    role = fields.Char(u'角色')
    jj = fields.Float(u'奖金')


class HrPerformanceCapBasic(models.Model):  # 标准业务组长考核
    _name = 'hr.performancecapbasic'
    _description = 'Hr Performance Cap Basic'
    _order = 'id'

    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    quarters = fields.Char(u'岗位')
    group = fields.Char(u'组别')
    manager = fields.Char(u'区域负责人')
    salary_level = fields.Char(u'薪资等级')
    ywlkh_avg = fields.Float(u'业务量考核平均完成率', digits=(5, 5))
    ywlkh_khqk = fields.Char(u'完成率考核情况')
    zqlkh_avg = fields.Float(u'业务量考核情况平均正确率', digits=(5, 5))
    zqlkh_khqk = fields.Char(u'正确率考核情况')
    dhlkh_avg = fields.Float(u'业务量考核情况平均打回率', digits=(5, 5))
    dhlkh_khqk = fields.Char(u'打回率考核情况')
    complete_rate = fields.Float(u'完成率', digits=(5, 5))  # 录入复核， 差错外联审核，专业化
    manage_area_score = fields.Float(u'管理指标考核得分')
    jj_rate = fields.Float(u'奖金系数')
    standard_bonus = fields.Float(u'标准绩效奖')
    fix_bonus = fields.Float(u'组长考核奖')
    bonus = fields.Float(u'奖金')
    addition_bonus = fields.Float(u'业务量完成可得组长岗位津贴')
    total_bonus = fields.Float(u'奖金合计')
    actual_bonus = fields.Float(u'实际奖金')
    cap_bonus = fields.Float(u'组长考核奖')
    remark = fields.Char(u'备注')
    remark2 = fields.Char(u'备注2')


class HrPerformanceCapPro(models.Model):  # 专业化业务组长考核
    _name = 'hr.performancecappro'
    _description = 'Hr Performance Cap Pro'
    _order = 'id'

    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    quarters = fields.Char(u'岗位')
    group = fields.Char(u'组别')
    manager = fields.Char(u'区域负责人')
    salary_level = fields.Char(u'薪资等级')
    ywlkh_avg = fields.Float(u'个人业务量完成率', digits=(5, 5))
    manage_area_score = fields.Float(u'管理指标考核得分')
    jj_rate = fields.Float(u'奖金系数')
    standard_bonus = fields.Float(u'标准绩效奖')
    fix_bonus = fields.Float(u'组长考核奖')
    bonus = fields.Float(u'奖金')
    addition_bonus = fields.Float(u'业务量完成可得组长岗位津贴')
    total_bonus = fields.Float(u'奖金合计')
    actual_bonus = fields.Float(u'实际奖金')
    cap_bonus = fields.Float(u'组长考核奖')
    remark = fields.Char(u'备注')


class HrPerformanceTelePara(models.Model):  # 外联系数，临时系数
    _name = 'hr.performancetelepara'
    _description = 'Hr Performance Tele Para'
    _order = 'id'

    role = fields.Char(u'角色')
    paramater = fields.Float(u'系数', digits=(5, 5))
    para_type = fields.Char(u'系数类型')


class HrPerformanceTeleAdditionReportOri(models.Model):  # 外联附加报表
    _name = 'hr.performanceteleadditionreportori'
    _description = 'Hr Performance Tele Addition Report Ori'
    _order = 'id'

    teller_name = fields.Char(u'柜员名')
    role = fields.Char(u'角色')
    dhlxywzhs = fields.Float(u'电话联系业务总耗时')
    zywl = fields.Float(u'总业务量')
    yxdw = fields.Float(u'影像定位')
    hzlzhjh = fields.Float(u'核准类账户激活')
    hcywl = fields.Float(u'呼出业务量')
    hrywl = fields.Float(u'呼入业务量')
    bjhshywl = fields.Float(u'补救核算后业务量')
    dyhbjywhshywl  = fields.Float(u'待银行补件业务核算后业务量')
