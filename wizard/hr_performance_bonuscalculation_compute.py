# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

#
# Order Point Method:
#    - Order if the virtual stock of today is bellow the min of the defined order point
#hr_performance_bonuscalculation_compute.py

from openerp import api, models
import threading



class HrPerformanceBonusCompute(models.TransientModel):
    _name = 'hr.performance.bonus.compute'
    _description = 'HR Performancebonus Compute'

    @api.multi
    def performancebonus_compute(self):
        role_datas=self.env['hr.performanceroleori'].search([])
        for rd in role_datas:
            #performanceglobalparameter_datas=self.env['hr.performanceglobalparameter'].search([])  #全局参数
            performanceparameter_datas=self.env['hr.performanceparameter'].search([])              #计奖参数  
            performancelurushenheparameter_datas=self.env['hr.performancelurushenheparameter'].search([])#录入审核计奖参数 
            
            
            
            
            
            performancereportori_datas=self.env['hr.performancereportori'].search([('teller_name','=',rd.name)])
            performancemobilereportori_datas=self.env['hr.performancemobilereportori'].search([('teller_name','=',rd.name)])
            performancebranchreportori_datas=self.env['hr.performancebranchreportori'].search([('teller_name','=',rd.name)])
            performancebranchmobilereportori_datas=self.env['hr.performancebranchmobilereportori'].search([('teller_name','=',rd.name)])
            
            
            for p in performancereportori_datas:

                performancebonusdetail=self.env['hr.performancebonus'].create({'performancebonus_id': self.id,
                                                                                 'teller_num': rd.teller_num,
                                                                                 'teller_name':rd.name,'identity':'派遣','quarters':rd.quarters,
                                                                                 'group':rd.work_group,'role':rd.role,'role1':rd.role1,
                                                                                 'ywlx':p.role,'ywzhs':p.ywzhs,'ywzl':p.ywzl,
                                                                                 'hzs':p.lrhzs,'zjs':p.lrzjs,'ccs':p.lrccs,
                                                                                 'tjyxmh':p.tjyxmh ,'cwl':p.lrcwl,'zql':p.lrzql,
                                                                                 'dhl':p.lrdhl
                                                                                 #,'jbzjs':,'gwxs':,
                                                                                 #'zshzjs':,'jjdj':,'sskcs':,
                                                                                 #'khxs':,'kj':,'jj':                                                                             
                                                                                 })
            
            
            
            
            




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
        
        performancebonuscalculation=self.env['hr.performancebonus'].search([])
        for r in performancebonuscalculation:
            r.unlink()

class HrPerformanceOriReportDelete(models.TransientModel):
    _name = 'hr.performance.orireport.delete'
    _description = 'HR Ori Report Delete'          
    
    @api.multi
    def performanceorireport_delete(self):
        #TODO:delete ori report
        pass
         
            
            
class HrPerformanceProCalculationCompute(models.TransientModel):
    _name = 'hr.performance.procalculation.compute'
    _description = 'HR PerformancePro Calculation Compute'

    
    @api.multi
    def performanceprocalculation_compute(self):
        role_datas=self.env['hr.performanceroleori'].search([])
        for rd in role_datas:
            recruitmentmodeldetail=self.env['hr.performancespecialistportfoliocalculation'].create({'performancespecialistportfoliocalculation_id': self.id,
                                                                                 'teller_num': rd.teller_num,
                                                                                 'teller_name':rd.name,'identity':'派遣','quarters':rd.quarters,
                                                                                 'group':rd.work_group,'role':rd.role,
                                                                                 'role1':rd.role1
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
