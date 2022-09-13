import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_ENDPOINT = os.environ.get('DB_ENDPOINT')

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_ENDPOINT}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Household(db.Model):
    __tablename__ = 'household'
    
    unit_no = db.Column(db.String(10), primary_key=True, nullable=False)
    housing_type = db.Column(db.String(50), primary_key=True, nullable=False)

    def __init__(self, unit_no, housing_type):
        self.unit_no = unit_no
        self.housing_type = housing_type

    def json(self):
        return {
            "unit_no": self.unit_no,
            "housing_type": self.housing_type
        }
        
class FamilyMember(db.Model):
    __tablename__ = 'family_member'
    
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    marital_status = db.Column(db.String(30), nullable=False)
    spouse_name = db.Column(db.String(50), primary_key=True)
    occupation_type = db.Column(db.String(20), nullable=False)
    annual_income = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.String(30), nullable=False)
    unit_no = db.Column(db.String(10), nullable=False)
    
    def __init__(self,name,gender,marital_status,spouse_name,occupation_type,annual_income,date_of_birth,unit_no):
        self.name = name
        self.gender = gender
        self.marital_status = marital_status
        self.spouse_name = spouse_name
        self.occupation_type = occupation_type
        self.annual_income = annual_income
        self.date_of_birth = date_of_birth
        self.unit_no = unit_no
        
    def json(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "marital_status": self.marital_status,
            "spouse_name": self.spouse_name,
            "occupation_type": self.occupation_type,
            "annual_income": self.annual_income,
            "date_of_birth": self.date_of_birth,
        }
        
        

@app.route("/createHousehold", methods=["POST"])
def insert_into_household():
    input_ans = request.get_json()
    try:
        unit_no = input_ans['unit_no']
        housing_type = input_ans['housing_type']
        row = Household(unit_no,housing_type)
        db.session.add(row)
        db.session.commit()
        return jsonify({
            "message": "New household created!"
        }), 201
    except Exception as e:
        return jsonify({
            "message": f"An error occurred while creating a new household. {e.args[0]}"
        }), 500


@app.route("/addFamilyMember", methods=["POST"])
def add_family_member():
    input_ans = request.get_json()
    try:
        unit_no = input_ans['unit_no']
        # Family Info
        name = input_ans['name']
        gender = input_ans['gender']
        marital_status = input_ans['marital_status']
        spouse_name = input_ans['spouse_name']
        occupation_type = input_ans['occupation_type']
        annual_income = input_ans['annual_income']
        date_of_birth = input_ans['date_of_birth']
        
        row = FamilyMember(name,gender,marital_status,spouse_name,occupation_type,annual_income,date_of_birth,unit_no)
        db.session.add(row)
        db.session.commit()
        return jsonify({
            "message": "Family member has been added to household!"
        }), 201
    except Exception as e:
        return jsonify({
            "message": f"An error occurred while adding a family member. {e.args[0]}"
        }), 500


@app.route("/getAllHouseholds", methods=["GET"])
def get_all_households():
    try:
        households = Household.query.all()
        return_list = []
        for household in households:
            household_dict = {"household_type": household.housing_type, "family_members": []}
            family_members = FamilyMember.query.filter_by(unit_no=household.unit_no)
            for family_member in family_members:
                household_dict["family_members"].append(family_member.json())
            return_list.append(household_dict)
            
        return jsonify({
            "result": return_list
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": f"An error occurred while getting all households. {e.args[0]}"
        }), 500
    

@app.route("/searchHousehold", methods=["GET"])
def search_household():
    input_ans = request.get_json()
    try:
        # Assuming that we are using unit number as the search criteria for household search
        unit_no = input_ans['unit_no']
        household = Household.query.filter_by(unit_no=unit_no).first()
        if not household:
            # Household doesnt exist
            return jsonify({
                "message": "Household does not exist"
            }), 404
        
        family_members = FamilyMember.query.filter_by(unit_no=unit_no)
        return_dict = {"household_type": household.housing_type, "family_members": [] }
        for family_member in family_members:
            return_dict["family_members"].append(family_member.json())
            
        return jsonify({
            "household_type": return_dict["household_type"],
            "family_members": return_dict["family_members"]
        }), 200
    except Exception as e:
        return jsonify({
            "message": f"An error occurred while searching for household. {e.args[0]}"
        }), 500
        
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)