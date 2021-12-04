from flask import Flask, json,render_template,request,jsonify,json
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict",methods=['POST'])
def predict():
    body=request.get_json()
    df=pd.DataFrame.from_dict(body)
    X_train=pd.read_csv('X_train.csv')
    df.fillna(X_train.mean(),inplace=True)
    price=predict_price(df)
    return jsonify({"Price":round(price,2)})

def set_type(a):
    if type(a)==np.int64:
        return int(a)
    return a

@app.route("/data")
def get_data():
    column=request.args.get('column')
    X=pd.read_csv('X_train.csv')
    y=pd.read_csv('y_train.csv')
    data=np.concatenate((X[column].values.reshape(-1,1),y['price'].values.reshape(-1,1)),axis=1)
    grouped_data=[[set_type(a),int(data[data[:,0]==a,1].mean())] for a in np.unique(data[:,0])]
    return jsonify(grouped_data)

def predict_price(arr):
    arr['fuelType']=arr['fuelType'].map({"diesel":0,"petrol":1,"hybrid":2,"other":3,"electric":4})
    arr['transmission']=arr['transmission'].map({"manual":0,"auto":1,"semi":2})
    X_train=pd.read_csv('X_train.csv')
    X_train.drop(columns=['carID','model'],axis=1,inplace=True)
    X_train=X_train.values
    arr=arr.values
    sc=StandardScaler()
    X_train[:,3]=sc.fit_transform(X_train[:,3].reshape(-1,1)).flatten()
    arr[:,3]=sc.transform(arr[:,3].reshape(-1,1)).flatten()
    ct=ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[0])],remainder='passthrough')
    ct.fit(X_train)
    arr=np.array(ct.transform(arr))
    with open('model.joblib','rb') as f:
        model=joblib.load(f)
    price=model.predict(arr)
    return price[0]


# To switch on debug mode
# set FLASK_ENV=development