# -*- coding: utf-8 -*-
import sys
from openerp import api, models
import threading
import logging
import itertools
from operator import itemgetter, attrgetter



reload(sys)
sys.setdefaultencoding('utf-8')
NOTINCLUDEDAYS = 8

class HrPerformanceBonusCompute(models.TransientModel):
    _name = 'hr.performance.bonus.compute'
    _description = 'HR Performancebonus Compute'

    @api.multi
    def performancebonus_compute(self):
        standard_trans = u'标准化业务-'
        mobile_prefix = u'信用卡'
        basic_prefix = u'基础补时'
        pro_prefix = u'专业化补时'
        gwxs_role_list = (u'录入', u'行号选择', u'行号录入',u'英文信息录入')
        lurushenhe_role1_group = (u'A', u'B', u'E', u'F')
        source_list = (u'绩效报表', u'双中心绩效报表', u'信用卡报表',
                       u'双中心信用卡报表', u'专业化补时报表', u'基础补时报表', u'外联附加报表',u'外借等其他')
        performancelurushenheparameter_datas = self.env[
            'hr.performancelurushenheparameter'].search([])  # 录入审核计奖参数
        role_datas = self.env['hr.performanceroleori'].search([])
        for rd in role_datas:
            performancereportori_datas = self.env[
                'hr.performancereportori'].search([('teller_num', '=', rd.teller_num)])
            performancemobilereportori_datas = self.env[
                'hr.performancemobilereportori'].search([('teller_num', '=', rd.teller_num)])
            performancebranchreportori_datas = self.env[
                'hr.performancebranchreportori'].search([('teller_num', '=', rd.teller_num)])
            performancebranchmobilereportori_datas = self.env[
                'hr.performancebranchmobilereportori'].search([('teller_num', '=', rd.teller_num)])
            performanceplusminus_datas = self.env[
                'hr.performanceplusminus'].search([('teller_name', '=', rd.name)])
            performanceproallowance_datas = self.env[
                'hr.performanceproallowance'].search([('teller_name', '=', rd.name)])
            # TODO: need edit teller_name
            performanceteleadditionreportori_datas = self.env[
                'hr.performanceteleadditionreportori'].search([('teller_name', '=', rd.name)])
            performanceattendance_datas = self.env[
                'hr.performanceattendance'].search([('teller_name', '=', rd.name)])
            jjcs = self.env['hr.performanceparameter'].search(
                [('role', '=', rd.role)])
            gwxs = self.env['hr.performanceglobalparameter'].search(
                [('parameter_name', '=', rd.role1)])
            performanceproratio = self.env['hr.performanceproratio'].search(
                [('teller_num', '=', rd.teller_num)])
            


            for p in performancereportori_datas:
                zshzjs = 0.0
                zsyz = 0.0
                para = None
                if rd.role1 != u'专业化岗位':
                    para = self.env['hr.performanceparameter'].search(
                        [('role', '=', p.role)], limit=1)
                else:
                    para = self.env['hr.performanceparameter'].search(
                        [('role', '=', standard_trans+p.role)], limit=1)
                    if len(para) == 0:
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', p.role)], limit=1)

                if para.jjfs == 'byByte':
                    zshzjs = p.lrhzs * para.parameter_valuex + p.lrzjs
                    zsyz = zshzjs
                elif para.jjfs == 'byQuantity':
                    zshzjs = p.ywzl * para.parameter_valuex
                    zsyz = p.ywzl
                elif para.jjfs == 'byTime':
                    zshzjs = p.ywzl * para.parameter_valuex
                    zsyz = p.ywzl
                elif para.jjfs == 'byMulti':
                    zshzjs = p.lrzjs * para.parameter_valuex
                    zsyz = zshzjs



                if rd.role1 != u'专业化岗位' and p.role == u'影像定位':
                    p1 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', u'影像定位账户激活')], limit=1)
                    p2 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', u'影像定位其他')], limit=1)
                    zshzjs += p.yxdw_zhjh * p1.parameter_valuex
                    zshzjs += p.yxdw_qt * p2.parameter_valuex
                    zsyz = zshzjs
                elif rd.role1 == u'专业化岗位' and p.role == u'影像定位':
                    p1 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', standard_trans+u'影像定位账户激活')], limit=1)
                    p2 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', standard_trans+u'影像定位其他')], limit=1)
                    zshzjs += p.yxdw_zhjh * p1.parameter_valuex
                    zshzjs += p.yxdw_qt * p2.parameter_valuex
                    zsyz = zshzjs

                performancebonusdetail = self.env['hr.performancebonus'].create({  # 'performancebonus_id': self.id,
                    'teller_num': rd.teller_num,'zsyz': zsyz,
                    'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                    'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                    'ywlx': p.role, 'ywzhs': p.ywzhs, 'ywzl': p.ywzl,
                    'hzs': p.lrhzs, 'zjs': p.lrzjs, 'ccs': p.lrccs,
                    'tjyxmh': p.tjyxmh,  'dhl': 0.0, 'gwxs': gwxs.parameter_value,
                    'zshzjs': zshzjs, 'cwl': 0.0, 'zql': 0.0, 'source_from': source_list[0]
                })
            for p in performancebranchreportori_datas:
                zshzjs = 0.0
                zsyz = 0.0
                para = None
                if rd.role1 != u'专业化岗位':
                    para = self.env['hr.performanceparameter'].search(
                        [('role', '=', p.role)], limit=1)
                else:
                    para = self.env['hr.performanceparameter'].search(
                        [('role', '=', standard_trans+p.role)], limit=1)
                    if len(para) == 0:
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', p.role)], limit=1)
                if para.jjfs == 'byByte':
                    zshzjs = p.lrhzs * para.parameter_valuex + p.lrzjs
                    zsyz = zshzjs
                elif para.jjfs == 'byQuantity':
                    zshzjs = p.ywzl * para.parameter_valuex
                    zsyz = p.ywzl
                elif para.jjfs == 'byTime':
                    zshzjs = p.ywzl * para.parameter_valuex
                    zsyz = p.ywzl
                elif para.jjfs == 'byMulti':
                    zshzjs = p.lrzjs * para.parameter_valuex
                    zsyz = zshzjs

                if rd.role1 != u'专业化岗位' and p.role == u'影像定位':
                    p1 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', u'影像定位账户激活')], limit=1)
                    p2 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', u'影像定位其他')], limit=1)
                    zshzjs += p.yxdw_zhjh * p1.parameter_valuex
                    zshzjs += p.yxdw_qt * p2.parameter_valuex
                    zsyz = zshzjs
                elif rd.role1 == u'专业化岗位' and p.role == u'影像定位':
                    p1 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', standard_trans+u'影像定位账户激活')], limit=1)
                    p2 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', standard_trans+u'影像定位其他')], limit=1)
                    zshzjs += p.yxdw_zhjh * p1.parameter_valuex
                    zshzjs += p.yxdw_qt * p2.parameter_valuex
                    zsyz = zshzjs
                performancebonusdetail = self.env['hr.performancebonus'].create({  # 'performancebonus_id': self.id,
                    'teller_num': rd.teller_num,'zsyz': zsyz,
                    'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                    'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                    'ywlx': p.role, 'ywzhs': p.ywzhs, 'ywzl': p.ywzl,
                    'hzs': p.lrhzs, 'zjs': p.lrzjs, 'ccs': p.lrccs,
                    'tjyxmh': p.tjyxmh,  'dhl': 0.0, 'gwxs': gwxs.parameter_value,
                    'zshzjs': zshzjs, 'cwl': 0.0, 'zql': 0.0, 'source_from': source_list[1]
                })
            for p in performancemobilereportori_datas:
                if not u'虚拟柜员' in p.teller_name:
                    zshzjs = 0.0
                    zsyz = 0.0
                    prole = mobile_prefix + p.role
                    para = None
                    if rd.role1 != u'专业化岗位':
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', prole)], limit=1)
                    else:
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', standard_trans+prole)], limit=1)
                        if len(para) == 0:
                            para = self.env['hr.performanceparameter'].search(
                                [('role', '=', prole)], limit=1)
                    if para.jjfs == 'byByte':
                        zshzjs = p.lrhzs * para.parameter_valuex + p.lrzjs
                        zsyz = zshzjs
                    elif para.jjfs == 'byQuantity':
                        zshzjs = p.ywbs * para.parameter_valuex
                        zsyz = p.ywbs
                    elif para.jjfs == 'bySub':
                        zshzjs = p.zrwxzs * para.parameter_valuex
                        zsyz = p.zrwxzs
                    elif para.jjfs == 'byTime':
                        zshzjs = p.ywzhs * para.parameter_valuex
                        zsyz = p.ywzhs


                    performancebonusdetail = self.env['hr.performancebonus'].create({  # 'performancebonus_id': self.id,
                        'teller_num': rd.teller_num,'zsyz': zsyz,
                        'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                        'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                        'ywlx': prole, 'ywzhs': p.ywzhs, 'ywzl': p.ywbs,
                        'hzs': p.lrhzs, 'zjs': p.lrzjs, 'ccs': p.ccs,
                        'tjyxmh': p.tjyxmhs,  'dhl': 0.0, 'gwxs': gwxs.parameter_value,
                        'zshzjs': zshzjs, 'cwl': 0.0, 'zql': 0.0, 'source_from': source_list[2]
                    })

            for p in performancebranchmobilereportori_datas:
                if not u'虚拟柜员' in p.teller_name:
                    zshzjs = 0.0
                    zsyz = 0.0
                    prole = mobile_prefix + p.role
                    para = None
                    if rd.role1 != u'专业化岗位':
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', prole)], limit=1)
                    else:
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', standard_trans+prole)], limit=1)
                        if len(para) == 0:
                            para = self.env['hr.performanceparameter'].search(
                                [('role', '=', prole)], limit=1)
                    if para.jjfs == 'byByte':
                        zshzjs = p.lrhzs * para.parameter_valuex + p.lrzjs
                        zsyz = zshzjs
                    elif para.jjfs == 'byQuantity':
                        zshzjs = p.ywbs * para.parameter_valuex
                        zsyz = p.ywbs
                    elif para.jjfs == 'bySub':
                        zshzjs = p.zrwxzs * para.parameter_valuex
                        zsyz = p.zrwxzs
                    elif para.jjfs == 'byTime':
                        zshzjs = p.ywzhs * para.parameter_valuex
                        zsyz = p.ywzhs

                    performancebonusdetail = self.env['hr.performancebonus'].create({  # 'performancebonus_id': self.id,
                        'teller_num': rd.teller_num,'zsyz': zsyz,
                        'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                        'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                        'ywlx': prole, 'ywzhs': p.ywzhs, 'ywzl': p.ywbs,
                        'hzs': p.lrhzs, 'zjs': p.lrzjs, 'ccs': p.lrccs,
                        'tjyxmh': p.tjyxmhs,  'dhl': 0.0, 'gwxs': gwxs.parameter_value,
                        'zshzjs': zshzjs, 'cwl': 0.0, 'zql': 0.0, 'source_from': source_list[3]
                    })

            for p in performanceproallowance_datas:
                if not u'虚拟柜员' in p.teller_name:
                    zshzjs = 0.0
                    zsyz = 0.0
                    prole = p.ywlx
                    if rd.role1 != u'专业化岗位':
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', prole)], limit=1)
                    else:
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', standard_trans+prole)], limit=1)
                        if len(para) == 0:
                            para = self.env['hr.performanceparameter'].search(
                                [('role', '=', prole)], limit=1)
                    if para.jjfs == 'byByte':
                        zshzjs = p.ywzl * para.parameter_valuex
                        zsyz = zshzjs
                    elif para.jjfs == 'byQuantity':
                        zshzjs = p.ywzl * para.parameter_valuex
                        zsyz = p.ywzl
                    elif para.jjfs == 'bySub':
                        zshzjs = p.ywzl * para.parameter_valuex
                        zsyz = p.ywzl
                    elif para.jjfs == 'byTime':
                        zshzjs = p.ywzl * para.parameter_valuex
                        zsyz = p.ywzl
                    elif p.ywlx == u'加减业务时间小计':
                        zshzjs = p.ywzl * 60
                        zsyz = p.ywzl

                    performancebonusdetail = self.env['hr.performancebonus'].create({  # 'performancebonus_id': self.id,
                        'teller_num': rd.teller_num,'zsyz': zsyz,
                        'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                        'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                        'ywlx': prole, 'ywzhs': p.ywzl, 'ywzl': p.ywzl,
                        'hzs': 0.0, 'zjs': 0.0, 'ccs': 0.0,
                        'tjyxmh': 0.0,  'dhl': 0.0, 'gwxs': 0.0,
                        'zshzjs': zshzjs, 'cwl': 0.0, 'zql': 0.0, 'source_from': source_list[4]
                    })

            for p in performanceplusminus_datas:
                if not u'虚拟柜员' in p.teller_name:
                    zshzjs = 0.0
                    zsyz = 0.0
                    prole = basic_prefix + p.role
                    if rd.role1 != u'专业化岗位':
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', prole)], limit=1)
                    else:
                        para = self.env['hr.performanceparameter'].search(
                            [('role', '=', standard_trans+prole)], limit=1)
                        if len(para) == 0:
                            para = self.env['hr.performanceparameter'].search(
                                [('role', '=', prole)], limit=1)
                    if para.jjfs == 'byByte':
                        zshzjs = p.btywlxj * para.parameter_valuex
                        zsyz = p.btywlxj
                    elif para.jjfs == 'byQuantity':
                        zshzjs = p.btywlxj * para.parameter_valuex
                        zsyz = p.btywlxj
                    elif para.jjfs == 'bySub':
                        zshzjs = p.btywlxj * para.parameter_valuex
                        zsyz = p.btywlxj
                    elif para.jjfs == 'byTime':
                        zshzjs = p.btywlxj * para.parameter_valuex
                        zsyz = p.btywlxj
                    performancebonusdetail = self.env['hr.performancebonus'].create({  # 'performancebonus_id': self.id,
                        'teller_num': rd.teller_num,'zsyz': zsyz,
                        'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                        'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                        'ywlx': prole, 'ywzhs': p.btywlxj, 'ywzl': p.btywlxj,
                        'hzs': 0.0, 'zjs': 0.0, 'ccs': 0.0,
                        'tjyxmh': 0.0,  'dhl': 0.0, 'gwxs': 0.0,
                        'zshzjs': zshzjs, 'cwl': 0.0, 'zql': 0.0, 'source_from': source_list[5]
                    })

            
                xxx = [p.ratio for p in performanceproratio]
                if  len(xxx):
                    self.write({'ratio': max(xxx)})

        name_list = [p.teller_name for p in self.env['hr.performancebonus'].search([])]
        for rd in role_datas:
            if rd.role1 != u'专业化岗位':
                # get cwl zql dhl，only related by lr
                performancebonus_datas = self.env['hr.performancebonus'].search(
                    [('teller_name', '=', rd.name), ('ywlx', '=', u'录入')])
                tempccs = sum([i.ccs for i in performancebonus_datas])
                tempywzl = sum([i.ywzl for i in performancebonus_datas])
                temptjyxmh = sum([i.tjyxmh for i in performancebonus_datas])
                if tempywzl != 0:
                    cwl = tempccs/tempywzl
                    zql = 1.0 - cwl
                    dhl = temptjyxmh/tempywzl
                    for pd in performancebonus_datas:
                        pd.write({'zql': zql, 'cwl': cwl, 'dhl': dhl})

            if not rd.name in name_list:
                performancebonusdetail = self.env['hr.performancebonus'].create({
                    'teller_num': rd.teller_num,'zsyz': 0,
                    'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                    'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                    'cwl': 0.0, 'zql': 0.0, 'source_from': source_list[7]
                })


class HrPerformanceBonusDelete(models.TransientModel):
    _name = 'hr.performance.bonus.delete'
    _description = 'HR Performancebonus Delete'

    @api.multi
    def performancebonus_delete(self):
        self.env.cr.execute("Delete  From hr_performancebonus")
        self.env.cr.execute("Delete  From hr_performancebonustotal")


class HrPerformanceOriReportDelete(models.TransientModel):
    _name = 'hr.performance.orireport.delete'
    _description = 'HR Ori Report Delete'

    @api.multi
    def performanceorireport_delete(self):
        self.env.cr.execute("Delete  From hr_performancereportori")
        self.env.cr.execute("Delete  From hr_performancemobilereportori")
        self.env.cr.execute("Delete  From hr_performancebranchreportori")
        self.env.cr.execute("Delete  From hr_performancebranchmobilereportori")
        self.env.cr.execute("Delete  From hr_performanceroleori")
        self.env.cr.execute("Delete  From hr_performanceteleadditionreportori")
        self.env.cr.execute("Delete  From hr_performanceplusminus")
        self.env.cr.execute("Delete  From hr_performanceproallowance")
        self.env.cr.execute("Delete  From hr_performanceattendance")
        self.env.cr.execute("Delete  From hr_performancememberinfo")
        self.env.cr.execute("Delete  From hr_performancecapbasic")
        self.env.cr.execute("Delete  From hr_performancecappro")
        self.env.cr.execute("Delete  From hr_performanceremovemember")




class HrPerformanceProCalculationCompute(models.TransientModel):  # 生成
    _name = 'hr.performance.procalculation.compute'
    _description = 'HR PerformancePro Calculation Compute'

    def get_lurushenheparameter(self, quarters, quantity):
        if quantity < 0:
            return None
        performancelurushenheparameter_data = self.env[
            'hr.performancelurushenheparameter'].search([('quarters', '=', quarters)])
        t_quantity = eval(
            performancelurushenheparameter_data.quantity)
        t_unit_price = eval(performancelurushenheparameter_data.unit_price)
        t_price_add_minus = eval(
            performancelurushenheparameter_data.price_add_minus)
        index = len(t_quantity) - 1
        for i, v in enumerate(t_quantity):
            if quantity < v:
                index = i - 1
                break
        return t_unit_price[index], t_price_add_minus[index]


    # =AC69+AG69+AI69+AK69+AZ69+BA69+(BQ69+BV69+BX69+BY69+BZ69+CA69+BS69*计奖参数!$B$13/计奖参数!$B$9)*50
    # =BE78+BK78+BR78+BT78+CB78+CI78+CN78+CP78+CQ78+DB78+DG78+DJ78+DM78+DU78+EB78+ED78+EF78+EG78
    # 
    @api.multi
    def performanceprocalculation_compute(self):
        _logger = logging.getLogger(__name__)


        self.env.cr.execute(
            'delete from hr_performanceproallowance where ywzl = 0')

        role_datas = self.env['hr.performanceroleori'].search([])
        gwxs_role_list = (u'录入', u'行号选择', u'行号录入',u'英文信息录入')
        lurushenhe_role1_list = (u'A', u'B', u'E', u'F')
        source_list = (u'绩效报表', u'双中心绩效报表', u'信用卡报表',
                       u'双中心信用卡报表', u'专业化补时报表', u'基础补时报表')
        wailian_tuple = (u'电话联系', u'双中心绩效报表', u'信用卡报表',
                       u'双中心信用卡报表')
        khywl_byquantity_tuple = (u'录入', u'复核')
        khywl_bysalary_tuple = (u'审核', u'信用卡外联')


        performancelurushenheparameter_datas = self.env[
            'hr.performancelurushenheparameter'].search([])
        performancegoal_datas = self.env['hr.performancegoal'].search([])

        b13 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', u'运营业务资料复核')], limit=1)
        b19 = (self.env['hr.performancelurushenheparameter'].search([], limit=1)[0]).work_day
        
        
        

        for rd in role_datas:
            performancebonus_datas = self.env['hr.performancebonus'].search(
                [('teller_name', '=', rd.name)])
            
            # if not performancebonus_datas:
            #     continue
            # if not performancebonus_datas[0].ywlx:
            #     continue

            performanceprofixedbonus = self.env['hr.performanceprofixedbonus'].search(
                [('role', '=', rd.role)], limit=1)
            performanceproratio = self.env['hr.performanceproratio'].search(
                [('teller_num', '=', rd.teller_num)])
            performanceattendance_data = self.env['hr.performanceattendance'].search(
                [('teller_name', '=', rd.name)], limit=1)
            performanceproallowance_data= self.env['hr.performanceproallowance'].search(
                [('work_num', '=', rd.teller_num)], limit=1)

            cal_process = []
            leave_days = sum([performanceattendance_data.sj, performanceattendance_data.bj, 
                 performanceattendance_data.kg, 
                performanceattendance_data.cqj, performanceattendance_data.cj])
            attendance_basic = performanceattendance_data.attendance_basic        
            attendance_actual = attendance_basic - leave_days

            kj = 0.0
            

            zyhgwbzj_dz = performanceprofixedbonus.jj/b19*attendance_basic
            xxx = [p.ratio for p in performanceproratio]
            if len(xxx):
                ratio = max(xxx)
            kfts = leave_days if leave_days>2 else 0
            if attendance_basic>0:
                kj = -(zyhgwbzj_dz*ratio)/attendance_basic*(kfts+performanceproallowance_data.minus_date)


            # paramater
            other_datas = u""
            other_datas_dict = {}
            cwl = 0.00000
            zql = 0.00000
            dhl = 0.00000
            jjdj, sskcs = 0.0, 0.0
            sh_jjdj = 0.0
            sh_sskcs = 0.0

            jj = 0.0
            ranking = 0
            
            jblr_mul_ac = 0.0
            jblr_mul_gwxs_ae = 0.0
            jjzzj_bb = 0.0
            lrjj_be = 0.0
            lrzlj_bk = 0.0
            shywlxj_cy = 0.0
            shjj_db = 0.0
            zyhgwjbzywzshs_dy = 0.0
            
            ywlwclkhywl = 0.0
            # pro
            jbzywzshs = 0.0
            zyhywbzhs = 0.0
            bs = 0.0
            pro_zhs = 0.0

            teller_num = rd.teller_num
            teller_name = rd.name
            # identity = performancebonus_datas[0].identity
            quarters = rd.quarters
            # quarters_date = performancebonus_datas[0].quarters_date
            group = rd.work_group
            role = rd.role
            role1 = rd.role1
            all_roleinlurushenhe_set = set()
            if role1 != u'专业化岗位':
                except_list = []

                jblr_mul_gwxs_ae = sum([current_account.zshzjs * current_account.gwxs for current_account in performancebonus_datas
                                        if current_account.ywlx in gwxs_role_list])  # and u'绩效' in current_account.source_from])
                jblr_mul_ac = sum([current_account.zshzjs  for current_account in performancebonus_datas
                                        if current_account.ywlx in gwxs_role_list])
                jjzzj_bb += jblr_mul_gwxs_ae

                for plsp in performancelurushenheparameter_datas:
                    role_list = [i for i in plsp.role.split(',')]
                    all_roleinlurushenhe_set = all_roleinlurushenhe_set | set(
                        role_list)
                    except_list.extend(role_list)
                    role_set = set(role_list) - set(gwxs_role_list)
                    if plsp.quarters == u'录入岗':
                        for i in performancebonus_datas:
                            if i.ywlx in role_set:
                                jjzzj_bb += i.zshzjs
                            if i.ywlx in role_list:
                                cwl = i.cwl if i.cwl != 0.0 else cwl
                                zql = i.zql if i.zql != 0.0 else zql
                                dhl = i.dhl if i.dhl != 0.0 else dhl
                                jjdj, sskcs = self.get_lurushenheparameter(
                                    plsp.quarters, jjzzj_bb)
                                # jjdj = i.jjdj if i.jjdj != 0.0 else jjdj
                                # sskcs = i.sskcs if i.sskcs != 0.0 else sskcs
                    elif plsp.quarters == u'审核岗':
                        for i in performancebonus_datas:
                            if i.ywlx in role_list:
                                shywlxj_cy += i.zshzjs

                                # sh_jjdj = i.jjdj
                                # sh_sskcs = i.sskcs
                            sh_jjdj, sh_sskcs = self.get_lurushenheparameter(
                                plsp.quarters, shywlxj_cy)

                


                lrjj_be = jjzzj_bb * jjdj - sskcs

                for i in performancegoal_datas:
                    if i.role == role and i.role1 == role1:
                        zqlxs = (1 + (zql - i.zql_goal) * 100)
                        lhlxs = (1 + (i.fql_goal - dhl))
                        lrzlj_bk = zqlxs * lhlxs
                        cal_process.append(str(i.zql_goal)+","+str(i.fql_goal)+","+str(zql)+","+str(dhl)+","+str(zqlxs)
                                           + ","+str(lhlxs)+","+str(lrzlj_bk))
                        lrzlj_bk = (lrzlj_bk - 1) * lrjj_be

                shjj_db = shywlxj_cy * sh_jjdj - sh_sskcs

                for p in performancebonus_datas:
                    if p.ywlx:
                        if not p.ywlx in all_roleinlurushenhe_set:
                            if other_datas_dict.has_key(p.ywlx):
                                other_datas_dict[p.ywlx] += p.zshzjs
                            else:
                                other_datas_dict[p.ywlx] = p.zshzjs
                        if not p.ywlx in except_list:  # or not u'绩效' in p.source_from:
                            jj += p.zshzjs
                            zsyz = p.zsyz * 50 if role != u'运营业务资料复核' else p.zsyz * 50 * b13 / b19
                            ywlwclkhywl += zsyz

                # 业务量完成率考核业务量
                if role in khywl_byquantity_tuple:
                    ywlwclkhywl += jjzzj_bb - jblr_mul_gwxs_ae + jblr_mul_ac

                jj += lrjj_be + lrzlj_bk + shjj_db
            else:
                pro_para_list = [x.role for x in self.env[
                    'hr.performanceparameter'].search([('quarters', '=', u'专业化岗位')])]
                for p in performancebonus_datas:
                    # _logger.info(p.ywlx)
                    # _logger.info(p.teller_name)
                    if  p.ywlx:
                        if other_datas_dict.has_key(p.ywlx):
                            other_datas_dict[p.ywlx] += p.zshzjs
                        else:
                            other_datas_dict[p.ywlx] = p.zshzjs
                        if p.ywlx in pro_para_list:
                            zyhywbzhs += p.zshzjs
                        elif not p.ywlx in pro_para_list and not u'补时' in p.ywlx and not u'加减业务时间小计' in p.ywlx:
                            jbzywzshs += p.zshzjs

                pro_zhs = sum([i.zshzjs for i in performancebonus_datas])
                jj = zyhgwbzj_dz*ratio

            # 组长
            # cap_basic_data = self.env['hr.performancecapbasic'].search(
            #     [('teller_name', '=', rd.name)])
            # cap_pro_data = self.env['hr.performancecappro'].search(
            #     [('teller_name', '=', rd.name)])
            # cap_bonus = 0.0
            # temp_cap_bzjxj_list = [0 , 0] 
            # standard_bonus = 0.0 
            # if len(cap_basic_data) > 0:
            #     for r in cap_basic_data.role.split('/'):
            #         performancecapbasic_caps = self.env['hr.performancecapbasic'].search(
            #     [('role', '=', r)])
            #         l = [x.jj for x in performancecapbasic_caps if not x.work_num in remove_member_set]
            #         _logger.info(rd.name)
            #         _logger.info(l)
            #         temp_cap_bzjxj_list[0]+=sum(l)
            #         temp_cap_bzjxj_list[1]+=len(l)
            #     if  temp_cap_bzjxj_list[1] != 0:
            #         standard_bonus = temp_cap_bzjxj_list[0]/temp_cap_bzjxj_list[1]

            #     if cap_basic_data.cap_bonus > 0.0:
            #         cap_bonus = cap_basic_data.cap_bonus
            #     elif cap_basic_data.actual_bonus == 0.0 or cap_basic_data.cap_bonus == 0.0:
            #         cap_bonus = (cap_basic_data.total_bonus -
            #                      jj) if cap_basic_data.total_bonus > 0.0 else 0.0
            #     cap_basic_data.write(
            #             {'actual_bonus': jj, 'cap_bonus': cap_bonus,'standard_bonus':standard_bonus})
            #     other_datas_dict[u"组长考核奖"] = cap_bonus
            # elif len(cap_pro_data) > 0:
            #     for r in cap_pro_data.role.split('/'):
            #         performancecappro_caps = self.env['hr.performancecappro'].search(
            #     [('role', '=', r)])
            #         l = [x.jj for x in performancecappro_caps if not x.work_num in remove_member_set]
            #         temp_cap_bzjxj_list[0]+=sum(l)
            #         temp_cap_bzjxj_list[1]+=len(l)
            #     if  temp_cap_bzjxj_list[1] != 0:
            #         standard_bonus = temp_cap_bzjxj_list[0]/temp_cap_bzjxj_list[1]

            #     if cap_pro_data.cap_bonus > 0.0:
            #         cap_bonus = cap_pro_data.cap_bonus
            #     elif cap_pro_data.actual_bonus == 0.0 or cap_pro_data.cap_bonus == 0.0:
            #         cap_bonus = (cap_pro_data.total_bonus -
            #                      jj) if cap_pro_data.total_bonus > 0.0 else 0.0
            #     cap_pro_data.write(
            #             {'actual_bonus': jj, 'cap_bonus': cap_bonus,'standard_bonus':standard_bonus})
            #     other_datas_dict[u"组长考核奖"] = cap_bonus
            # jj += cap_bonus

            # other_datas_list = [k + ":  " + str(v) for k, v in other_datas_dict.items()]
            # other_datas = "\n".join(other_datas_list) # p.ywlx + u": " +
            # str(p.zshzjs) + "\n"

            if zyhywbzhs or jbzywzshs:
                if other_datas_dict.has_key(u"加减业务时间小计"):
                    bs = other_datas_dict[u"加减业务时间小计"]
                    del(other_datas_dict[u"加减业务时间小计"])
                other_datas_list = [
                    k + ":  " + str(v) for k, v in other_datas_dict.items()]
                other_datas = "\n".join(other_datas_list)
                other_datas += "\n" + u"---------------------------------"  + "\n" + u"补时:  " + str(bs) + "\n" + \
                    u"当月专业化业务总标准耗时:  " + \
                    str(zyhywbzhs) + "\n" + \
                    u"兼标准业务折算耗时:  " + str(jbzywzshs) + "\n"
            else:
                other_datas_list = [
                    k + ":  " + str(v) for k, v in other_datas_dict.items()]
                other_datas = "\n".join(other_datas_list)
            jj += kj


            if jj == 0.0 and len(self.env['hr.performanceremovemember'].search([('teller_num','=', rd.teller_num)]))<1:
                self.env['hr.performanceremovemember'].create({
                        'teller_num': rd.teller_num,'teller_name': rd.name,'role': rd.role
                    })

            performancebonustotal = self.env['hr.performancebonustotal'].create({'cal_process': ' '.join(cal_process), 'teller_num': teller_num,
                                                                                 'teller_name': teller_name, 'identity': u'派遣', 'quarters': rd.quarters,
                                                                                 'group': rd.work_group, 'role': rd.role,
                                                                                 'role1': rd.role1, 'jblr_mul_gwxs_ae': jblr_mul_gwxs_ae,
                                                                                 'jjzzj_bb': jjzzj_bb, 'lrjj_be': lrjj_be,
                                                                                 'lrzlj_bk': lrzlj_bk, 'shywlxj_cy': shywlxj_cy,
                                                                                 'shjj_db': shjj_db, 'zyhgwjbzywzshs_dy': zyhgwjbzywzshs_dy,
                                                                                 'kj': kj, 'bs': bs, 'zyhywbzhs': zyhywbzhs,
                                                                                 'jbzywzshs': jbzywzshs, 'jj': jj, 'ranking': ranking,'pro_zhs':pro_zhs,
                                                                                 'lrjjdj_bc': jjdj, 'sskc_bd': sskcs,'zyhgwbzj_dz':zyhgwbzj_dz,
                                                                                 'shjjdj_cz': sh_jjdj, 'shsskc_da': sh_sskcs,
                                                                                 'other_datas': other_datas,'attendance_basic': attendance_basic,
                                                                                 'attendance_actual':attendance_actual,'ywlwclkhywl':ywlwclkhywl,
                                                                                 })




            for p in performancebonus_datas:
                p.write({'performancebonustotal_id': performancebonustotal.id})
        # for end
        
        #rank pro
        datas = self.env['hr.performancebonustotal'].search(
            [('role1', '=', u'专业化岗位')])
        datas = datas.sorted(key=attrgetter('role', 'jj'), reverse=True)
        lastrole = ''
        rank = 0
        lastjj = 0.0
        samecount = 0
        for d in datas:
            if lastrole == '' or d.role == lastrole:
                if lastjj == d.pro_zhs:
                    samecount += 1
                else:
                    rank = rank + 1 if samecount == 0 else rank+samecount
                    samecount = 0
                lastrole = d.role
                lastjj = d.pro_zhs
            else:
                rank = 1
                # rank += 1
                lastrole = d.role
            d.write({'ranking': rank})


        all_datas = self.env['hr.performancebonustotal'].search([])
        role_ywlwclkhywl_dict = {}
 
        
        for m,n in itertools.groupby(all_datas,key = itemgetter('role')):
            x = list(n)
            # _logger.info(m)
            if len(x):
                role_ywlwclkhywl_dict[m] = sum([x.ywlwclkhywl for x in list(n)])/len(x)
                # _logger.info(role_ywlwclkhywl_dict[m])
                
        for d in all_datas:
            _logger.info(d.role)
            avg_num = role_ywlwclkhywl_dict[d.role] if role_ywlwclkhywl_dict.has_key(d.role) else 0
            _logger.info(str(avg_num))
            if avg_num:
                d.write({'complete_rate': d.ywlwclkhywl/avg_num,'other_datas':d.other_datas + "\n\n" + str(avg_num)})
    # def complete_rate(self, role, performancebonus_datas):
    #     ywlwclkhywl = 0.0
    #     if role == u'录入':
    #         para = self.env['hr.performanceparameter'].search([])

    #         for r in role_without_pro_set:
    #             role_averge_dict[r] = avg([for])

    #     return ywlwclkhywl

class HrPerformanceBonusCheck(models.TransientModel):
    _name = 'hr.performance.bonus.check'
    _description = 'HR Performancebonus Check'

    @api.multi
    def performancebonus_check(self):
        # add role, group to performanceroleori
        performancemonth = self.env['hr.performancemonth'].search([], limit=1)
        performancememberinfo_datas = self.env['hr.performancememberinfo'].search([])
        performanceroleori_datas = self.env['hr.performanceroleori'].search([])
        m = performancemonth.report_date
        performancememberinfo_filter_datas1 = self.env['hr.performancememberinfo'].search(
            [('incumbency','=',u'离职'),('leave_date','>=',m),('teller_type','!=',u'1-正式员工'),('role','!=',u'管理')])
        performancememberinfo_filter_datas2 = self.env['hr.performancememberinfo'].search(
            [('quarters_date','>',m),('teller_type','!=',u'1-正式员工'),('role','!=',u'管理')])
        performancememberinfo_filter_datas3 = self.env['hr.performancememberinfo'].search(
            [('incumbency','=',u'在职'),('teller_type','!=',u'1-正式员工'),('role','!=',u'管理')])


        role_set = (u'培训（复核）', u'培训（审核）')
        pro_role_set = (u'专职讲师',u'授权')
        teller_list = [x.teller_num for x in performanceroleori_datas]
        for p in performancememberinfo_filter_datas1:
            if not p.member_num in teller_list:
                role1 = u'专业化岗位' if not p.role in role_set else u''
                self.env['hr.performanceroleori'].create({
                        'work_num': p.work_num,'teller_num': p.member_num,'name': p.teller_name,'work_center': u'上海' if u'上海' in p.orgnization3 else u'合肥',
                        'work_group': p.group,'quarters': p.quarters,'role': p.role,'role1': role1})

        for p in performancememberinfo_filter_datas3:
            if not p.member_num in teller_list and len(self.env['hr.performanceroleori'].search([('teller_num','=', p.member_num)]))<1:
                role1 = u'专业化岗位' if not p.role in role_set else u''
                self.env['hr.performanceroleori'].create({
                        'work_num': p.work_num,'teller_num': p.member_num,'name': p.teller_name,'work_center': u'上海' if u'上海' in p.orgnization3 else u'合肥',
                        'work_group': p.group,'quarters': p.quarters,'role': p.role,'role1': role1})

        for d in performanceroleori_datas:
            for out in performancememberinfo_datas:
                if d.teller_num == out.member_num:
                    d.write({'work_group': out.group,'role': out.role})
                    if d.role in pro_role_set:
                        d.write({'role1': u'专业化岗位'})

        # replace () to （）, insert captain into performanceremovemember
        performanceplusminus_datas = self.env['hr.performanceplusminus'].search([])
        performanceproallowance_datas = self.env['hr.performanceproallowance'].search([])
        
        for p in performanceplusminus_datas:
            if '(' in p.role or ')' in p.role:
                result = p.role.replace('(', '（').replace(')', '）')
                p.write({'role':result})

        for p in performanceproallowance_datas:
            if '(' in p.ywlx or ')' in p.ywlx:
                result = p.ywlx.replace('(', '（').replace(')', '）')
                p.write({'ywlx':result})

        # insert absent>=8, dimission, captain, quarters_date>this month 1st into performanceremovemember
        performancecapbasic_datas = self.env['hr.performancecapbasic'].search([])
        performancecappro_datas = self.env['hr.performancecappro'].search([])
        performanceattendance_datas = self.env['hr.performanceattendance'].search([])

        for p in performancecapbasic_datas:
            self.env['hr.performanceremovemember'].create({
                        'teller_num': p.work_num,'teller_name': p.teller_name,'role': p.role
                    })

        for p in performancecappro_datas:
            self.env['hr.performanceremovemember'].create({
                        'teller_num': p.work_num,'teller_name': p.teller_name,'role': p.role
                    })

        global NOTINCLUDEDAYS
        for performanceattendance_data in performanceattendance_datas:
            leave_days = sum([performanceattendance_data.sj, performanceattendance_data.bj, 
                    performanceattendance_data.kg, 
                    performanceattendance_data.cqj, performanceattendance_data.cj])
            if leave_days >= NOTINCLUDEDAYS:
                self.env['hr.performanceremovemember'].create({
                    'teller_num': performanceattendance_data.sap_num,'teller_name': performanceattendance_data.teller_name,'role': performanceattendance_data.role})
        
        for p in performancememberinfo_filter_datas1:
            self.env['hr.performanceremovemember'].create({
                    'teller_num': p.member_num,'teller_name': p.teller_name,'quarters_date': p.quarters_date,'role': p.role})
        for p in performancememberinfo_filter_datas2:
            if len(self.env['hr.performanceremovemember'].search([('teller_num','=', p.member_num)]))<1:
                self.env['hr.performanceremovemember'].create({
                        'teller_num': p.member_num,'teller_name': p.teller_name,'quarters_date': p.quarters_date,'role': p.role})


class HrPerformanceCapCalculate(models.TransientModel):
    _name = 'hr.performance.cap.calculate'
    _description = 'HR Performancebonus cap calculate'

    @api.multi
    def performancecapcalculate_check(self):
        performanceremovemember_datas = self.env['hr.performanceremovemember'].search([])
        remove_member_set = set([x.teller_num for x in performanceremovemember_datas])
        role_datas = self.env['hr.performanceroleori'].search([])
        # performancebonustotal_datas = self.env['hr.performancebonustotal'].search([])
        for rd in role_datas:
         # 组长
            performancebonustotal = self.env['hr.performancebonustotal'].search(
                [('teller_num', '=', rd.teller_num)],limit=1)
            cap_basic_data = self.env['hr.performancecapbasic'].search(
                [('teller_name', '=', rd.name)],limit=1)
            cap_pro_data = self.env['hr.performancecappro'].search(
                [('teller_name', '=', rd.name)],limit=1)
            jj = performancebonustotal.jj
            cap_bonus = 0.0
            temp_cap_bzjxj_list = [0 , 0] 
            standard_bonus = 0.0 
            if len(cap_basic_data) > 0:
                for r in cap_basic_data.role.split('/'):
                    performancebonustotal_datas = self.env['hr.performancebonustotal'].search(
                [('role', '=', r)])
                    l = [x.jj for x in performancebonustotal_datas if not x.teller_num in remove_member_set]
                    temp_cap_bzjxj_list[0]+=sum(l)
                    temp_cap_bzjxj_list[1]+=len(l)
                if  temp_cap_bzjxj_list[1] != 0:
                    standard_bonus = temp_cap_bzjxj_list[0]/temp_cap_bzjxj_list[1]

                if cap_basic_data.cap_bonus > 0.0:
                    cap_bonus = cap_basic_data.cap_bonus
                elif cap_basic_data.actual_bonus == 0.0 or cap_basic_data.cap_bonus == 0.0:
                    cap_bonus = (cap_basic_data.total_bonus -
                                 jj) if cap_basic_data.total_bonus > 0.0 else 0.0
                cap_basic_data.write(
                        {'actual_bonus': jj, 'cap_bonus': cap_bonus,'standard_bonus':standard_bonus})
                # other_datas_dict[u"组长考核奖"] = cap_bonus
            elif len(cap_pro_data) > 0:
                # for r in cap_pro_data.role.split('/'):
                #     performancebonustotal_datas = self.env['hr.performancebonustotal'].search(
                # [('role', '=', r)])
                #     l = [x.jj for x in performancebonustotal_datas if not x.teller_num in remove_member_set]
                #     temp_cap_bzjxj_list[0]+=sum(l)
                #     temp_cap_bzjxj_list[1]+=len(l)
                # if  temp_cap_bzjxj_list[1] != 0:
                #     standard_bonus = temp_cap_bzjxj_list[0]/temp_cap_bzjxj_list[1]
                performanceprofixedbonus = self.env['hr.performanceprofixedbonus'].search(
                [('role', '=', rd.role)], limit=1)


                if cap_pro_data.cap_bonus > 0.0:
                    cap_bonus = cap_pro_data.cap_bonus
                elif cap_pro_data.actual_bonus == 0.0 or cap_pro_data.cap_bonus == 0.0:
                    cap_bonus = (cap_pro_data.total_bonus -
                                 jj) if cap_pro_data.total_bonus > 0.0 else 0.0
                cap_pro_data.write(
                        {'actual_bonus': jj, 'cap_bonus': cap_bonus,'standard_bonus':performanceprofixedbonus.jj})
                # other_datas_dict[u"组长考核奖"] = cap_bonus