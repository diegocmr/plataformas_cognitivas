print ('iniciando')
from flask import Flask;print ('flask')
from flask import request;print ('flask.request')
import requests;print ('requests')
import os;print ('os')
import json;print ('json')
import numpy as np;print('numpy')

app = Flask(__name__)

def get_url(model,dict_params):
    protocol = 'http://'
    ip_address = '127.0.0.1'
    endpoint = '/predict'
    
    model_port = {'kmeans':'1000','rf':'2000','mlp':'3000'}
    port = model_port[model]
    
    model_params = {
                    'kmeans':['age',  'gender',  'income'],
                    'rf':['loan_limit','gender',
                          'approv_in_adv','loan_type',
                          'loan_purpose','loan_amount',
                          'rate_of_interest','lump_sum_payment',
                          'property_value','construction_type',
                          'occupancy_type','total_units'
                          ,'income','credit_type','age'],
                    'mlp':['loan_limit','gender',
                          'approv_in_adv','loan_type',
                          'loan_purpose','loan_amount',
                          'rate_of_interest','lump_sum_payment',
                          'property_value','construction_type',
                          'occupancy_type','total_units'
                          ,'income','credit_type','age']}
    
    str_post = protocol + ip_address + ':' + port + endpoint + '?'
    i = 0
    for param in range(0, len(model_params[model])):
        str_post = str_post + model_params[model][i] + '=' + dict_params[model_params[model][i]]
        if i != len(model_params[model])-1:
            str_post = str_post + '&'
        i = i+1

    return str_post

@app.route('/')
def front():
    return 'Model Manager' 

@app.route("/route")
def rout_to_model():
    model = request.args.get('model').lower()
    if model not in ['kmeans', 'rf', 'mlp']:
        raise Exception ('modelo inexistente!')

    dict_params = {}

    dict_params.update({'loan_limit':request.args.get('loan_limit')})
    dict_params.update({'gender':request.args.get('gender')})
    dict_params.update({'approv_in_adv':request.args.get('approv_in_adv')})
    dict_params.update({'loan_type':request.args.get('loan_type')})
    dict_params.update({'loan_purpose':request.args.get('loan_purpose')})
    dict_params.update({'loan_amount':request.args.get('loan_amount')})
    dict_params.update({'rate_of_interest':request.args.get('rate_of_interest')})
    dict_params.update({'lump_sum_payment':request.args.get('lump_sum_payment')})
    dict_params.update({'property_value':request.args.get('property_value')})
    dict_params.update({'construction_type':request.args.get('construction_type')})
    dict_params.update({'occupancy_type':request.args.get('occupancy_type')})
    dict_params.update({'total_units':request.args.get('total_units')})
    dict_params.update({'income':request.args.get('income')})
    dict_params.update({'credit_type':request.args.get('credit_type')})
    dict_params.update({'age':request.args.get('age')})

    str_post = get_url(model,dict_params)
    print ('enviando requisição para', str_post)

    req = str(requests.get(str_post).content).replace('b', '').replace("'", '')
    if model == 'mlp':
        req=req.replace('[','').replace(']','')
        if 'e' in req:
            np.set_printoptions(suppress=True)
            num = float(req.split('e')[0])
            exp = int(req.split('e')[1])
            print (num, exp)
            req = str(round(np.power(num,exp),6))

    print (req)

    return req

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80)