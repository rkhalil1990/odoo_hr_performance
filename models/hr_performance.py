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
    zsyz = fields.Float(u'折算原值')
 

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
    jj = fields.Float(u'奖金', digits=(18, 2))
    pro_zhs = fields.Float(u'排名用专业总耗时')
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
    attendance_basic = fields.Float(u'应出勤')
    attendance_actual = fields.Float(u'出勤日')
    jk = fields.Float(u'加扣金额', digits=(18, 2))
    jkhjj = fields.Float(u'加扣后奖金', digits=(18, 2))
    jj_without_cap = fields.Float(u'排除组长奖金', digits=(18, 2))
    ywl_datas = fields.Text(u'业务量考核业务量明细')

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

    @api.one
    def set_g_r(self):
        records = self.env['hr.performancememberinfo'].search([])
        for r in records:
            if self.teller_num == r.member_num:
                self.write({'work_group': r.group,'role': r.role}) 

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
         ('byQuantity', u'按笔数'), ('bySub', u'按子任务项'), ('byMulti', u'按字节乘系数')],
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
    minus_date = fields.Integer(u'新上岗员工当月应扣发天数')


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
    leave_date = fields.Char(u'离职日期')
    attendance_basic = fields.Float(u'应出勤')
    attendance_actual = fields.Float(u'出勤日')
    sj = fields.Float(u'250648事假')
    bj = fields.Float(u'250649病假')
    hzj = fields.Float(u'250647婚丧假')
    cdzt = fields.Float(u'迟到早退')
    cdzt0502 = fields.Float(u'迟到早退0502')
    kg = fields.Float(u'250651旷工')
    nxj = fields.Float(u'250651年休假')
    dx = fields.Float(u'250651调休')
    cqj = fields.Float(u'250651产前假')
    cj = fields.Float(u'250653产假')
    gj = fields.Float(u'250655公假')




class HrPerformanceMemberInfo(models.Model):  # 人员信息导入
    _name = 'hr.performancememberinfo'
    _description = 'Hr Performance Member Information'
    _order = 'id'

    member_num = fields.Char(u'人员编号')
    member_record = fields.Char(u'员工记录')
    work_num = fields.Char(u'工号')
    teller_name = fields.Char(u'人员姓名')
    hr_range = fields.Char(u'人事子范围')
    card_num = fields.Char(u'考勤卡号')
    ps_teller_num = fields.Char(u'人员管理系统人员编号')
    gender = fields.Char(u'性别')
    orgnization1 = fields.Char(u'所在机构')
    orgnization2 = fields.Char(u'机构二')
    orgnization3 = fields.Char(u'机构')
    department = fields.Char(u'部门')
    quarters = fields.Char(u'岗位')
    quarters_date = fields.Char(u'当前岗位上岗日期')
    teller_num = fields.Char(u'柜员号')
    role = fields.Char(u'柜员角色')
    group = fields.Char(u'组别')
    area_manager = fields.Char(u'区域负责人')
    teller_type = fields.Char(u'员工类别')
    teller_subtype = fields.Char(u'员工子类别')
    enter_date = fields.Date(u'进中心日期')
    adjusted_enter_date = fields.Date(u'调整的进中心日期')
    company_work_age = fields.Char(u'本中心工龄')
    contract_1st_date = fields.Char(u'首次合同签订日期')
    contract_try_end_date = fields.Date(u'首次合同试用期到期日')
    contract_start_date = fields.Date(u'本次合同开始日期')
    contract_1st_end_date = fields.Date(u'派遣合同到期日')
    contract_count = fields.Char(u'合同累计签订次数')
    company_count = fields.Char(u'当前派遣公司签订次数')
    incumbency = fields.Char(u'在职情况')
    leave_date = fields.Date(u'离职日期')


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
    role = fields.Char(u'考核角色')
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
    role = fields.Char(u'考核角色')
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


class HrPerformanceRemoveMember(models.Model):  # 排除人员
    _name = 'hr.performanceremovemember'
    _description = 'Hr Performance Remove Member'
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    role = fields.Char(u'角色')
    quarters_date = fields.Date(u'当前岗位上岗日期')

class HrPerformanceNotRemoveRole(models.Model):  # 强制不排除组别
    _name = 'hr.performancenotremoverole'
    _description = 'Hr Performance Not Remove Role'
    _order = 'id'

    role = fields.Char(u'角色')


class HrPerformanceProRatio(models.Model):  # 专业化绩效加扣报表
    _name = 'hr.performanceproratio'
    _description = 'Hr Performance Pro Ratio '
    _order = 'id'

    teller_num = fields.Char(u'柜员号')
    teller_name = fields.Char(u'柜员名')
    group = fields.Char(u'组别')
    area = fields.Char(u'区域')
    role = fields.Char(u'角色')
    total_jk = fields.Float(u'加扣金额总计')
    rank = fields.Float(u'专业化岗综合排名')
    ratio = fields.Float(u'专业化岗绩效系数')


class HrPerformanceMonth(models.Model):  # 专业化绩效加扣报表
    _name = 'hr.performancemonth'
    _description = 'Hr Performance Month '
    _order = 'id'

    report_date = fields.Date(u'报表月份')


class HrPerformanceAvgQuarters(models.Model):  # 
    _name = 'hr.performanceavgquarters'
    _description = 'Hr Performance Avg Quarters'
    _order = 'id'

    role = fields.Char(u'角色')
    role1 = fields.Char(u'角色1')
    avg_jjzzj = fields.Float(u'平均值计奖总字节')
    total_ywl = fields.Float(u'总业务量')
    total_ccs = fields.Float(u'总差错数')
    total_mhs = fields.Float(u'总模糊数')
    ccl = fields.Float(u'差错率', digits=(5, 5))
    zql = fields.Float(u'正确率', digits=(5, 5))
    dhl = fields.Float(u'打回率', digits=(5, 5))


class HrPerformanceAvgGroup(models.Model):  # 
    _name = 'hr.performanceavggroup'
    _description = 'Hr Performance Avg Group'
    _order = 'id'

    role = fields.Char(u'角色')
    group = fields.Char(u'组别')
    avg_jjzzj = fields.Float(u'平均值计奖总字节')
    total_ywl = fields.Float(u'总业务量')
    total_ccs = fields.Float(u'总差错数')
    total_mhs = fields.Float(u'总模糊数')
    ccl = fields.Float(u'差错率', digits=(5, 5))
    zql = fields.Float(u'正确率', digits=(5, 5))
    dhl = fields.Float(u'打回率', digits=(5, 5))

class HrPerformanceGWXS(models.Model):  # 岗位系数业务
    _name = 'hr.performancegwxs'
    _description = 'Hr Performance GWXS'
    _order = 'id'

    GWXS_YW = fields.Char(u'岗位系数业务')



class HrPerformanceSumGroup(models.Model):  #
    _name = 'hr.performancesumgroup'
    _description = 'Hr Performance Sum Group'
    _order = 'id'

    role = fields.Char(u'角色')
    role1 = fields.Char(u'角色1')
    total_name = fields.Float(u'计数项:柜员名')
    avg_lrjj = fields.Float(u'平均值项:录入奖金', digits=(5, 5))
    avg_lrzlj = fields.Float(u'平均值项:录入质量奖', digits=(5,5))
    avg_fhjj = fields.Float(u'平均值项:复核奖金', digits=(5, 5))
    avg_zlfhj = fields.Float(u'平均值项:资料复核考核奖(20)', digits=(5, 5))
    avg_xykkhj = fields.Float(u'平均值项:信用卡差错业务考核奖', digits=(5, 5))
    avg_ccjj = fields.Float(u'平均值项:差错奖金(22)', digits=(5, 5))
    avg_xykjc = fields.Float(u'平均值项:信用卡纠错奖金(24)', digits=(5, 5))
    avg_shjj = fields.Float(u'平均值项:审核奖金(34)', digits=(5, 5))
    avg_hhqrj = fields.Float(u'平均值项:行号确认奖（35）', digits=(5, 5))
    avg_xykjj = fields.Float(u'平均值项:信移卡检件奖(36)', digits=(5, 5))
    avg_xykjjfh = fields.Float(u'平均值项:信移卡检件复核奖(37)', digits=(5, 5))
    avg_wl = fields.Float(u'平均值项:外联奖金（38）', digits=(5, 5))
    avg_bzjj = fields.Float(u'平均值项:按标准奖金考核奖（53）', digits=(5, 5))
    avg_btjj = fields.Float(u'平均值项:各岗位补贴奖金(54)', digits=(5, 5))
    avg_zzkhj = fields.Float(u'平均值项:组长考核奖(55)', digits=(5, 5))
    avg_qita = fields.Float(u'平均值项:其他加(56)', digits=(5, 5))
    avg_jjin = fields.Float(u'平均值项:奖金小计', digits=(5, 5))
    

