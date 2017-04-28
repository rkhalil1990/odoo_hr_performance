# -*- coding: utf-8 -*-
from openerp import http

# class ChangeRequest(http.Controller):
#     @http.route('/change_request/change_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/change_request/change_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('change_request.listing', {
#             'root': '/change_request/change_request',
#             'objects': http.request.env['change_request.change_request'].search([]),
#         })

#     @http.route('/change_request/change_request/objects/<model("change_request.change_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('change_request.object', {
#             'object': obj
#         })