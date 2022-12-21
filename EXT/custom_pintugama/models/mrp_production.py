from email.policy import default
from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    production_capacity_line_ids = fields.One2many('production.capacity.line.production', 'production_id', 'Capacidad de produccion')
    physicochemical_properties_line_ids = fields.One2many('physicochemical.properties.line.production', 'production_id', 'Propiedades Fisicoquimicas')
    
    @api.onchange('bom_id', 'product_id', 'product_qty', 'product_uom_id')
    def _onchange_move_raw(self):
        if not self.bom_id and not self._origin.product_id:
            return
        # Clear move raws if we are changing the product. In case of creation (self._origin is empty),
        # we need to avoid keeping incorrect lines, so clearing is necessary too.
        if self.product_id != self._origin.product_id:
            self.move_raw_ids = [(5,)]
        if self.bom_id and self.product_qty > 0:
            # keep manual entries
            list_move_raw = [(4, move.id) for move in self.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
            moves_raw_values = self._get_moves_raw_values()
            production_capacity_values = self._get_production_capacity_values()
            physicochemical_properties_values = self._get_physicochemical_properties_values()
            move_raw_dict = {move.bom_line_id.id: move for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)}
            for move_raw_values in moves_raw_values:
                if move_raw_values['bom_line_id'] in move_raw_dict:
                    # update existing entries
                    list_move_raw += [(1, move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
                else:
                    # add new entries
                    list_move_raw += [(0, 0, move_raw_values)]
            self.move_raw_ids = list_move_raw
        else:
            self.move_raw_ids = [(2, move.id) for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)]


    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        source_location = self.location_src_id
        data = {
            'sequence': bom_line.sequence if bom_line else 10,
            'name': self.name,
            'date': self.date_planned_start,
            'date_deadline': self.date_planned_start,
            'bom_line_id': bom_line.id if bom_line else False,
            'picking_type_id': self.picking_type_id.id,
            'product_id': product_id.id,
            'product_uom_qty': product_uom_qty,
            'product_uom': product_uom.id,
            'percentage': bom_line.percentage,
            'density': bom_line.density,
            'dough': bom_line.dough,
            'volume': bom_line.volume,
            'location_id': source_location.id,
            'location_dest_id': self.product_id.with_company(self.company_id).property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            'operation_id': operation_id,
            'price_unit': product_id.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self.name,
            'state': 'draft',
            'warehouse_id': source_location.get_warehouse().id,
            'group_id': self.procurement_group_id.id,
            'propagate_cancel': self.propagate_cancel,
        }
        return data
    
    def _get_production_capacity_values(self):
        production_capacity_list = []
        for record in self.bom_id:
            for pro in record.production_capacity_line_ids:
                production_capacity_list.append((0,0,{
                    'production_capacity': pro.production_capacity,
                    'specifies': pro.specifies,
                    'minimum': pro.minimum,
                    'maximun': pro.maximun,
                    'production_id': self.id.origin
                }))
            
            self.production_capacity_line_ids = production_capacity_list
               
                    
    def _get_physicochemical_properties_values(self):
        physicochemical_properties_list = []
        for record in self.bom_id:
            for phy in record.physicochemical_properties_line_ids:
                physicochemical_properties_list.append((0,0,{
                    'physicochemical_properties':phy.physicochemical_properties,
                    'specifies': phy.specifies,
                    'minimum': phy.minimum,
                    'maximun': phy.maximun,
                    'production_id': self.id.origin
                }))
                
            self.physicochemical_properties_line_ids = physicochemical_properties_list
 
            
               
   
            

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    percentage = fields.Float(string="Porcentaje %")
    density = fields.Float(string="Densidad %") 
    volume = fields.Float(string='Volumen')
    dough = fields.Float(string='Masa', digits=(12, 4))



    
class ProductionCapacityLineProduction(models.Model):
    _name = 'production.capacity.line.production'  

    production_capacity = fields.Selection([('reactor_volume', 'Volumen del Reactor'),
                                            ('dilusor_volume', 'Volumen del Dilusor'),
                                            ('storage_volume', 'Volumen del Almacenador'),
                                            ('reactor_capacity', 'Capacidad del Reactor'),
                                            ('dilusor_capacity', 'Capacidad del Dilusor'),
                                            ('storage_cpacity', 'Capacidad del Almacenador'),], string='Capacidad de Produccion')
    # production_capacity = fields.Many2one('production.capacity', string='Capacidad de Produccion')
    specifies = fields.Float('Especifica')
    minimum = fields.Float('Minimo')
    maximun = fields.Float('Maximo')
    production_id = fields.Many2one(
        'mrp.production', 'Parent production',
        index=True, invisible=True)


class PhysicochemicalPropertiesLineProduction(models.Model):
    _name = 'physicochemical.properties.line.production'  
    
    physicochemical_properties = fields.Selection([('density', 'Densidad'),
                                            ('ph', 'Ph'),
                                            ('conductivity', 'Conductividad'),
                                            ('solids', '% Solidos'),
                                            ('concentration_active_compound', 'Concentración de compuesto activo'),
                                            ('viscosity', 'Viscosidad'), 
                                            ], string="Propiedades Fisicoquimicas"
                                           )
    # physicochemical_properties = fields.Many2one('physicochemical.properties', string='Propiedades Fisicoquimicas')
    specifies = fields.Float('Especifica')
    minimum = fields.Float('Minimo')
    maximun = fields.Float('Maximo')
    production_id = fields.Many2one(
        'mrp.production', 'Parent production',
        index=True, invisible=True)
    
    
    