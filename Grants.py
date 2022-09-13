import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import timedelta, date
import requests
load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_ENDPOINT = os.environ.get('DB_ENDPOINT')

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_ENDPOINT}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

household_url = "http://localhost:5000/getAllHouseholds"

db = SQLAlchemy(app)

class GrantSchemes(db.Model):
    __tablename__ = 'grant_schemes'
    
    grant_name = db.Column(db.String(100), primary_key=True, nullable=False)
    criteria = db.Column(db.String(200), nullable=False)
    qualifying_members = db.Column(db.String(200), nullable=False)
    
    def __init__(self,grant_name,criteria,qualifying_members):
        self.grant_name = grant_name
        self.criteria = criteria
        self.qualifying_members = qualifying_members
        
    def get_list_of_criteria(self):
        # Gets a list of criteria, where each criteria is a tuple: (ATTRIBUTE,OPERATOR,VALUE)
        criteria_list = self.criteria.split(",")
        criteria_return_list = []
        for criteria in criteria_list:
            attribute = ""
            operator = ""
            value = ""
            for ch in criteria:
                if ch not in "><=" and operator == "":
                    attribute += ch
                elif ch in "><=":
                    operator += ch
                else:
                    value += ch
            
            criteria_return_list.append((attribute,operator,value))
            
        return criteria_return_list
    
    def get_member_qualifier(self):
        attribute = ""
        operator = ""
        value = ""
        for ch in self.qualifying_members:
            if ch not in "><=" and operator == "":
                attribute += ch
            elif ch in "><=":
                operator += ch
            else:
                value += ch
            
        return (attribute,operator,value)
    
# Helper Function to process operations with ambiguous operators
def perform_operation(left_operand,operator,right_operand):
    if operator == ">":
        return left_operand > right_operand
    elif operator == ">=":
        return left_operand >= right_operand
    elif operator == "<":
        return left_operand < right_operand
    elif operator == "<=":
        return left_operand <= right_operand
    elif operator == "==":
        return left_operand == right_operand

# Helper Function to calculate age
def get_age(date_of_birth):
    date_of_birth_list = date_of_birth.split("-")
    birth_year = int(date_of_birth_list[0])
    birth_month = int(date_of_birth_list[1])
    birth_day = int(date_of_birth_list[2])
    today = date.today()
    return today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))

@app.route("/getHouseholdsOfGrant", methods=["GET"])
def get_households_of_grant():
    input_ans = request.get_json()
    try:
        grant_name = input_ans['grant_name']
        # Getting Grant Details
        grant_scheme = GrantSchemes.query.filter_by(grant_name=grant_name).first()
        if not grant_scheme:
            # Grant Scheme does not exist
            return jsonify({
                "message": "Grant Scheme does not exist"
            }), 404
        
        criteria_list = grant_scheme.get_list_of_criteria()

        # Calling Household microservice to get households
        households = requests.request("GET",household_url)
        if households.status_code != 200:
            return jsonify({
            "message": "An error occurred while calling Household microservice"
        }), 500
        household_list = households.json()["result"]
        qualifying_households = []
        for household in household_list:
            family_members = household['family_members']
            # Go through criteria
            overall_criteria_met = True
            for criteria in criteria_list:
                if criteria[0] == "MEMBER_AGE":
                    age_met = False
                    for family_member in family_members:
                        if perform_operation(get_age(family_member["date_of_birth"]),criteria[1],int(criteria[2])):
                            age_met = True
                            
                    if not age_met:
                        overall_criteria_met = False
                        break
                    
                elif criteria[0] == "TOTAL_INCOME":
                    total_income = 0
                    for family_member in family_members:
                        total_income += family_member["annual_income"]
                        
                    if not perform_operation(total_income,criteria[1],int(criteria[2])):
                        overall_criteria_met = False
            
            # Overall criteria is met, so now checks for qualifying members
            if overall_criteria_met:
                qualifying_members = []
                member_qualifier_tup = grant_scheme.get_member_qualifier()
                if (member_qualifier_tup[0] == "ALL"):
                    qualifying_members = family_members
                elif (member_qualifier_tup[0] == "AGE"):
                    for family_member in family_members:
                        age = get_age(family_member["date_of_birth"])
                        qualifying_age = int(member_qualifier_tup[2])
                        if perform_operation(age,member_qualifier_tup[1],qualifying_age):
                            qualifying_members.append(family_member)
                            
                qualifying_households.append({"household_type": household["household_type"], "qualifying_family": qualifying_members})
                
        if len(qualifying_households) <= 0:
            return jsonify({
                "message": "No households fulfill this grant scheme"
            }), 404
                
            
        return jsonify({
            "qualified_households": qualifying_households
        }), 200
        
        
        
    except Exception as e:
        return jsonify({
            "message": f"An error occurred while searching for household. {e.args[0]}"
        }), 500
        
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)