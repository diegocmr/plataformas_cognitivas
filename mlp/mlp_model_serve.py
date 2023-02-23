print ('iniciando')
from flask import Flask;print ('flask')
from flask import request;print ('request')
import pickle;print ('pickle')
import os;print ('os')
import sklearn;print ('sklearn')
import json;print ('json')
import numpy as np;print('numpy')

app = Flask(__name__)

with open (os.path.join(os.getcwd(), 'mlp_model.pkl'),'rb') as picklefile:
    model = pickle.load(picklefile)

with open (os.path.join(os.getcwd(), 'standard_scaler_15col.pkl'),'rb') as picklefile:
    sc = pickle.load(picklefile)

with open (os.path.join(os.getcwd(), 'label_encode_15col.json'),'r') as jsonfile:
    for f in jsonfile:
        lowerfile = f.lower()
    le = json.loads(lowerfile)
    le = {key.lower():value for key, value in le.items()}

with open (os.path.join(os.getcwd(), 'datatypes.json'),'r') as jsonfile:
    datatypes = json.load(jsonfile)
    datatypes = {key.lower():value for key, value in datatypes.items()}
    
def transform_input(dict_params):
    print ('iniciando transformação dos inputs', dict_params)
    le_list_params = []
    for param in dict_params: #transformando datatypes
        if datatypes[param] == 'object':
            le_list_params.append(le[param][dict_params[param]])
        elif datatypes[param] == 'int64':
            le_list_params.append(np.int64(dict_params[param]))
        elif datatypes[param] == 'float64':
            le_list_params.append(np.float64(dict_params[param]))
    return [le_list_params] #retornando matriz com representação numérica do dado

def scale_input(list_params):
    return (sc.transform(list_params))

def predict(scaled_params):
    return model.predict(scaled_params)

@app.route("/")
def model_serve():
    dict_params = {}

    dict_params.update({'loan_limit':request.args.get('loan_limit').lower()})
    dict_params.update({'gender':request.args.get('gender').lower()})
    dict_params.update({'approv_in_adv':request.args.get('approv_in_adv').lower()})
    dict_params.update({'loan_type':request.args.get('loan_type').lower()})
    dict_params.update({'loan_purpose':request.args.get('loan_purpose').lower()})
    dict_params.update({'loan_amount':request.args.get('loan_amount').lower()})
    dict_params.update({'rate_of_interest':request.args.get('rate_of_interest').lower()})
    dict_params.update({'lump_sum_payment':request.args.get('lump_sum_payment').lower()})
    dict_params.update({'property_value':request.args.get('property_value').lower()})
    dict_params.update({'construction_type':request.args.get('construction_type').lower()})
    dict_params.update({'occupancy_type':request.args.get('occupancy_type').lower()})
    dict_params.update({'total_units':request.args.get('total_units').lower()})
    dict_params.update({'income':request.args.get('income').lower()})
    dict_params.update({'credit_type':request.args.get('credit_type').lower()})
    dict_params.update({'age':request.args.get('age').lower()})

    print (dict_params)

    list_params = transform_input(dict_params)
    print (list_params)
    scaled_params = scale_input(list_params)
    print (scaled_params)
    output = predict(scaled_params)
    print ('output',output)
    return str(output[0])

if __name__ == '__main__':
    app.run(port=3000)