
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            balance=float(request.form['balance'])
            c_age=int(request.form['age'])
            if c_age<=24:
                client_age=1
            if (c_age>24 & c_age <=35):
                client_age=2
            if (c_age>=36 & c_age<=64):
                client_age=3
            if c_age>=65:
                client_age=4
            district_id = int(request.form['district_id'])
            c_sex=request.form['client_sex']
            if (c_sex=='M'):
                client_sex=1
            if (c_sex=='F'):
                client_sex=0
            freq = request.form['frequency']
            if(freq=='MI'):
                frequency_MI=1
                frequency_TI=0
                frequency_WI=0
            if(freq=='WI'):
                frequency_MI=0
                frequency_TI=0
                frequency_WI=1
            if(freq=='TI'):
                frequency_MI=0
                frequency_TI=1
                frequency_WI=0
            c_type = request.form['ctype']
            if(c_type=='J'):
                type_x_classic=0
                type_x_gold=0
                type_x_junior=1
            if(c_type=='C'):
                type_x_classic=1
                type_x_gold=0
                type_x_junior=0
            if(c_type=='G'):
                type_x_classic=0
                type_x_gold=1
                type_x_junior=0
            filename = 'final_model.pkl'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict([[client_age,district_id,client_sex,balance,frequency_MI,frequency_TI,frequency_WI,type_x_classic,type_x_gold,type_x_junior]])
            print('prediction is', prediction)
            if prediction[0]==1:
                prediction="GOOD"
            else:
                prediction="BAD"
            # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction) 
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')
if __name__ == "__main__":
	app.run(debug=True) # running the app