from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin


load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
CORS(app)

db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    home_address = db.Column(db.String(50))
    date_of_birth = db.Column(db.DateTime)
    date_of_employment = db.Column(db.DateTime)


'''
healthcheck route
'''
@app.route('/healthcheck', methods=['GET'])
def healthcheck() -> dict:
    return {'message': 'Healthcheck done!'}, 200


'''
add employee route
'''
@app.route('/employee', methods=['POST'])
def add_employee() -> dict:
    data = request.get_json()

    employee = Employee.query.filter_by(first_name=data['first_name']).first()

    if employee:
        return {'message': 'Employee already exists.'}, 400

    new_employee = Employee(
        public_id=str(uuid.uuid4()),
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        home_address=data['home_address'],
        date_of_birth=data['date_of_birth'],
        date_of_employment=data['date_of_employment']
    )

    db.session.add(new_employee)
    db.session.commit()

    return {'message': 'New employee created!'}, 201

'''
list all employees route
'''
@app.route('/employee', methods=['GET'])
def list_all_employees() -> dict:
    employees = Employee.query.all()

    result = []
    
    for employee in employees:
        employee_data = {}
        employee_data['public_id'] = employee.public_id
        employee_data['first_name'] = employee.first_name
        employee_data['last_name'] = employee.last_name
        employee_data['email'] = employee.email
        employee_data['home_address'] = employee.home_address
        employee_data['date_of_birth'] = employee.date_of_birth
        employee_data['date_of_employment'] = employee.date_of_employment
        result.append(employee_data)

    return {'message': result}, 200


'''
edit employee route
'''
@app.route('/employee/<id>', methods=['PATCH'])
def edit_employee(id: str) -> dict:
    data = request.get_json()

    employee = Employee.query.filter_by(public_id=id).first()

    employee.first_name = data['first_name']
    employee.last_name = data['last_name']
    employee.email = data['email']
    employee.home_address = data['home_address']
    employee.first_name = data['first_name']

    db.session.add(employee)
    db.session.commit()

    return {'message': data}, 202

'''
delete route
'''
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id: str) -> dict:

    employee = Employee.query.filter_by(public_id=id).first()

    db.session.delete(employee)
    db.session.commit()

    return {'message': 'Employee has been deleted'}, 200

if __name__ == '__main__':
    app.run(debug=True)