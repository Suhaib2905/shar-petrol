from odoo import models, fields, api, _
import time

class Gasoline(models.Model):
    _name = 'gasoline'

    shift = [('morning', 'Morning Shift'), ('night', 'Night Shift')]
    state_ = [('draft', 'Draft'), ('done', 'Done')]

    # @api.one
    # @api.depends('gasoline_lines_ids.cash', 'gasoline_lines_ids.credit')
    def _compute_total(self):
     self.total_cash = sum(line.cash for line in self.gasoline_lines_ids)
     self.total_credit = sum(line.credit for line in self.gasoline_lines_ids)
     self.sub_total = self.total_cash + self.total_credit
     self.difference = self.close_meter_reading - self.open_meter_reading
    name = fields.Char(string="Name")
    station = fields.Many2one('gasoline.station', string="Station")
    date = fields.Datetime("Date", default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    duty_shift = fields.Selection(string="Duty Shift", selection=shift)
    pump = fields.Integer(string="Pump")
    fuel_product_id = fields.Many2one('product.product', string="Fuel")
    employee = fields.Many2one('hr.employee', string="Employee")
    open_meter_reading = fields.Integer(string="Open Meter Reading")
    close_meter_reading = fields.Integer(string="Close Meter Reading")
    state = fields.Selection(selection=state_)
    difference = fields.Integer(string="Difference")
    unit_price = fields.Float(string="Unit Price")
    total_price = fields.Float(string="Total Price")
    ltr = fields.Float(string="Ltr")
    ltr_cash = fields.Float(string="Cash")
    ltr_credit = fields.Float(string="Credit")
    ltr_total = fields.Float(string="Total")
    ltr_total_amount = fields.Float(string="Total Amount")
  
    
    gasoline_lines_ids = fields.One2many('gasoline.lines', 'gasoline_id', string="Pumps")
    total_cash = fields.Float(string="Cash", readonly=True, store=True,deafult=0.00, compute="_compute_total")
    total_credit = fields.Float(string="Credit", readonly=True, store=True,deafult=0.00, compute="_compute_total")
    sub_total = fields.Float(string="Sub Total", readonly=True, store=True, default=0.00, compute="_compute_total")

    @api.onchange('fuel_product_id')
    def _fuel_product(self):
        self.unit_price = self.fuel_product_id.list_price
        
class GasolineLines(models.Model):
    _name = 'gasoline.lines'

    cash_credit = [('cash', 'Cash'), ('credit', 'Credit')]

    ltr = fields.Float(string="Ltr")
    ltr_cash_credit = fields.Selection(selection=cash_credit)
    ltr_unit_price = fields.Float(string="Unit Price")
    ltr_total_amount = fields.Float(string="Total Amount")
    gasoline_id = fields.Many2one('gasoline', string="Gasoline")


class GasolineStation(models.Model):
    _name = 'gasoline.station'

    name = fields.Char(string='Name')
    pumps_ids = fields.One2many('gasoline.station.pumps', 'station_id', string="Pumps")
    cash_account_id = fields.Many2one('account.account', string="Cash Account")
    credit_account_id = fields.Many2one('account.account', string="Credit Account")

class GasolineStationPumps(models.Model):
    _name = 'gasoline.station.pumps'

    name = fields.Char(string="Name")
    station_id = fields.Many2one('gasoline.station', string="Station")
