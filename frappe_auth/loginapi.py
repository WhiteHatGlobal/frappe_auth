# Copyright (c) 2022, White Hat Global and contributors
# For license information, please see license.txt
# 
from __future__ import unicode_literals
import frappe
from frappe import auth
import json
from frappe.utils import floor, flt, today, cint
from frappe import _

@frappe.whitelist( allow_guest=True )
def login(usr, pwd):
    # if frappe.request.data:
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key": 0,
            "error": {
                "code": 401,
                "message":"Invalid Username / Password"
            },
            "data": {}
            
        }
        return #True


    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)

    frappe.response["message"] = {
        "success": 1,
        "error": {
            "code": 200,
            "message": "Authentication Success"
        },
        "data": {
            "sid": frappe.session.sid,
            "api_key":user.api_key,
            "api_secret":api_generate,
            "username":user.username,
            "email":user.email,
            "user_image":user.user_image,
            "roles":user.roles
        }
    }

def generate_keys(user):
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key

    user_details.api_secret = api_secret
    user_details.save()

    return api_secret