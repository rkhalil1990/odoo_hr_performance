# -*- coding: utf-8 -*-

from openerp import api, fields, models, fields
from openerp import _, tools
from openerp.exceptions import UserError, AccessError
from datetime import date, datetime, timedelta
import calendar


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
    zql = fields.Float(u'正确率', digits=(5, 5))
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


# class HrPerformanceBonus(models.Model):  # 奖金计算new
#     _name = 'hr.performancebonus'
#     _description = 'Hr Performance Bonus'
#     _order = 'id'

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
#     cwl = fields.Float(u'错误率')
#     zql = fields.Float(u'正确率')
#     dhl = fields.Float(u'打回率')
#     jbzjs = fields.Float(u'基本字节数')
#     gwxs = fields.Float(u'岗位系数')
#     zshzjs = fields.Float(u'折算后字节数')
#     jjdj = fields.Float(u'计奖单价')
#     sskcs = fields.Float(u'速算扣除数')
#     khxs = fields.Float(u'考核系数')
#     kj = fields.Float(u'扣奖')
#     jj = fields.Float(u'奖金')
#     ranking = fields.Integer(u'排名')
#     ratio = fields.Float(u'整体系数')
#     manager_ratio = fields.Float(u'作业经理系数')
#     complete_rate = fields.Float(u'完成率')


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
    lrcwl = fields.Float(u'录入错误率')
    lrzql = fields.Float(u'录入正确率')
    lrdhl = fields.Float(u'录入打回率')
    shdhs = fields.Integer(u'审核打回数')
    ythqtdhs = fields.Integer(u'用途和其他审核打回数')
    rqshdhs = fields.Integer(u'日期审核打回数')
    jeshdhs = fields.Integer(u'金额审核打回数')
    skrshdhs = fields.Integer(u'收款人审核打回数')
    fkrshdhs = fields.Integer(u'付款人审核打回数')
    bsshdhs = fields.Integer(u'背书审核打回数')
    shdhl = fields.Float(u'审核打回率')
    sqdhs = fields.Integer(u'授权打回数')
    sqdhl = fields.Float(u'授权打回率')
    pjclsd = fields.Float(u'平均处理速度')
    pzhs = fields.Float(u'批注耗时')


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
    cwl = fields.Float(u'错误率')
    zql = fields.Float(u'正确率')
    yxmhl = fields.Float(u'影像模糊率')
    jjgtg = fields.Integer(u'检件岗(通过)')
    jjgbtg = fields.Integer(u'检件岗(不通过)')
    jjgdqrdbj = fields.Integer(u'检件岗(待确认待补件)')
    dhlxgtg = fields.Integer(u'电话联系岗(通过)')
    dhlxgbtg = fields.Integer(u'电话联系岗(不通过)')
    dhlxgbj = fields.Integer(u'电话联系岗(补件)')
    ccgthqt = fields.Integer(u'差错岗(退回前台)')
    ccgcxtj = fields.Integer(u'差错岗(重新提交)')
    ccgdhlx = fields.Integer(u'差错岗(电话联系)')
    clsd = fields.Float(u'处理速度')


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
    lrcwl = fields.Float(u'录入错误率')
    lrzql = fields.Float(u'录入正确率')
    lrdhl = fields.Float(u'录入打回率')
    shdhs = fields.Integer(u'审核打回数')
    ythqtdhs = fields.Integer(u'用途和其他审核打回数')
    rqshdhs = fields.Integer(u'日期审核打回数')
    jeshdhs = fields.Integer(u'金额审核打回数')
    skrshdhs = fields.Integer(u'收款人审核打回数')
    fkrshdhs = fields.Integer(u'付款人审核打回数')
    bsshdhs = fields.Integer(u'背书审核打回数')
    shdhl = fields.Float(u'审核打回率')


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
    lrcwl = fields.Float(u'录入错误率')
    lrzql = fields.Float(u'录入正确率')
    yxmhl = fields.Float(u'影像模糊率')


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


class HrPerformanceParameter(models.Model):  # 计奖参数
    _name = 'hr.performanceparameter'
    _description = 'Hr Performance Parameter'
    _order = 'id'

    quarters = fields.Char(u'岗位')
    jjfs = fields.Selection(
        [('byTime', u'按时'), ('byByte', u'按字节'), ('byQuantity', u'按笔数')],
        string=u'计奖方式',
        required=True,
        default='byTime')
    role = fields.Char(u'角色')
    parameter_name = fields.Char(u'参数名称')
    parameter_valuex = fields.Float(u'参数值')


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


class HrPerformancePlusMinus(models.Model):  # 加扣
    _name = 'hr.performanceplusminus'
    _description = 'Hr Performance PlusMinus'
    _order = 'id'

    teller_name = fields.Char(u'柜员名')
    work_num = fields.Char(u'工号')
    work_group = fields.Char(u'组别')


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


class HrPerformanceYXDW(models.Model):  # 影像定位
    _name = 'hr.performanceyxdw'
    _description = 'Hr Performance YXDW'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    role = fields.Char(u'角色')
    ywzhs = fields.Float(u'业务总耗时(分钟)')
    yxdwywzl = fields.Integer(u'影像定位业务总量')
    hzlzhjh = fields.Integer(u'其中：核准类账户激活')
    qtywlx = fields.Integer(u'其中：其他业务类型')


class HrPerformanceBonusTotal(models.Model):  # 奖金汇总
    _name = 'hr.performancebonustotal'
    _description = 'Hr Performance Bonus Total'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    quarters = fields.Char(u'聘用岗位')
    role = fields.Char(u'柜员角色')
    group = fields.Char(u'组别')
    identity = fields.Char(u'员工身份')
    jjjsz = fields.Float(u'奖金计算值')
    qttz = fields.Float(u'其他调整')
    jxjjxj = fields.Float(u'绩效奖金小计', compute='_compute_jxjjxj', store=True)
    jljkzj = fields.Float(u'经理加扣总计')
    jljkbz = fields.Char(u'经理加扣备注')
    jljkzj = fields.Float(u'经理加扣总计')
    sfjj = fields.Float(u'实发奖金', compute='_compute_sfjj', store=True)
    remark = fields.Char(u'备注')
    yjj = fields.Float(u'原奖金')
    bc = fields.Float(u'补差', compute='_compute_bc', store=True)

    @api.depends('jjjsz', 'qttz')
    def _compute_jxjjxj(self):
        self.jxjjxj = self.jjjsz+self.qttz

    @api.depends('jjjsz', 'qttz', 'jljkzj')
    def _compute_sfjj(self):
        self.sfjj = self.jjjsz+self.qttz+self.jljkzj

    @api.depends('jjjsz', 'qttz', 'jljkzj', 'yjj')
    def _compute_bc(self):
        self.bc = self.jjjsz+self.qttz+self.jljkzj-self.yjj


class HrPerformanceBasicAllowance(models.Model):  # 补业务量明细表
    _name = 'hr.performancebasicallowance'
    _description = 'Hr Performance Basic Allowance'
    _order = 'id'

    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    group = fields.Char(u'组别')
    area = fields.Char(u'区域')
    role = fields.Char(u'柜员角色')
    jjywsj1 = fields.Float(u'加减业务时间（作业经理）')
    jjywsj2 = fields.Float(u'加减业务时间（管理组）')
    jjywsj3 = fields.Float(u'加减业务时间（调度及流程管理组）')
    jjywsj4 = fields.Float(u'加减业务时间（人事组）')
    jjywsj5 = fields.Float(u'加减业务时间（IT行政组）')
    jjywsjxj = fields.Float(u'加减业务时间小计')
    mxsbtywl = fields.Float(u'每小时补贴业务量')
    btywlxj = fields.Float(u'补贴业务量小计')
    remark = fields.Char(u'备注')


class HrPerformanceBasicAllowancePara(models.Model):  # 补业务量参数
    _name = 'hr.performancebasicallowancepara'
    _description = 'Hr Performance Basic Allowance Para'
    _order = 'id'

    role = fields.Char(u'柜员角色')
    mxsbtywl = fields.Float(u'每小时补贴业务量')
    ywldw = fields.Char(u'业务量单位')
    remark = fields.Char(u'备注')


class HrPerformanceProAllowance(models.Model):  # 专业化业务量明细表
    _name = 'hr.performanceproallowance'
    _description = 'Hr Performance Pro Allowance'
    _order = 'id'

    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'姓名')
    quarters = fields.Char(u'岗位')
    role = fields.Char(u'柜员角色')
    group = fields.Char(u'组别')
    quarters_date = fields.Date(u'当月上岗时间')
    jjywsj1 = fields.Float(u'加减业务时间（调度及流程管理组）')
    jjywsj2 = fields.Float(u'加减业务时间（人事组）')
    jjywsj3 = fields.Float(u'加减业务时间（IT行政组）')
    total_time = fields.Float(u'总业务时间')


class HrPerformanceProName(models.Model):  # 专业化业务
    _name = 'hr.performanceproname'
    _description = 'Hr Performance Pro Name'
    _order = 'id'

    quarters = fields.Char(u'岗位')
    ywmc = fields.Char(u'业务名称')
    total_time = fields.Float(u'耗时')