print ('iniciando')
from flask import Flask;print ('flask')
from flask import request;print ('request')
import pickle;print ('pickle')
import os;print ('os')
import sklearn;print ('sklearn')
import json;print ('json')
import numpy as np;print('numpy')

app = Flask(__name__)

with open (os.path.join(os.getcwd(), 'kmeans_model.pkl'),'rb') as picklefile:
    model = pickle.load(picklefile)

with open (os.path.join(os.getcwd(), 'standard_scaler_3col.pkl'),'rb') as picklefile:
    sc = pickle.load(picklefile)

with open (os.path.join(os.getcwd(), 'label_encode_3col.json'),'r') as jsonfile:
    le = json.load(jsonfile)
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
    dict_params.update({'gender':request.args.get('gender').lower()})
    dict_params.update({'age':request.args.get('age').lower()})
    dict_params.update({'income':request.args.get('income').lower()})
    list_params = transform_input(dict_params)
    print (list_params)
    scaled_params = scale_input(list_params)
    print (scaled_params)
    output = predict(scaled_params)
    print ('output',output)
    return str(output[0])

if __name__ == '__main__':
    app.run(port=8080)