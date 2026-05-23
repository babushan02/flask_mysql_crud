from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:root123@localhost/flask_mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Student(db.Model):
    __tablename__='students'

    id=db.Column(db.Integer, primary_key=True)
    full_name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(120), nullable=False, unique=True)
    age=db.Column(db.Integer, nullable=False)
    cgpa=db.Column(db.Float, default=0.0)
    is_active=db.Column(db.Boolean, default=True)
    joined_date=db.Column(db.Date, nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    __tablename__='courses'

    id=db.Column(db.Integer, primary_key=True)
    course_title=db.Column(db.String(100), nullable=False, unique=True)
    course_fee=db.Column(db.Float, nullable=False)
    duration_months=db.Column(db.Integer, nullable=False)
    description=db.Column(db.Text, nullable=True)
    is_available=db.Column(db.Boolean, default=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

##---------------- POST students --------------------##    

@app.route('/api/students', methods=['POST']) 
def create_student():
    try:
        data=request.get_json()

        if not data:
            return jsonify({'error': 'NO data provided'}),400
        if not data.get('full_name'):
            return jsonify({'error': 'Full name id required'}),400
        
        ##================Email test ===================##

        if not data.get('email'):
            return jsonify({'error': 'Email is required'}),400
        existing_email= Student.query.filter_by(
            email=data['email']
        ).first()
        if existing_email:
            return jsonify({'error': 'Email is already exists'}),400
        
        ##================Age test ===================##

        if not data.get('age'):
            return jsonify({'error': 'Age is required'}),400
        if int(data['age'])<=0:
            return jsonify({'error': 'age want to be positive integer'})
        
        if not data.get('joined_date'):
            return jsonify({'error': 'joined date is required'}),400
        student = Student(
            full_name=data['full_name'],
            email=data['email'],
            age=data['data'],
            cgpa=data.get['cgpa', 0.0],
            is_active=data.get('is_active', True), 
            joined_date=datetime.strptime(
                data['joined_date'],
                '%Y-%m-%d'
            ).date()  
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({'message': 'Student created successfully'}),200

    except Exception as e:
        return jsonify({'error' : 'Internal server error',
                        'details': str(e)}),500 
    

       
##--------------- GET (all) students -----------------##   

app.route('/api/students', methods=['GET'])
def get_students():
    try:
        students= Student.query.all()
        student_list=[]

        for student in students:
            student_list.append({
                'id': student.id,
                'full_name': student.full_name,
                'email': student.email,
                'age': student.age,
                'cgpa': student.cgpa,
                'is_active': student.is_active,
                'joined_date': student.joined_date.strftime('%Y-%m-%d'),
                'created_at': student.created_at
            })

        return jsonify(student_list),200
    except Exception as e:
        return jsonify({'error':'Internal server error','details':str(e)})    
 
##--------------- GET (one) student ------------------## 

@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    try:
        student=Student.query.get(id)
        if not student:
            return jsonify({'error': 'Student not found'}),400
        return jsonify({
            'id': student.id,
            'full_name': student.full_name,
            'email': student.email,
            'age': student.age,
            'cgpa': student.cgpa,
            'is_active': student.is_active,
            'joined_date': student.joined_date.strftime('%Y-%m-%d'),
            'created_at': student.created_at            
        })
    except Exception as e:
        return jsonify({'error':'Internal server error','details':str(e)})
    
##-------------------- PUT student ---------------------## 

# @app.route('/api/students/<int:id>', methods=['PUT'])
# def update_student(id):

##-------------------- DELETE student ------------------## 
          
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    try:
        student = Student.query.get(id)

        if not student:
            return jsonify({
                'error': 'Student not found.'
            }), 404

        db.session.delete(student)
        db.session.commit()

        return jsonify({
            'message': 'Student deleted successfully.'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error.',
            'details': str(e)
        }), 500
       
if __name__=='__main__':
    app.run(debug=True)