# -*- coding: utf-8 -*-
import sys
from openerp import api, models
import threading
import logging

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
        performancelurushenheparameter_datas =self.env['hr.performancelurushenheparameter'].search([])  # 录入审核计奖参数
        role_datas = self.env['hr.performanceroleori'].search([])
        for rd in role_datas:
            # performanceparameter_datas = self.env['hr.performanceparameter'].search([])              # 计奖参数
         
            performancereportori_datas = self.env[
                'hr.performancereportori'].search([('teller_name', '=', rd.name)])
            performancemobilereportori_datas = self.env[
                'hr.performancemobilereportori'].search([('teller_name', '=', rd.name)])
            performancebranchreportori_datas = self.env[
                'hr.performancebranchreportori'].search([('teller_name', '=', rd.name)])
            performancebranchmobilereportori_datas = self.env[
                'hr.performancebranchmobilereportori'].search([('teller_name', '=', rd.name)])

            for p in performancereportori_datas:
                jjcs = self.env['hr.performanceparameter'].search(
                    [('role', '=', rd.role)])
                gwxs = self.env['hr.performanceglobalparameter'].search(
                    [('parameter_name', '=', rd.role1)])
                # _logger = logging.getLogger(__name__)  
                # _logger.info(p.role) 
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
                                                                                 'zshzjs': zshzjs,'cwl': 0.0, 'zql': 0.0,
                                                                                 
                                                                                 #'jjdj':,'sskcs':,
                                                                                 #'khxs':,'kj':,'jj':
                                                                                 })

        for rd in role_datas:
            if rd.role1 != u'专业化岗':
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

        performancebonuscalculation = self.env[
            'hr.performancebonus'].search([])
        for r in performancebonuscalculation:
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


class HrPerformanceProCalculationCompute(models.TransientModel):
    _name = 'hr.performance.procalculation.compute'
    _description = 'HR PerformancePro Calculation Compute'

    @api.multi
    def performanceprocalculation_compute(self):
        role_datas = self.env['hr.performanceroleori'].search([])
        for rd in role_datas:
            recruitmentmodeldetail = self.env['hr.performancespecialistportfoliocalculation'].create({'performancespecialistportfoliocalculation_id': self.id,
                                                                                                      'teller_num': rd.teller_num,
                                                                                                      'teller_name': rd.name, 'identity': '派遣', 'quarters': rd.quarters,
                                                                                                      'group': rd.work_group, 'role': rd.role,
                                                                                                      'role1': rd.role1
                                                                                                      })

    # def _procure_calculation_orderpoint(self):
        # with api.Environment.manage():
            # # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            # new_cr = self.pool.cursor()
            # self = self.with_env(self.env(cr=new_cr))
            # self.env['procurement.order']._procure_orderpoint_confirm(
            # use_new_cursor=new_cr.dbname,
            # company_id=self.env.user.company_id.id)
            # new_cr.close()
            # return {}

    # @api.multi
    # def procure_calculation(self):
        # threaded_calculation = threading.Thread(target=self._procure_calculation_orderpoint, args=())
        # threaded_calculation.start()
        # return {'type': 'ir.actions.act_window_close'}


# read_group(*args, **kwargs)
# Get the list of records in list view grouped by the given groupby fields
# Parameters
# cr -- database cursor
# uid -- current user id
# domain -- list specifying search criteria [['field_name', 'operator', 'value'], ...]
# fields (list) -- list of fields present in the list view specified on the object
# groupby (list) -- list of groupby descriptions by which the records will be grouped. A groupby description is either a field (then it will be grouped by that field) or a string 'field:groupby_function'. Right now, the only functions supported are 'day', 'week', 'month', 'quarter' or 'year', and they only make sense for date/datetime fields.
# offset (int) -- optional number of records to skip
# limit (int) -- optional max number of records to return
# context (dict) -- context arguments, like lang, time zone.
# orderby (list) -- optional order by specification, for overriding the natural sort ordering of the groups, see also search() (supported only for many2one fields currently)
# lazy (bool) -- if true, the results are only grouped by the first groupby and the remaining groupbys are put in the __context key. If false, all the groupbys are done in one call.
# Returns
# list of dictionaries(one dictionary for each record) containing:

# the values of fields grouped by the fields in groupby argument
# __domain: list of tuples specifying the search criteria
# __context: dictionary with argument like groupby
# Return type [{'field_name_1': value, ...]
# Raises  AccessError --
# if user has no read rights on the requested object
# if user tries to bypass access rules for read on the requested object


# class your_class(osv.osv):
#     # ...

#     def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False, lazy=True):
#         res = super(your_class, self).read_group(cr, uid, domain, fields, groupby, offset, limit=limit, context=context, orderby=orderby, lazy=lazy)
#         if 'amount_pending' in fields:
#             for line in res:
#                 if '__domain' in line:
#                     lines = self.search(cr, uid, line['__domain'], context=context)
#                     pending_value = 0.0
#                     for current_account in self.browse(cr, uid, lines, context=context):
#                         pending_value += current_account.amount_pending
#                     line['amount_pending'] = pending_value
#         if 'amount_payed' in fields:
#             for line in res:
#                 if '__domain' in line:
#                     lines = self.search(cr, uid, line['__domain'], context=context)
#                     payed_value = 0.0
#                     for current_account in self.browse(cr, uid, lines, context=context):
#                         payed_value += current_account.amount_payed
#                     line['amount_payed'] = payed_value
#         return res


#         class your_class(osv.osv):
#     # ...

#     def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False, lazy=True):
#         if 'column' in fields:
#             fields.remove('column')
# return super(your_class, self).read_group(cr, uid, domain, fields,
# groupby, offset, limit=limit, context=context, orderby=orderby,
# lazy=lazy):
