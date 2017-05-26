# -*- coding: utf-8 -*-
import sys
from openerp import api, models
import threading
import logging
import itertools
from operator import itemgetter, attrgetter

reload(sys)
sys.setdefaultencoding('utf-8')

class HrPerformanceBonusCompute(models.TransientModel):
    _name = 'hr.performance.bonus.compute'
    _description = 'HR Performancebonus Compute'

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

    @api.multi
    def performancebonus_compute(self):
        gwxs_role = (u'录入', u'行号选择', u'行号录入')
        lurushenhe_role1_group = (u'A', u'B', u'E', u'F')
        source_list = (u'绩效报表', u'双中心绩效报表', u'信用卡报表',u'双中心信用卡报表')
        performancelurushenheparameter_datas =self.env['hr.performancelurushenheparameter'].search([])  # 录入审核计奖参数
        role_datas = self.env['hr.performanceroleori'].search([])
        for rd in role_datas:
            performancereportori_datas = self.env[
                'hr.performancereportori'].search([('teller_name', '=', rd.name)])
            performancemobilereportori_datas = self.env[
                'hr.performancemobilereportori'].search([('teller_name', '=', rd.name)])
            performancebranchreportori_datas = self.env[
                'hr.performancebranchreportori'].search([('teller_name', '=', rd.name)])
            performancebranchmobilereportori_datas = self.env[
                'hr.performancebranchmobilereportori'].search([('teller_name', '=', rd.name)])


            performanceattendance_datas = self.env[
                'hr.performanceattendance'].search([('teller_name', '=', rd.name)])
            jjcs = self.env['hr.performanceparameter'].search(
                    [('role', '=', rd.role)])
            gwxs = self.env['hr.performanceglobalparameter'].search(
                    [('parameter_name', '=', rd.role1)])

            for p in performancereportori_datas:
                zshzjs = 0.0
                para = self.env['hr.performanceparameter'].search([('role', '=', p.role)], limit=1)
                if para.jjfs == 'byByte':
                    if p.role == u'影像定位':
                        p1 = self.env['hr.performanceparameter'].search([('parameter_name', '=', u'影像定位账户激活')], limit=1)
                        p2 = self.env['hr.performanceparameter'].search([('parameter_name', '=', u'影像定位其他')], limit=1)
                        zshzjs += p.yxdw_zhjh * p1.parameter_valuex
                        zshzjs += p.yxdw_qt * p2.parameter_valuex
                    else:
                        zshzjs = p.lrhzs * para.parameter_valuex  + p.lrzjs
                elif  para.jjfs == 'byQuantity':
                    zshzjs = p.ywzl * para.parameter_valuex
                elif  para.jjfs == 'byTime':
                    zshzjs = p.ywzl * para.parameter_valuex
                performancebonusdetail = self.env['hr.performancebonus'].create({#'performancebonus_id': self.id,
                                                                                 'teller_num': rd.teller_num,
                                                                                 'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                                                                                 'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                                                                                 'ywlx': p.role, 'ywzhs': p.ywzhs, 'ywzl': p.ywzl,
                                                                                 'hzs': p.lrhzs, 'zjs': p.lrzjs, 'ccs': p.lrccs,
                                                                                 'tjyxmh': p.tjyxmh,  'dhl': 0.0, 'gwxs': gwxs.parameter_value,
                                                                                 'zshzjs': zshzjs,'cwl': 0.0, 'zql': 0.0,'source_from': source_list[0]
                                                                                 })
            for p in performancebranchreportori_datas:
                zshzjs = 0.0
                para = self.env['hr.performanceparameter'].search([('role', '=', p.role)], limit=1)
                if para.jjfs == 'byByte':
                    if p.role == u'影像定位':
                        p1 = self.env['hr.performanceparameter'].search([('parameter_name', '=', u'影像定位账户激活')], limit=1)
                        p2 = self.env['hr.performanceparameter'].search([('parameter_name', '=', u'影像定位其他')], limit=1)
                        zshzjs += p.yxdw_zhjh * p1.parameter_valuex
                        zshzjs += p.yxdw_qt * p2.parameter_valuex
                    else:
                        zshzjs = p.lrhzs * para.parameter_valuex  + p.lrzjs
                elif  para.jjfs == 'byQuantity':
                    zshzjs = p.ywzl * para.parameter_valuex
                elif  para.jjfs == 'byTime':
                    zshzjs = p.ywzl * para.parameter_valuex
                performancebonusdetail = self.env['hr.performancebonus'].create({#'performancebonus_id': self.id,
                                                                                 'teller_num': rd.teller_num,
                                                                                 'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                                                                                 'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                                                                                 'ywlx': p.role, 'ywzhs': p.ywzhs, 'ywzl': p.ywzl,
                                                                                 'hzs': p.lrhzs, 'zjs': p.lrzjs, 'ccs': p.lrccs,
                                                                                 'tjyxmh': p.tjyxmh,  'dhl': 0.0, 'gwxs': gwxs.parameter_value,
                                                                                 'zshzjs': zshzjs,'cwl': 0.0, 'zql': 0.0,'source_from': source_list[1]
                                                                                 })
            for p in performancemobilereportori_datas:
                if not p.teller_name in u'虚拟柜员':
                    zshzjs = 0.0
                    para = self.env['hr.performanceparameter'].search([('role', '=', p.role)], limit=1)
                    if para.jjfs == 'byByte':
                        zshzjs = p.lrhzs * para.parameter_valuex  + p.lrzjs
                    elif  para.jjfs == 'byQuantity':
                        zshzjs = p.ywbs * para.parameter_valuex
                    elif  para.jjfs == 'bySub':
                        zshzjs = p.zrwxzs * para.parameter_valuex
                    elif  para.jjfs == 'byTime':
                        zshzjs = p.ywzhs * para.parameter_valuex
                    performancebonusdetail = self.env['hr.performancebonus'].create({#'performancebonus_id': self.id,
                                                                                     'teller_num': rd.teller_num,
                                                                                     'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                                                                                     'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                                                                                     'ywlx': p.role, 'ywzhs': p.ywzhs, 'ywbs': p.ywbs,
                                                                                     'hzs': p.lrhzs, 'zjs': p.lrzjs, 'ccs': p.ccs,
                                                                                     'tjyxmh': p.tjyxmhs,  'dhl': 0.0, 'gwxs': gwxs.parameter_value,
                                                                                     'zshzjs': zshzjs,'cwl': 0.0, 'zql': 0.0,'source_from': source_list[2]
                                                                                     })

            for p in performancebranchmobilereportori_datas:
                if not p.teller_name in u'虚拟柜员':
                    zshzjs = 0.0
                    para = self.env['hr.performanceparameter'].search([('role', '=', p.role)], limit=1)
                    if para.jjfs == 'byByte':
                        zshzjs = p.lrhzs * para.parameter_valuex  + p.lrzjs
                    elif  para.jjfs == 'byQuantity':
                        zshzjs = p.ywbs * para.parameter_valuex
                    elif  para.jjfs == 'bySub':
                        zshzjs = p.zrwxzs * para.parameter_valuex
                    elif  para.jjfs == 'byTime':
                        zshzjs = p.ywzhs * para.parameter_valuex
                    performancebonusdetail = self.env['hr.performancebonus'].create({#'performancebonus_id': self.id,
                                                                                     'teller_num': rd.teller_num,
                                                                                     'teller_name': rd.name, 'identity': u'派遣', 'quarters': rd.quarters,
                                                                                     'group': rd.work_group, 'role': rd.role, 'role1': rd.role1,
                                                                                     'ywlx': p.role, 'ywzhs': p.ywzhs, 'ywbs': p.ywbs,
                                                                                     'hzs': p.lrhzs, 'zjs': p.lrzjs, 'ccs': p.lrccs,
                                                                                     'tjyxmh': p.tjyxmhs,  'dhl': 0.0, 'gwxs': gwxs.parameter_value,
                                                                                     'zshzjs': zshzjs,'cwl': 0.0, 'zql': 0.0,'source_from': source_list[3]
                                                                                     })


        for rd in role_datas:
            if rd.role1 != u'专业化岗位':
                # get cwl zql dhl，only related by lr
                performancebonus_datas = self.env['hr.performancebonus'].search(
                    [('teller_name', '=', rd.name),('ywlx', '=', u'录入')])
                tempccs = sum([i.ccs for i in performancebonus_datas])
                tempywzl = sum([i.ywzl for i in performancebonus_datas])
                temptjyxmh = sum([i.tjyxmh for i in performancebonus_datas])
                if tempywzl != 0:
                    cwl = tempccs/tempywzl
                    zql = 1.0 - cwl
                    dhl = temptjyxmh/tempywzl
                    for pd in performancebonus_datas:
                        pd.write({'zql': zql, 'cwl': cwl, 'dhl': dhl})

                # get jjdj sskcs
                performancebonus_datas_byname = self.env['hr.performancebonus'].search(
                    [('teller_name', '=', rd.name)])
                # if rd.role1 in lurushenhe_role1_group:
                for plsp in performancelurushenheparameter_datas:
                    rolelist = [i for i in plsp.role.split(',')]
                    quantity = sum([i.zshzjs for i in performancebonus_datas_byname if i.ywlx in rolelist])
                    jjdj, sskcs = self.get_lurushenheparameter(plsp.quarters, quantity)
                    for pd in performancebonus_datas_byname:
                        if pd.ywlx in rolelist:
                            pd.write({'jjdj': jjdj, 'sskcs': sskcs})
            # else:
            #     performancebonus_datas_byname_byrole1 = self.env['hr.performancebonus'].search(
            #         [('teller_name', '=', rd.name),('role1', '=', u'专业化岗')])

# =AE2+AG2+AI2+AK2+AZ2+BA2
# "基本录入总字节*岗位系数
# (6)=(4)*(5)"
# 资料录入折合字节（7）
# 影像定位折合字节(8-1)
# 影像定位折合字节(8-2)

# 信用卡录入总字节
# 录入补业务量字节


# class HrPerformanceBonuscalculationCompute(models.TransientModel):
    # _name = 'hr.performance.bonuscalculation.compute'
    # _description = 'HR Performancebonuscalculation Compute'

    # @api.multi
    # def performancebonuscalculation_compute(self):
        # role_datas=self.env['hr.performanceroleori'].search([])
        # for rd in role_datas:
            # recruitmentmodeldetail=self.env['hr.performancebonuscalculation'].create({'performancebonuscalculation_id': self.id,
                # 'teller_num': rd.teller_num,
                # 'teller_name':rd.name,'identity':'派遣','quarters':rd.quarters,
                # 'group':rd.work_group,'role':rd.role,
                # 'role1':rd.role1
                # })


class HrPerformanceBonusDelete(models.TransientModel):
    _name = 'hr.performance.bonus.delete'
    _description = 'HR Performancebonus Delete'

    @api.multi
    def performancebonus_delete(self):
        # performancebonuscalculation = self.env[
        #     'hr.performancebonus'].search([])
        # for r in performancebonuscalculation:
        #     r.unlink()
        performancebonustotal = self.env[
            'hr.performancebonustotal'].search([])
        for r in performancebonustotal:
            r.unlink()

class HrPerformanceOriReportDelete(models.TransientModel):
    _name = 'hr.performance.orireport.delete'
    _description = 'HR Ori Report Delete'

    @api.multi
    def performanceorireport_delete(self):
        # TODO:delete ori report
        performancereportori_datas = self.env[
            'hr.performancereportori'].search([])
        for r in performancereportori_datas:
            r.unlink()
        performancemobilereportori_datas = self.env[
            'hr.performancemobilereportori'].search([])
        for r in performancemobilereportori_datas:
            r.unlink()    
        performancebranchreportori_datas = self.env[
            'hr.performancebranchreportori'].search([])
        for r in performancebranchreportori_datas:
            r.unlink()
        performancebranchmobilereportori_datas = self.env[
            'hr.performancebranchmobilereportori'].search([])
        for r in performancebranchmobilereportori_datas:
            r.unlink() 


class HrPerformanceProCalculationCompute(models.TransientModel):  # 生成
    _name = 'hr.performance.procalculation.compute'
    _description = 'HR PerformancePro Calculation Compute'


    @api.multi
    def performanceprocalculation_compute(self):
        role_datas = self.env['hr.performanceroleori'].search([])
        gwxs_role_list = (u'录入', u'行号选择', u'行号录入')
        lurushenhe_role1_list = (u'A', u'B', u'E', u'F')
        source_list = (u'绩效报表', u'双中心绩效报表', u'信用卡报表',u'双中心信用卡报表')
        performancelurushenheparameter_datas = self.env['hr.performancelurushenheparameter'].search([])
        performancegoal_datas = self.env['hr.performancegoal'].search([])

        for rd in role_datas:
            performancebonus_datas = self.env['hr.performancebonus'].search(
                    [('teller_name', '=', rd.name)])
            if not performancebonus_datas:
                continue


            # paramater
            cwl = 0.00000
            zql = 0.00000
            dhl = 0.00000
            jjdj, sskcs = 0.0, 0.0
            sh_jjdj = 0.0
            sh_sskcs = 0.0

            jj = 0.0
            ranking = 0
            kj = 0.0

            jblr_mul_gwxs_ae = 0.0
            jjzzj_bb   = 0.0
            lrjj_be = 0.0
            lrzlj_bk = 0.0
            shywlxj_cy = 0.0
            shjj_db = 0.0
            zyhgwjbzywzshs_dy = 0.0
            zyhgwbzj_dz = 0.0
            teller_num = performancebonus_datas[0].teller_num
            teller_name =performancebonus_datas[0].teller_name
            identity = performancebonus_datas[0].identity
            quarters = performancebonus_datas[0].quarters
            quarters_date = performancebonus_datas[0].quarters_date
            group = performancebonus_datas[0].group
            role = performancebonus_datas[0].role
            role1 = performancebonus_datas[0].role1
            if role1 != u'专业化岗位':
                except_list=[]
                for plsp in performancelurushenheparameter_datas:
                    role_list = [i for i in plsp.role.split(',')]
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
                                jjdj = i.jjdj if i.jjdj != 0.0 else jjdj
                                sskcs = i.sskcs if i.sskcs != 0.0 else sskcs
                    elif plsp.quarters == u'审核岗':
                        for i in performancebonus_datas:
                            if i.ywlx in role_list:
                                shywlxj_cy += i.zshzjs
                                sh_jjdj = i.jjdj
                                sh_sskcs = i.sskcs

                jblr_mul_gwxs_ae = sum([current_account.zshzjs * current_account.gwxs for current_account in performancebonus_datas if current_account.ywlx in gwxs_role_list and u'绩效' in current_account.source_from])
                jjzzj_bb += jblr_mul_gwxs_ae
                lrjj_be = jjzzj_bb * jjdj - sskcs

                for i in performancegoal_datas:
                    if i.role == role and  i.role1 == role1:
                        zqlxs = (1+(zql-i.zql_goal)*100)
                        lhlxs = (1+(i.fql_goal - dhl))
                        lrzlj_bk = zqlxs*lhlxs
                        lrzlj_bk = (lrzlj_bk - 1) * lrjj_be

                shjj_db = shywlxj_cy * sh_jjdj - sh_sskcs

                for p in performancebonus_datas:
                    if not p.ywlx in except_list or not u'绩效' in p.source_from:
                        jj += p.zshzjs

                jj += lrjj_be + lrzlj_bk + shjj_db
            else:
                jj = sum([i.zshzjs for i in performancebonus_datas]) 
                   

            

            performancebonustotal = self.env['hr.performancebonustotal'].create({'teller_num': teller_num,
                                                                                  'teller_name': teller_name, 'identity': '派遣', 'quarters': rd.quarters,
                                                                                  'group': rd.work_group, 'role': rd.role,
                                                                                  'role1': rd.role1, 'jblr_mul_gwxs_ae':jblr_mul_gwxs_ae,
                                                                                  'jjzzj_bb':jjzzj_bb,'lrjj_be':lrjj_be,
                                                                                  'lrzlj_bk':lrzlj_bk,'shywlxj_cy':shywlxj_cy,
                                                                                  'shjj_db':shjj_db,'zyhgwjbzywzshs_dy':zyhgwjbzywzshs_dy,
                                                                                  'zyhgwbzj_dz':zyhgwbzj_dz,'kj':kj,
                                                                                  'jj':jj,'ranking':ranking,
                                                                                    'lrjjdj_bc':jjdj,'sskc_bd':sskcs,
                                                                                    'shjjdj_cz':sh_jjdj,'shsskc_da':sh_sskcs,
                                                                                  })

        datas = self.env['hr.performancebonustotal'].search([('role1','=',u'专业化岗位')])
        datas=datas.sorted(key=attrgetter('role', 'jj'), reverse=True)
        lastrole = ''
        rank = 0
        lastjj=0.0
        samecount = 0
        for d in datas:
            if lastrole=='' or d.role == lastrole:
                if lastjj == d.jj:
                    samecount += 1
                else:
                    rank = rank + 1 if samecount == 0 else rank+samecount
                    samecount = 0
                lastrole = d.role
                lastjj = d.jj
            else:
                rank = 1
                # rank += 1
                lastrole = d.role
            d.write({'ranking':rank})