# This solution is in the case when it's not necesarry to unlink and save the reference
# and change the status in class lead
# ALDO NERIO
# REQUEST
# http:///localhost:8069/api/contact
# {
#  "name": "ALDO TEST",
#  "email": "prueba_aldo@example.com",
#  "phone": "123456789"
# }
from odoo import http
from odoo.http import request
import json
from werkzeug.exceptions import Unauthorized

class ContactController(http.Controller):

    @http.route('/api/contact', type='json', auth='public', methods=['POST'], csrf=False)
    def api_contact(self, **kwargs):
        contact_data = request.jsonrequest
        name_data = contact_data.get('name', None)
        if not name_data:
            raise Unauthorized("Dont have name, please write a name!!!")
        contact = self.verify_contact(contact_data)
        if contact:
            return {"name": contact.name, "message": "Contat Already Register!!!"}
        lead_obj = self._verify_lead(contact_data)
        if lead_obj:
            contact = self.convert_lead_to_contact(contact_data, lead_obj)
            return {"name": contact.name, "message": "Contat Register!!!"}
        new_contact = self.create_contact(contact_data)
        return {"name": contact.name, "message": "Contat Register!!!"}

    def verify_contact(self, contact_data):
        email_data = contact_data.get('email', None)
        if email_data:
            partner_email = self._search_contact([('email', '=', email_data)])
            if partner_email:
                return partner_email
        phone_data = contact_data.get('phone', None)
        if phone_data:
            partner_phone = self._search_contact([('phone', '=', phone_data)])
            if partner_email:
                return partner_phone
        return False

    def _search_contact(self, search):
        partner_obj = request.env['res.partner'].sudo()
        partner = partner_obj.search(search)
        return partner

    def create_contact(self, contact_data):
        partner_obj = request.env['res.partner'].sudo()
        vals_list = self._contact_list_data(contact_data)
        contact = partner_obj.sudo().create(vals_list)
        return contact

    def _contact_list_data(self, contact_data):
        vals_list = [{
            'name': contact_data.get('name', None),
            'email': contact_data.get('email', None),
            'phone': contact_data.get('phone', None),
            'country_id': 146,
            'company_id': 1,
            'customer_rank': 1,
            'property_product_pricelist': 1,
            'cfdi_usage': '3',
            'category_id': [(6, 0, [3])],
            'zip': 12345,
            'vat': 'XAXX010101000',
            'property_account_receivable_id': 1786,
            'property_account_payable_id': 1890,
            'l10n_mx_edi_fiscal_regime': '601'
        }]
        return vals_list

    def _verify_lead(self, contact_data):
        lead_obj = request.env['res.lead'].sudo()
        lead_name = contact_data.get('name', None)
        if lead_name:
            lead_search = lead_obj.search([('name', '=', lead_name)])
            return lead_search
        return False

    def convert_lead_to_contact(self, contact_data, lead):
        new_contact = self.create_contact(contact_data)
        lead.update({'state': 'inactive', 'contact_id': new_contact.id})
        return new_contact
