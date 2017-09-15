# -*- coding: utf-8 -*-
from __future__ import division
import sys
from openerp import api, models
import threading
import logging
import itertools
from operator import itemgetter, attrgetter
import math

reload(sys)
sys.setdefaultencoding('utf-8')
NOTINCLUDEDAYS = 8

class HrPerformanceBonusCompute(models.TransientModel):
    _name = 'hr.performance.bonus.compute'
    _description = 'HR Performancebonus Compute'

    @api.multi
    def performancebonus_compute(self):

        self.env.cr.execute("Delete  From hr_performancebonus")
        self.env.cr.execute("Delete  From hr_performancebonustotal")

        standard_trans = u'标准化业务-'
        mobile_prefix = u'信用卡'
        basic_prefix = u'基础补时'
        pro_prefix = u'专业化补时'

        performancegwxs = self.env['hr.performancegwxs'].search([], limit=1)
        gwxs_role_list = eval(
            performancegwxs.GWXS_YW)#(u'录入', u'行号选择', u'行号录入',u'英文信息录入')

        
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
                    if p.ywzl > 0 or p.minus_date>0:
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
        t_quantity = eval(performancelurushenheparameter_data.quantity)
        t_unit_price = eval(performancelurushenheparameter_data.unit_price)
        t_price_add_minus = eval(performancelurushenheparameter_data.price_add_minus)
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

        cap_list = [x.work_num for x in self.env['hr.performancecapbasic'].search([])]
        cap_list.extend([x.work_num for x in self.env['hr.performancecappro'].search([])])
        role_datas = self.env['hr.performanceroleori'].search([])
        # gwxs_role_list = (u'录入', u'行号选择', u'行号录入',u'英文信息录入')

        performancegwxs = self.env['hr.performancegwxs'].search([], limit=1)
        gwxs_role_list = eval(performancegwxs.GWXS_YW)#(u'录入', u'行号选择', u'行号录入',u'英文信息录入')

        lurushenhe_role1_list = (u'A', u'B', u'E', u'F')
        source_list = (u'绩效报表', u'双中心绩效报表', u'信用卡报表',
                       u'双中心信用卡报表', u'专业化补时报表', u'基础补时报表')
        wailian_tuple = (u'电话联系', u'双中心绩效报表', u'信用卡报表',
                       u'双中心信用卡报表')
        khywl_byquantity_tuple = (u'录入', u'复核')
        khywl_bysalary_tuple = (u'审核', u'信用卡外联')

        notremoverole_set = set([x.role for x in self.env['hr.performancenotremoverole'].search([])])
        performancelurushenheparameter_datas = self.env[
            'hr.performancelurushenheparameter'].search([])
        performancegoal_datas = self.env['hr.performancegoal'].search([])

        b13 = self.env['hr.performanceparameter'].search(
                        [('parameter_name', '=', u'运营业务资料复核')], limit=1)
        b19 = (self.env['hr.performancelurushenheparameter'].search([], limit=1)[0]).work_day
        

        for rd in role_datas:
            performancebonus_datas = self.env['hr.performancebonus'].search(
                [('teller_name', '=', rd.name)])
            performancememberinfo = self.env['hr.performancememberinfo'].search(
                [('member_num', '=', rd.teller_num)], limit=1)
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
            ratio = 0.0

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
            quarters_date = performancememberinfo.quarters_date
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
                    elif plsp.quarters == u'审核岗':
                        for i in performancebonus_datas:
                            if i.ywlx in role_list:
                                shywlxj_cy += i.zshzjs
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

                #pro_zhs = sum([i.zshzjs for i in performancebonus_datas])
                jj = zyhgwbzj_dz*ratio

            if other_datas_dict.has_key(u"加减业务时间小计"):
                bs += other_datas_dict[u"加减业务时间小计"]
                del other_datas_dict[u"加减业务时间小计"]

            if zyhywbzhs or jbzywzshs or bs:
                other_datas_list = [
                    k + ":  " + str(v) for k, v in other_datas_dict.items()]
                other_datas = "\n".join(other_datas_list)
                other_datas += "\n" + u"---------------------------------"  + "\n" + u"补时:  " + str(bs) + "\n" + \
                    u"当月专业化业务总标准耗时:  " + \
                    str(zyhywbzhs) + "\n" + \
                    u"兼准业务折算耗时:  " + str(jbzywzshs) + "\n"
            else:
                other_datas_list = [
                    k + ":  " + str(v) for k, v in other_datas_dict.items()]
                other_datas = "\n".join(other_datas_list)
            jj += kj
            pro_zhs = zyhywbzhs + jbzywzshs + bs
            # 业务量完成率考核业务量
            if role in khywl_bysalary_tuple:
                ywlwclkhywl = jj
            if role1 == u'专业化岗位':
                ywlwclkhywl = pro_zhs

            
            if not rd.role in notremoverole_set and jj == 0.0 and pro_zhs == 0.0 and len(self.env['hr.performanceremovemember'].search([('teller_num','=', rd.teller_num)]))<1:
                self.env['hr.performanceremovemember'].create({
                        'teller_num': rd.teller_num,'teller_name': rd.name,'role': rd.role
                    })

            performancebonustotal = self.env['hr.performancebonustotal'].create({'cal_process': ' '.join(cal_process), 'teller_num': teller_num,
                                                                                 'teller_name': teller_name, 'identity': u'派遣', 'quarters': rd.quarters,
                                                                                 'group': rd.work_group, 'role': rd.role,'quarters_date':quarters_date,
                                                                                 'role1': rd.role1, 'jblr_mul_gwxs_ae': jblr_mul_gwxs_ae,
                                                                                 'jjzzj_bb': jjzzj_bb, 'lrjj_be': lrjj_be,
                                                                                 'lrzlj_bk': lrzlj_bk, 'shywlxj_cy': shywlxj_cy,
                                                                                 'shjj_db': shjj_db, 'zyhgwjbzywzshs_dy': zyhgwjbzywzshs_dy,
                                                                                 'kj': kj, 'bs': bs, 'zyhywbzhs': zyhywbzhs,'jj_without_cap':round(jj,2),
                                                                                 'jbzywzshs': jbzywzshs, 'jj': round(jj,2), 'ranking': ranking,'pro_zhs':pro_zhs,
                                                                                 'lrjjdj_bc': jjdj, 'sskc_bd': sskcs,'zyhgwbzj_dz':zyhgwbzj_dz,
                                                                                 'shjjdj_cz': sh_jjdj, 'shsskc_da': sh_sskcs,'ratio':ratio,
                                                                                 'other_datas': other_datas,'attendance_basic': attendance_basic,
                                                                                 'attendance_actual':attendance_actual,'ywlwclkhywl':ywlwclkhywl,
                                                                                 })


            for p in performancebonus_datas:
                p.write({'performancebonustotal_id': performancebonustotal.id})
        # for end
        
        # rank pro
        self.set_pro_rank(True)
        self.set_pro_rank(False)
        # complete rate
        self.set_complete_rate()
        # jk
        self.set_jk()

    def set_pro_rank(self,in_or_not):
        datas = self.env['hr.performancebonustotal'].search([('role1', '=', u'专业化岗位'),('group', 'like', u'H')]) if in_or_not else self.env['hr.performancebonustotal'].search([('role1', '=', u'专业化岗位'),('group', 'not like', u'H')])
        datas = datas.sorted(key=attrgetter('role','pro_zhs'), reverse=True)
        lastrole = ''
        rank = 0
        lastjj = 0.0
        samecount = 0
        for d in datas:
            if d.group: # and not d.teller_num in remove_member_set:
                if lastrole == '' or d.role == lastrole:
                    if lastjj == d.pro_zhs:
                        samecount += 1
                    else:
                        rank = rank + 1 if samecount == 0 else rank + samecount
                        samecount = 0
                    lastrole = d.role
                    lastjj = d.pro_zhs
                else:
                    rank = 1
                    lastrole = d.role
                    samecount = 0
                d.write({'ranking': rank})


    def set_complete_rate(self):
        # complete rate
        all_datas = self.env['hr.performancebonustotal'].search([])
        role_ywlwclkhywl_dict = {}
        role_set = set([x.role for x in all_datas])
        for rd in role_set:
            group_datas = all_datas.filtered(lambda r: r.role == rd)
            if len(group_datas)>0:
                role_ywlwclkhywl_dict[rd] = sum([y.ywlwclkhywl for y in group_datas])/len(group_datas)
        for d in all_datas:
            avg_num = role_ywlwclkhywl_dict[d.role] if role_ywlwclkhywl_dict.has_key(d.role) else 0
            if avg_num:
                d.write({'complete_rate': d.ywlwclkhywl/avg_num,'other_datas':d.other_datas + "\n\n"  +  u'角色平均考核业务量:'+ str(avg_num)})


    def set_jk(self):
        all_datas = self.env['hr.performancebonustotal'].search([])
        jk_datas = self.env['hr.performanceproratio'].search([])
        for rd in all_datas:
            data = jk_datas.filtered(lambda r: r.teller_num == rd.teller_num)
            if len(data)>0:
                jk = sum([x.total_jk for x in data])
                rd.write({'jk': jk,'jkhjj': jk + rd.jj,})


class HrPerformanceTest(models.TransientModel):
    _name = 'hr.performance.test'
    _description = 'HR Performance Test'

    @api.multi
    def performancebonus_set_complete_rate(self):
        _logger = logging.getLogger(__name__)
        # complete rate
        all_datas = self.env['hr.performancebonustotal'].search([])
        role_ywlwclkhywl_dict = {}
        role_set = set([x.role for x in all_datas])
        for rd in role_set:
            group_datas = all_datas.filtered(lambda r: r.role == rd)
            if len(group_datas)>0:
                role_ywlwclkhywl_dict[rd] = sum([y.ywlwclkhywl for y in group_datas])/len(group_datas)
        _logger.info(role_ywlwclkhywl_dict)
        for d in all_datas:
            avg_num = role_ywlwclkhywl_dict[d.role] if role_ywlwclkhywl_dict.has_key(d.role) else 0
            if avg_num:
                d.write({'complete_rate': d.ywlwclkhywl/avg_num,'other_datas':d.other_datas + "\n\n"  +  u'角色平均考核业务量:'+ str(avg_num)})


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

        
        all_mem_list = [r.member_num for r in performancememberinfo_filter_datas1]
        all_mem_list.extend([r.member_num for r in performancememberinfo_filter_datas3]) 
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
                    d.write({'work_group': out.group,'role': out.role,'quarters':out.quarters})
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
            if len(self.env['hr.performanceremovemember'].search([('teller_num','=', p.work_num)]))<1:
                self.env['hr.performanceremovemember'].create({
                            'teller_num': p.work_num,'teller_name': p.teller_name,'role': p.role
                        })

        for p in performancecappro_datas:
            if len(self.env['hr.performanceremovemember'].search([('teller_num','=', p.work_num)]))<1:
                self.env['hr.performanceremovemember'].create({
                            'teller_num': p.work_num,'teller_name': p.teller_name,'role': p.role
                        })

        global NOTINCLUDEDAYS
        for performanceattendance_data in performanceattendance_datas:
            leave_days = sum([performanceattendance_data.sj, performanceattendance_data.bj, 
                    performanceattendance_data.kg, 
                    performanceattendance_data.cqj, performanceattendance_data.cj])
            if leave_days >= NOTINCLUDEDAYS and len(self.env['hr.performanceremovemember'].search([('teller_num','=', performanceattendance_data.sap_num)]))<1:
                self.env['hr.performanceremovemember'].create({
                    'teller_num': performanceattendance_data.sap_num,'teller_name': performanceattendance_data.teller_name,'role': performanceattendance_data.role})
        
        for p in performancememberinfo_filter_datas1:
            if len(self.env['hr.performanceremovemember'].search([('teller_num','=', p.member_num)]))<1:
                self.env['hr.performanceremovemember'].create({
                        'teller_num': p.member_num,'teller_name': p.teller_name,'quarters_date': p.quarters_date,'role': p.role})
        for p in performancememberinfo_filter_datas2:
            if len(self.env['hr.performanceremovemember'].search([('teller_num','=', p.member_num)]))<1:
                self.env['hr.performanceremovemember'].create({
                        'teller_num': p.member_num,'teller_name': p.teller_name,'quarters_date': p.quarters_date,'role': p.role})
        for delr in self.env['hr.performanceroleori'].search([]):
            if not delr.teller_num in all_mem_list:
                delr.unlink()

class HrPerformanceCapCalculate(models.TransientModel):
    _name = 'hr.performance.cap.calculate'
    _description = 'HR Performancebonus cap calculate'

    @api.multi
    def performancecapcalculate_check(self):
        _logger = logging.getLogger(__name__)
        performanceremovemember_datas = self.env['hr.performanceremovemember'].search([])
        remove_member_set = set([x.teller_num for x in performanceremovemember_datas])
        cap_pro_datas = self.env['hr.performancecappro'].search([])
        cap_basic_datas = self.env['hr.performancecapbasic'].search([])
        performancemonth = self.env['hr.performancemonth'].search([], limit=1)
        m = performancemonth.report_date
        b19 = (self.env['hr.performancelurushenheparameter'].search([], limit=1)[0]).work_day
        for rd in cap_basic_datas:
            performancebonustotal = self.env['hr.performancebonustotal'].search(
                [('teller_num', '=', rd.work_num)],limit=1)
           
            jj = performancebonustotal.jj
            bonus = 0.0
            total_bonus = 0.0
            cap_bonus = 0.0
            temp_cap_bzjxj_list = [0 , 0] 
            standard_bonus = 0.0 
            
            for r in rd.role.split('/'):
                performancebonustotal_datas = self.env['hr.performancebonustotal'].search([('role', '=', r)])
                l = [x.jj for x in performancebonustotal_datas if not x.teller_num in remove_member_set]
                y = [x.teller_num for x in performancebonustotal_datas if not x.teller_num in remove_member_set]
                temp_cap_bzjxj_list[0]+=sum(l)
                temp_cap_bzjxj_list[1]+=len(l)

            if  temp_cap_bzjxj_list[1] != 0:
                standard_bonus = temp_cap_bzjxj_list[0]/temp_cap_bzjxj_list[1]

            bonus = (standard_bonus + rd.fix_bonus)*rd.jj_rate
            total_bonus = bonus+rd.addition_bonus
            cap_bonus = total_bonus- jj

            performanceattendance_data = self.env['hr.performanceattendance'].search([('leave_date','>=',m),('sap_num','=',rd.work_num)], limit=1)
            if len(performanceattendance_data)>0:
                leave_days = sum([performanceattendance_data.sj, performanceattendance_data.bj, 
                performanceattendance_data.kg, performanceattendance_data.cqj, performanceattendance_data.cj])
                attendance_basic = performanceattendance_data.attendance_basic        
                kfts = leave_days if leave_days>2 else 0
                attendance_actual = attendance_basic - kfts
                ratio = attendance_actual*1.00/(b19*1.00)
                standard_bonus = standard_bonus * ratio
                bonus = bonus * ratio
                total_bonus = total_bonus * ratio
                jj = jj * ratio
                cap_bonus = cap_bonus * ratio


            rd.write({'standard_bonus':standard_bonus,'bonus':bonus,
                'total_bonus':total_bonus,'actual_bonus': jj, 'cap_bonus': cap_bonus,})
            totaldata = self.env['hr.performancebonustotal'].search([('teller_num', '=', rd.work_num)], limit=1)
            totaldata.write({'jj':total_bonus})

            # other_datas_dict[u"组长考核奖"] = cap_bonus
        for rd in cap_pro_datas:
            performanceprofixedbonus = self.env['hr.performanceprofixedbonus'].search(
            [('role', '=', rd.role)], limit=1)
            
            jj = performanceprofixedbonus.jj
            bonus = 0.0
            total_bonus = 0.0
            cap_bonus = 0.0
            standard_bonus = performanceprofixedbonus.jj

            bonus = (standard_bonus + rd.fix_bonus)*rd.jj_rate
            total_bonus = bonus+rd.addition_bonus
            cap_bonus = total_bonus- jj

            performanceattendance_data = self.env['hr.performanceattendance'].search([('leave_date','>=',m),('sap_num','=',rd.work_num)], limit=1)
            if len(performanceattendance_data)>0:
                leave_days = sum([performanceattendance_data.sj, performanceattendance_data.bj, 
                performanceattendance_data.kg, performanceattendance_data.cqj, performanceattendance_data.cj])
                attendance_basic = performanceattendance_data.attendance_basic        
                kfts = leave_days if leave_days>2 else 0
                attendance_actual = attendance_basic - kfts
                ratio = attendance_actual*1.00/(b19*1.00)
                standard_bonus = standard_bonus * ratio
                bonus = bonus * ratio
                total_bonus = total_bonus * ratio
                jj = jj * ratio
                cap_bonus = cap_bonus * ratio


            rd.write({'standard_bonus':standard_bonus,'bonus':bonus,
                'total_bonus':total_bonus,'actual_bonus': jj, 'cap_bonus': cap_bonus,})
            totaldata = self.env['hr.performancebonustotal'].search([('teller_num', '=', rd.work_num)], limit=1)
            totaldata.write({'jj':total_bonus})



        
        



class HrPerformanceAvgQuartersCalculate(models.TransientModel):
    _name = 'hr.performanceavgquarters.calculate'
    _description = 'HR Performance Avg Quarters Calculate'

    @api.multi
    def performanceavgquarterscalculate_check(self):
        _logger = logging.getLogger(__name__)
        self.env.cr.execute("Delete From hr_performanceavgquarters")
        self.env.cr.execute("Delete From hr_performanceavggroup")

        role_set = set([x.role + ',' + x.role1 for x in  self.env['hr.performancebonustotal'].search([])])
        
        for role12 in role_set:
            avg_jjzzj = 0.0
            total_ywl = 0.0
            total_ccs = 0.0
            total_mhs = 0.0
            ccl = 0.0
            zql = 0.0
            dhl = 0.0
            role,role1 = role12.split(',')
            datas = performancebonustotal = self.env['hr.performancebonustotal'].search(
                [('role', '=', role),('role1', '=', role1)])
            data_details = performancebonustotal = self.env['hr.performancebonus'].search(
                [('role', '=', role),('role1', '=', role1),('ywlx', '=', u'录入')])
            temp_list = [data.jjzzj_bb for data in datas]
            if len(temp_list)>0:
                avg_jjzzj = sum(temp_list)/len(temp_list)
                total_ywl = sum([data.ywzl for data in data_details])
                if total_ywl>0:
                    total_ccs = sum([data.ccs for data in data_details])
                    total_mhs = sum([data.tjyxmh for data in data_details])
                    ccl = total_ccs/total_ywl
                    zql = 1- ccl
                    dhl = total_mhs/total_ywl

                    self.env['hr.performanceavgquarters'].create({
                    'role': role,'role1': role1,'avg_jjzzj': avg_jjzzj,'total_ywl': total_ywl,
                    'total_mhs': total_mhs,'total_ccs': total_ccs,'ccl': ccl,'zql': zql,'dhl': dhl})


        role_group_set = set([x.role + ',' + x.group for x in  self.env['hr.performancebonustotal'].search([]) if x.role and x.group])
        performanceremovemember_datas = self.env['hr.performanceremovemember'].search([])
        remove_member_set = set([x.teller_num for x in performanceremovemember_datas])
        for role12 in role_group_set:
            avg_jjzzj = 0.0
            total_ywl = 0.0
            total_ccs = 0.0
            total_mhs = 0.0
            ccl = 0.0
            zql = 0.0
            dhl = 0.0
            role,group = role12.split(',')
            datas = performancebonustotal = self.env['hr.performancebonustotal'].search(
                [('role', '=', role),('group', '=', group)])
            data_details = performancebonustotal = self.env['hr.performancebonus'].search(
                [('role', '=', role),('group', '=', group),('ywlx', '=', u'录入')])
            temp_list = [data.jjzzj_bb for data in datas if not data.teller_num in remove_member_set]
            if len(temp_list)>0:
                avg_jjzzj = sum(temp_list)/len(temp_list)
                total_ywl = sum([data.ywzl for data in data_details if not data.teller_num in remove_member_set])
                if total_ywl>0:
                    total_ccs = sum([data.ccs for data in data_details if not data.teller_num in remove_member_set])
                    total_mhs = sum([data.tjyxmh for data in data_details if not data.teller_num in remove_member_set])
                    ccl = total_ccs/total_ywl
                    zql = 1- ccl
                    dhl = total_mhs/total_ywl

                    self.env['hr.performanceavggroup'].create({
                    'role': role,'group': group,'avg_jjzzj': avg_jjzzj,'total_ywl': total_ywl,
                    'total_mhs': total_mhs,'total_ccs': total_ccs,'ccl': ccl,'zql': zql,'dhl': dhl})