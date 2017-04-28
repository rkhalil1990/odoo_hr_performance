# -*- coding: utf-8 -*-

from collections import defaultdict
import logging
import re
import time
import types

import openerp
from openerp import SUPERUSER_ID
from openerp import models, tools, api

from openerp.modules.registry import RegistryManager
from openerp.osv import fields, osv
from openerp.osv.orm import BaseModel, Model, MAGIC_COLUMNS
from openerp.exceptions import UserError, AccessError

_logger = logging.getLogger(__name__)

MODULE_UNINSTALL_FLAG = '_force_unlink'

def _get_fields_type(self, cr, uid, context=None):
    # Avoid too many nested `if`s below, as RedHat's Python 2.6
    # break on it. See bug 939653.
    return sorted([(k,k) for k,v in fields.__dict__.iteritems()
                      if type(v) == types.TypeType and \
                         issubclass(v, fields._column) and \
                         v != fields._column and \
                         not v._deprecated and \
                         not issubclass(v, fields.function)])

def _in_modules(self, cr, uid, ids, field_name, arg, context=None):
    #pseudo-method used by fields.function in ir.model/ir.model.fields
    module_pool = self.pool["ir.module.module"]
    installed_module_ids = module_pool.search(cr, uid, [('state','=','installed')])
    installed_module_names = module_pool.read(cr, uid, installed_module_ids, ['name'], context=context)
    installed_modules = set(x['name'] for x in installed_module_names)

    result = {}
    xml_ids = osv.osv._get_xml_ids(self, cr, uid, ids)
    for k,v in xml_ids.iteritems():
        result[k] = ', '.join(sorted(installed_modules & set(xml_id.split('.')[0] for xml_id in v)))
    return result

    
class HrPerformanceFields(osv.osv):
    _name = 'hr.performancefields'
    _description = "Hr Performancefields"
    _rec_name = 'field_description'

    _columns = {
        'name': fields.char('Field Name', required=True, select=1),
        'complete_name': fields.char('Complete Name', select=1),
        'model': fields.char('Object Name', required=True, select=1,
            help="The technical name of the model this field belongs to"),
        'relation': fields.char('Object Relation',
            help="For relationship fields, the technical name of the target model"),
        'relation_field': fields.char('Relation Field',
            help="For one2many fields, the field on the target model that implement the opposite many2one relationship"),
        'model_id': fields.many2one('ir.model', 'Model', required=True, select=True, ondelete='cascade',
            help="The model this field belongs to"),
        'field_description': fields.char('Field Label', required=True, translate=True),
        'help': fields.text('Field Help', translate=True),
        'ttype': fields.selection(_get_fields_type, 'Field Type', required=True),
        'selection': fields.char('Selection Options', help="List of options for a selection field, "
            "specified as a Python expression defining a list of (key, label) pairs. "
            "For example: [('blue','Blue'),('yellow','Yellow')]"),
        'copy': fields.boolean('Copied', help="Whether the value is copied when duplicating a record."),
        'related': fields.char('Related Field', help="The corresponding related field, if any. This must be a dot-separated list of field names."),
        'required': fields.boolean('Required'),
        'readonly': fields.boolean('Readonly'),
        'index': fields.boolean('Indexed'),
        'translate': fields.boolean('Translatable', help="Whether values for this field can be translated (enables the translation mechanism for that field)"),
        'size': fields.integer('Size'),
        'state': fields.selection([('manual','Custom Field'),('base','Base Field')],'Type', required=True, readonly=True, select=1),
        'on_delete': fields.selection([('cascade', 'Cascade'), ('set null', 'Set NULL'), ('restrict', 'Restrict')],
                                      'On Delete', help='On delete property for many2one fields'),
        'domain': fields.char('Domain', help="The optional domain to restrict possible values for relationship fields, "
            "specified as a Python expression defining a list of triplets. "
            "For example: [('color','=','red')]"),
        'groups': fields.many2many('res.groups', 'ir_model_fields_group_rel', 'field_id', 'group_id', 'Groups'),
        'selectable': fields.boolean('Selectable'),
        'modules': fields.function(_in_modules, type='char', string='In Apps', help='List of modules in which the field is defined'),
        'serialization_field_id': fields.many2one('ir.model.fields', 'Serialization Field', domain = "[('ttype','=','serialized')]",
                                                  ondelete='cascade', help="If set, this field will be stored in the sparse "
                                                                           "structure of the serialization field, instead "
                                                                           "of having its own database column. This cannot be "
                                                                           "changed after creation."),
        'relation_table': fields.char("Relation Table", help="Used for custom many2many fields to define a custom relation table name"),
        'column1': fields.char("Column 1", help="Column referring to the record in the model table"),
        'column2': fields.char("Column 2", help="Column referring to the record in the comodel table"),
        'compute': fields.text("Compute", help="Code to compute the value of the field.\n"
                        "Iterate on the recordset 'self' and assign the field's value:\n\n"
                        "    for record in self:\n"
                        "        record['size'] = len(record.name)\n\n"
                        "Modules time, datetime, dateutil are available."),
        'depends': fields.char("Dependencies", help="Dependencies of compute method; "
                        "a list of comma-separated field names, like\n\n"
                        "    name, partner_id.name"),
    }
    _rec_name='field_description'
    _defaults = {
        'selection': "",
        'domain': "[]",
        'name': 'x_',
        'model':'hr.performancefields',
        'state': 'manual',
        'on_delete': 'set null',
        'field_description': '',
        'selectable': 1,
    }
    _order = "name"

    def _check_selection(self, cr, uid, selection, context=None):
        try:
            selection_list = eval(selection)
        except Exception:
            _logger.info('Invalid selection list definition for fields.selection', exc_info=True)
            raise UserError(_("The Selection Options expression is not a valid Pythonic expression."
                                "Please provide an expression in the [('key','Label'), ...] format."))

        check = True
        if not (isinstance(selection_list, list) and selection_list):
            check = False
        else:
            for item in selection_list:
                if not (isinstance(item, (tuple,list)) and len(item) == 2):
                    check = False
                    break

        if not check:
                raise UserError(_("The Selection Options expression is must be in the [('key','Label'), ...] format!"))
        return True

    def _size_gt_zero_msg(self, cr, user, ids, context=None):
        return _('Size of the field can never be less than 0 !')

    _sql_constraints = [
        ('size_gt_zero', 'CHECK (size>=0)',_size_gt_zero_msg ),
    ]

    def _related_field(self):
        """ Return the ``Field`` instance corresponding to ``self.related``. """
        names = self.related.split(".")
        last = len(names) - 1
        model = self.env[self.model or self.model_id.model]
        for index, name in enumerate(names):
            field = model._fields.get(name)
            if field is None:
                raise UserError(_("Unknown field name '%s' in related field '%s'") % (name, self.related))
            if index < last and not field.relational:
                raise UserError(_("Non-relational field name '%s' in related field '%s'") % (name, self.related))
            model = model[name]
        return field

    @api.one
    @api.constrains('related')
    def _check_related(self):
        if self.state == 'manual' and self.related:
            field = self._related_field()
            if field.type != self.ttype:
                raise UserError(_("Related field '%s' does not have type '%s'") % (self.related, self.ttype))
            if field.relational and field.comodel_name != self.relation:
                raise UserError(_("Related field '%s' does not have comodel '%s'") % (self.related, self.relation))

    @api.onchange('related')
    def _onchange_related(self):
        if self.related:
            try:
                field = self._related_field()
            except UserError as e:
                return {'warning': {'title': _("Warning"), 'message': e.message}}
            self.ttype = field.type
            self.relation = field.comodel_name
            self.readonly = True
            self.copy = False

    @api.constrains('depends')
    def _check_depends(self):
        """ Check whether all fields in dependencies are valid. """
        for record in self:
            if not record.depends:
                continue
            for seq in record.depends.split(","):
                if not seq.strip():
                    raise UserError(_("Empty dependency in %r") % (record.depends))
                model = self.env[record.model]
                names = seq.strip().split(".")
                last = len(names) - 1
                for index, name in enumerate(names):
                    field = model._fields.get(name)
                    if field is None:
                        raise UserError(_("Unknown field %r in dependency %r") % (name, seq.strip()))
                    if index < last and not field.relational:
                        raise UserError(_("Non-relational field %r in dependency %r") % (name, seq.strip()))
                    model = model[name]

    @api.onchange('compute')
    def _onchange_compute(self):
        if self.compute:
            self.readonly = True
            self.copy = False

    @api.one
    @api.constrains('relation_table')
    def _check_relation_table(self):
        models.check_pg_name(self.relation_table)

    @api.model
    def _custom_many2many_names(self, model_name, comodel_name):
        """ Return default names for the table and columns of a custom many2many field. """
        rel1 = self.env[model_name]._table
        rel2 = self.env[comodel_name]._table
        table = 'x_%s_%s_rel' % tuple(sorted([rel1, rel2]))
        if rel1 == rel2:
            return (table, 'id1', 'id2')
        else:
            return (table, '%s_id' % rel1, '%s_id' % rel2)

    @api.onchange('ttype', 'model_id', 'relation')
    def _onchange_ttype(self):
        self.copy = (self.ttype != 'one2many')
        if self.ttype == 'many2many' and self.model_id and self.relation:
            names = self._custom_many2many_names(self.model_id.model, self.relation)
            self.relation_table, self.column1, self.column2 = names
        else:
            self.relation_table = False
            self.column1 = False
            self.column2 = False

    @api.onchange('relation_table')
    def _onchange_relation_table(self):
        if self.relation_table:
            # check whether other fields use the same table
            others = self.search([('ttype', '=', 'many2many'),
                                  ('relation_table', '=', self.relation_table),
                                  ('id', 'not in', self._origin.ids)])
            if others:
                for other in others:
                    if (other.model, other.relation) == (self.relation, self.model):
                        # other is a candidate inverse field
                        self.column1 = other.column2
                        self.column2 = other.column1
                        return
                return {'warning':{
                    'title': _("Warning"),
                    'message': _("The table %r if used for other, possibly incompatible fields.") % self.relation_table,
                }}

    def _drop_column(self, cr, uid, ids, context=None):
        tables_to_drop = set()

        for field in self.browse(cr, uid, ids, context):
            if field.name in MAGIC_COLUMNS:
                continue
            model = self.pool[field.model]
            cr.execute('SELECT relkind FROM pg_class WHERE relname=%s', (model._table,))
            result = cr.fetchone()
            cr.execute("""SELECT column_name FROM information_schema.columns
                          WHERE table_name=%s AND column_name=%s""",
                       (model._table, field.name))
            column_name = cr.fetchone()
            if column_name and (result and result[0] == 'r'):
                cr.execute('ALTER table "%s" DROP column "%s" cascade' % (model._table, field.name))
            if field.state == 'manual' and field.ttype == 'many2many':
                rel_name = field.relation_table or model._fields[field.name].relation
                tables_to_drop.add(rel_name)
            model._pop_field(cr, uid, field.name, context=context)

        if tables_to_drop:
            # drop the relation tables that are not used by other fields
            cr.execute("""SELECT relation_table FROM HrPerformanceFields
                          WHERE relation_table IN %s AND id NOT IN %s""",
                       (tuple(tables_to_drop), tuple(ids)))
            tables_to_keep = set(row[0] for row in cr.fetchall())
            for rel_name in tables_to_drop - tables_to_keep:
                cr.execute('DROP TABLE "%s"' % rel_name)

        return True

    def unlink(self, cr, user, ids, context=None):
        # Prevent manual deletion of module columns
        if context is None: context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not context.get(MODULE_UNINSTALL_FLAG) and \
                any(field.state != 'manual' for field in self.browse(cr, user, ids, context)):
            raise UserError(_("This column contains module data and cannot be removed!"))

        self._drop_column(cr, user, ids, context)
        res = super(HrPerformanceFields, self).unlink(cr, user, ids, context)
        if not context.get(MODULE_UNINSTALL_FLAG):
            # The field we just deleted might be inherited, and the registry is
            # inconsistent in this case; therefore we reload the registry.
            cr.commit()
            api.Environment.reset()
            RegistryManager.new(cr.dbname)
            RegistryManager.signal_registry_change(cr.dbname)
        return res

    def create(self, cr, user, vals, context=None):
        if 'model_id' in vals:
            model_data = self.pool['ir.model'].browse(cr, user, vals['model_id'])
            vals['model'] = model_data.model
        if context is None:
            context = {}
        if vals.get('ttype', False) == 'selection':
            if not vals.get('selection',False):
                raise UserError(_('For selection fields, the Selection Options must be given!'))
            self._check_selection(cr, user, vals['selection'], context=context)
        res = super(HrPerformanceFields,self).create(cr, user, vals, context)
        if vals.get('state','manual') == 'manual':
            if not vals['name'].startswith('x_'):
                raise UserError(_("Custom fields must have a name that starts with 'x_' !"))

            if vals.get('relation',False) and not self.pool['ir.model'].search(cr, user, [('model','=',vals['relation'])]):
                raise UserError(_("Model %s does not exist!") % vals['relation'])

            if vals.get('ttype', False) == 'one2many':
                if not self.search(cr, user, [('model_id','=',vals['relation']), ('name','=',vals['relation_field']), ('ttype','=','many2one')]):
                    raise UserError(_("Many2one %s on model %s does not exist!") % (vals['relation_field'], vals['relation']))

            self.pool.clear_manual_fields()

            if vals['model'] in self.pool:
                # setup models; this re-initializes model in registry
                self.pool.setup_models(cr, partial=(not self.pool.ready))
                # update database schema
                model = self.pool[vals['model']]
                ctx = dict(context, update_custom_fields=True)
                model._auto_init(cr, ctx)
                model._auto_end(cr, ctx) # actually create FKs!
                RegistryManager.signal_registry_change(cr.dbname)

        return res

    def write(self, cr, user, ids, vals, context=None):
        if context is None:
            context = {}

        #For the moment renaming a sparse field or changing the storing system is not allowed. This may be done later
        if 'serialization_field_id' in vals or 'name' in vals:
            for field in self.browse(cr, user, ids, context=context):
                if 'serialization_field_id' in vals and field.serialization_field_id.id != vals['serialization_field_id']:
                    raise UserError(_('Changing the storing system for field "%s" is not allowed.') % field.name)
                if field.serialization_field_id and (field.name != vals['name']):
                    raise UserError(_('Renaming sparse field "%s" is not allowed') % field.name)

        # if set, *one* column can be renamed here
        column_rename = None

        # names of the models to patch
        patched_models = set()

        if vals and ids:
            # check selection if given
            if vals.get('selection'):
                self._check_selection(cr, user, vals['selection'], context=context)

            for item in self.browse(cr, user, ids, context=context):
                if item.state != 'manual':
                    raise UserError(_('Properties of base fields cannot be altered in this manner! '
                                        'Please modify them through Python code, '
                                        'preferably through a custom addon!'))

                if vals.get('model_id', item.model_id.id) != item.model_id.id:
                    raise UserError(_("Changing the model of a field is forbidden!"))

                if vals.get('ttype', item.ttype) != item.ttype:
                    raise UserError(_("Changing the type of a field is not yet supported. "
                                      "Please drop it and create it again!"))

                obj = self.pool.get(item.model)
                field = getattr(obj, '_fields', {}).get(item.name)

                if vals.get('name', item.name) != item.name:
                    # We need to rename the column
                    if column_rename:
                        raise UserError(_('Can only rename one field at a time!'))
                    if vals['name'] in obj._fields:
                        raise UserError(_('Cannot rename field to %s, because that field already exists!') % vals['name'])
                    if vals.get('state', 'manual') == 'manual' and not vals['name'].startswith('x_'):
                        raise UserError(_('New field name must still start with x_ , because it is a custom field!'))
                    if '\'' in vals['name'] or '"' in vals['name'] or ';' in vals['name']:
                        raise ValueError('Invalid character in column name')
                    column_rename = (obj._table, item.name, vals['name'], item.index)

                # We don't check the 'state', because it might come from the context
                # (thus be set for multiple fields) and will be ignored anyway.
                if obj is not None and field is not None:
                    patched_models.add(obj._name)

        # These shall never be written (modified)
        for column_name in ('model_id', 'model', 'state'):
            if column_name in vals:
                del vals[column_name]

        res = super(HrPerformanceFields,self).write(cr, user, ids, vals, context=context)

        self.pool.clear_manual_fields()

        if column_rename:
            # rename column in database, and its corresponding index if present
            table, oldname, newname, index = column_rename
            cr.execute('ALTER TABLE "%s" RENAME COLUMN "%s" TO "%s"' % (table, oldname, newname))
            if index:
                cr.execute('ALTER INDEX "%s_%s_index" RENAME TO "%s_%s_index"' % (table, oldname, table, newname))

        if column_rename or patched_models:
            # setup models, this will reload all manual fields in registry
            self.pool.setup_models(cr, partial=(not self.pool.ready))

        if patched_models:
            # update the database schema of the models to patch
            ctx = dict(context, update_custom_fields=True)
            for model_name in patched_models:
                obj = self.pool[model_name]
                obj._auto_init(cr, ctx)
                obj._auto_end(cr, ctx) # actually create FKs!

        if column_rename or patched_models:
            RegistryManager.signal_registry_change(cr.dbname)

        return res    
    