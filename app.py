import pickle
import flask 

from flask import Flask, request
app = Flask(__name__)

# loading the ml model
model_pickle = open("./classifier.pkl","rb")
clf = pickle.load(model_pickle)

# decorator 1st 
@app.route("/ping", methods=["GET"])
def ping():
    return {"message": "Pinging the model successful !!!"}

# 2nd
@app.route("/predict", methods = ["POST"])
def prediction():
    loan_req = request.get_json()   # loan_req: dict

    if loan_req['Gender'] == "Male":
        gender = 0
    else:
        gender = 1
    
    if loan_req['Married'] == "Unmarried":
        marital_status = 0
    else:
        marital_status = 1

    if loan_req['Credit_History'] == "Uncleared Debts":
        credit_history = 0
    else:
        credit_history = 1
    

    applicant_income = loan_req['ApplicantIncome']
    loan_amt =  loan_req['LoanAmount']/1000


    input_data = [[gender, marital_status, applicant_income, loan_amt, credit_history]]

    # generate inference
    prediction = clf.predict(input_data)

    if prediction == 0:
        pred = "Rejected"
    else:
        pred = "Approved"
    
    return {"loan_approval_status" : pred}

# 3rd method
@app.route("/get_params", methods=["GET"])
def get_application_params():
    parameters = {
        "Gender" : "<Male/Female>",
        "Married" : "<Unmarried/Married>",
        "ApplicantIncome" : 500000000,
        "LoanAmount" : 5000,
        "Credit_History" : "<Cleared Debts/ Uncleared Debts>"
        }
