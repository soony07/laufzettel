from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask import render_template_string
import requests
import json
import re
import os
import time
from flask import make_response
#from flask_weasyprint import HTML, render_pdf
#from weasyprint import default_url_fetcher, HTML, CSS

import urllib.parse


getbarcode = Blueprint("getbarcode", __name__)

@getbarcode.route('/getbarcode', methods=['GET', 'POST'])
def my_form_post():
    jsonData = (send_request())
   #css = CSS(string='@page { size: A2; margin: 1cm }')
    fields = call_fields(jsonData)
    #content = render_template("getbarcode.html", fields=fields)
    #HTML(string=render_template("getbarcode.html", fields=fields)).write_pdf("report.pdf",stylesheets=[CSS(string='/static/css/index.css')])
    return render_template("getbarcode.html", fields=fields)

def call_fields(jsonData):

    titel = ""
    autor = ""
    call_number=""
    barcode=""
    public_note=""
    inventory_number=""
    alternative_call_number=""
    internal_note_1=""
    requested=""
    po_line=""
    ac=""

    fields = []
    i = 0
    for i in range(1):

        try:
            titel = (jsonData['bib_data']['title'])
        except KeyError:
            pass

        try:
            ac = (jsonData['bib_data']['network_number'])
        except KeyError:
            pass

        try:
            autor = (jsonData['bib_data']['author'])
        except KeyError:
            pass

        try:
            call_number = (jsonData['holding_data']['accession_number'])
        except KeyError:
            pass

        try:
            barcode = (jsonData['item_data']['barcode'])
        except KeyError:
            pass

        try:
            po_line = (jsonData['item_data']['po_line'])
        except KeyError:
            pass

        try:
            public_note = (jsonData['item_data']['public_note'])
        except KeyError:
            pass


        try:
            inventory_number = (jsonData['item_data']['inventory_number'])
        except KeyError:
            pass

        try:
            alternative_call_number = (jsonData['item_data']['alternative_call_number'])
        except KeyError:
            pass

        try:
            internal_note_1 = (jsonData['item_data']['internal_note_1'])
        except KeyError:
            pass

        try:
            requested = (jsonData['item_data']['requested'])
        except KeyError:
            pass


        po_request = get_pol_nr(po_line)

        print(po_request)
        check = '(AT-OBV)'
        print("The original list : " + str(ac))

        res = [idx for idx in ac if idx.lower().startswith(check.lower())]
        print('This is AC:' + str(res))

        ac_nr = str(res).strip('[]')
        print('this is ac string:' + ac_nr)

        print(barcode)
        print(type(barcode))
        if barcode.startswith('+L'):
            print('true')
            barcode=barcode
        else:
            barcode=""
            print('false')

       # if re.match(r'^+L', barcode):
        #   barcode = barcode
        #else:
         #   barcode=""

        print('this is signature' + call_number)
        fields.append({"titel" : titel, "ac" : ac_nr, "autor" : autor, "call_number" : call_number, "barcode" : barcode, "public_note" : public_note, "inventory_number" : inventory_number,  "alternative_call_number" : alternative_call_number, "internal_note_1" : internal_note_1, "requested" : requested, "po_request" : po_request })
        i += 1
    return fields

def send_request():


    session['search'] = request.form["search"]
    barcode = session['search']
    test = urllib.parse.quote(barcode)
    print(test)
    key = 'xxxxxxxxxxxxxxxxxxxxx'
    hed = {'Accept': 'application/json;charset=UTF-8'}
    url = 'https://xxxxxxxxxxxxxxxx.xxxx/almaws/v1/items?item_barcode='+test+'&apikey='+key+'&format=json'
    print(url)
    response = requests.get(url, headers = hed)
    jsonData = response.json()
   # print(jsonData)
    return jsonData



def get_pol_nr(po_line):
    print(po_line)

    key = 'xxxxxxxxxxxxxxxxxxxx'
    hed = {'Accept': 'application/json;charset=UTF-8'}
    url = 'https://xxxxxxxxxxxxxx/almaws/v1/acq/po-lines/'+po_line+'?apikey='+key+'&format=json'
    print(url)
    response = requests.get(url, headers = hed)
    po_line_json = response.json()
    #print(po_line_json)
    fund_code_value=""
    fund_code_desc=""
    vendor_note=""
    po_request = []

    i = 0
    for i in range(1):
        try:
            fund_code_value = po_line_json['fund_distribution'][0]['fund_code']['value']
        except KeyError:
            pass

        try:
            fund_code_desc = po_line_json['fund_distribution'][0]['fund_code']['desc']
        except KeyError:
            pass
        try:
            vendor_note = po_line_json['vendor_note']
        except KeyError:
            pass

        po_request.append({"fund_code_value":fund_code_value, "vendor_note" : vendor_note, "fund_code_desc" :fund_code_desc  })
        i += 1

    return po_request
