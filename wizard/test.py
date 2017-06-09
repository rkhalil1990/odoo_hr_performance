# -*- coding: utf-8 -*-

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



# y = '录入'
# s = [u'\u5f55\u5165', u'\u884c\u53f7\u5f55\u5165', u'\u884c\u53f7\u9009\u62e9']
# x = u'\u5f55\u5165'




# uname = y.decode('GBK')
# print uname
# print x.encode("utf-8").decode('utf-8')
# print y.encode('utf-8')
# print u'\u98de\u8f6c\u9080\u8bf7\u6392\u884c\u699c'.encode('utf-8')
# print unicode('呵呵','utf-8')
# 
# a = [1, 2, 3, 4]
# b = [1, 2]


s = u'你好-哈哈哈'
x = u'你好-哈哈哈'


print x + s
# 
# 
# import re


# r = re.sub(r'not[\w\d\s]*bad', 'good','This dinner is not that bad!')
# print r
# print s.replace(r.group[0], 'good')
# import base64

# a = '6KaB54K577yaSlTmsqHog4zmma/vvJtMWemHjOmdouS6i+WEv+aMuuWkp++8m0xLUeWkseWKv++8m0xGRuiAgeWFrOiiq25lbmfmrbs='
# b = base64.b64decode(a)


# def print_msg():
#     # print_msg 是外围函数
#     msg = "zen of python"
#     def printer():
#         # printer 是嵌套函数
#         print(msg)
#     return printer

# another = print_msg()
# # 输出 zen of python
# print another
# another()