from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask import render_template_string
import requests
import json
import re
import os
import time
import urllib.parse 
 

blankoformular = Blueprint("blankoformular", __name__)

@blankoformular.route('/blankoformular', methods=['GET', 'POST'])
def blanko():
    return render_template("blankoformular.html")    
