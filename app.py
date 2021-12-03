from flask import Flask, json,render_template,request,jsonify,json
import numpy as np
import pandas as pd

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict",methods=['POST'])
def predict():
    body=request.get_json()
    df=pd.DataFrame.from_dict(body)
    X_train=pd.read_csv('X_train.csv')
    df.fillna(X_train.mean(),axis=0,inplace=True)
    X_test=df.values
    print(df.isnull().sum())
    print(X_test)
    return jsonify({"Message":"Recieved"})

@app.route("/data")
def get_data():
    column=request.args.get('column')
    print(column)
    X=pd.read_csv('X_train.csv')
    y=pd.read_csv('y_train.csv')
    data=np.concatenate((X[column].values.reshape(-1,1),y['price'].values.reshape(-1,1)),axis=1)
    print(data[:5,:])
    grouped_data=[[ntype(a),int(data[data[:,0]==a,1].mean())] for a in np.unique(data[:,0])]
    z=pd.DataFrame(grouped_data,columns=[column,'price']).to_json()
    print(type(z))
    return jsonify(grouped_data)

def ntype(a):
    if type(a)==np.int64:
        return int(a)
    return a

# To switch on debug mode
# set FLASK_ENV=development