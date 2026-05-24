from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text

app=Flask(__name__)

app.json.sort_keys = False

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

##---------------- POST students --------------------##    

@app.route('/api/students', methods=['POST']) 
def create_student():
    try:
        data=request.get_json()

        if not data:
            return jsonify({'error': 'NO data provided'}),400
        if not data.get('full_name'):
            return jsonify({'error': 'Full name is required'}),400
        
        ##================Email test ===================##

        if not data.get('email'):
            return jsonify({'error': 'Email is required'}),400
        existing_email= Student.query.filter_by(
            email=data['email']
        ).first()
        if existing_email:
            return jsonify({'error': 'Email is already exists'}),400
        
        ##================Age test ====================##

        if not data.get('age'):
            return jsonify({'error': 'Age is required'}),400
        if int(data['age'])<=0:
            return jsonify({'error': 'age want to be positive integer'}),400
        
        if not data.get('joined_date'):
            return jsonify({'error': 'joined date is required'}),400
        student = Student(
            full_name=data['full_name'],
            email=data['email'],
            age=data['age'],
            cgpa=data.get('cgpa', 0.0),
            is_active=data.get('is_active', True), 
            joined_date=datetime.strptime(
                data['joined_date'],
                '%Y-%m-%d'
            ).date()  
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({'message': 'Student created successfully'}),201

    except Exception as e:
        return jsonify({'error' : 'Internal server error',
                        'details': str(e)}),500 
           
##--------------- GET (all) students -----------------##   

@app.route('/api/students', methods=['GET'])
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
                'created_at': student.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return jsonify(student_list),200
    except Exception as e:
        return jsonify({'error':'Internal server error','details':str(e)}),500    
 
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
            'created_at': student.created_at.strftime('%Y-%m-%d %H:%M:%S')            
        })
    except Exception as e:
        return jsonify({'error':'Internal server error','details':str(e)}),500
    
##-------------------- PUT student ---------------------## 

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):

    try:
        student = Student.query.get(id)

        if not student:
            return jsonify({'error': 'Student not found.'}), 404

        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided.'}), 400

        # EMAIL UNIQUE CHECK
        if 'email' in data:
            existing_student = Student.query.filter(Student.email == data['email'],Student.id != id).first()

            if existing_student:
                return jsonify({'error': 'Email address already exists.'}), 409

        # AGE VALIDATION
        if 'age' in data:
            if int(data['age']) <= 0:
                return jsonify({
                    'error': 'Age must be a positive integer.'
                }), 400

        # UPDATE VALUES
        if 'full_name' in data:
            student.full_name = data['full_name']

        if 'email' in data:
            student.email = data['email']

        if 'age' in data:
            student.age = data['age']

        if 'cgpa' in data:
            student.cgpa = data['cgpa']

        if 'is_active' in data:
            student.is_active = data['is_active']

        if 'joined_date' in data:
            student.joined_date = datetime.strptime(
                data['joined_date'],
                '%Y-%m-%d').date()

        db.session.commit()

        return jsonify({'message': 'Student updated successfully.'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error.','details': str(e)}), 500


##-------------------- DELETE student ------------------## 
          
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    try:
        student = Student.query.get(id)

        if not student:
            return jsonify({'error': 'Student not found.'}), 404
        
        db.session.delete(student)
        db.session.commit()

        return jsonify({'message': 'Student deleted successfully.'}), 200
    except Exception as e:
        return jsonify({
            'error': 'Internal server error.','details': str(e)}), 500
    
#---------------- POST courses --------------------##

@app.route('/api/courses', methods=['POST']) 
def create_course():
    try:
        data=request.get_json()

        if not data:
            return jsonify({'error':'no data provided'}),400
        if not data.get('course_title'):
            return jsonify({'error':'course_title is required'}),400 
        existing_course_title=Course.query.filter_by(course_title=data['course_title']).first()
        if existing_course_title:
            return jsonify({'error':'course_title is exists'}),400
        if not data.get('course_fee'):
            return jsonify({'error':'course_fee is required'}),400
        if float(data['course_fee'])<=0:
            return jsonify ({'error':'course_fee must be positive number'}),400
        if not data.get('duration_months'):
            return jsonify({'error':'duration_months is required'}),400
        if int(data['duration_months'])<=0:
            return jsonify({'error':'duration_months must be positive integer'}),400
        course = Course(
            course_title=data['course_title'],
            course_fee=data['course_fee'],
            duration_months=data['duration_months'],
            description=data.get('description'),
            is_available=data.get('is_available', True)
)
        db.session.add(course)
        db.session.commit()

        return jsonify({'message':'Course created successfully'}),201
    except Exception as e:
        return jsonify({'error':'Internal server error','details':str(e)}),500    

##----------------- Get(all) courses ------------------##
@app.route('/api/courses', methods=['GET'])
def get_courses():
    try:
        courses=Course.query.all()
        course_list=[]
        for course in courses:
            course_list.append({
                'id':course.id,
                'course_title':course.course_title,
                'course_fee':course.course_fee,
                'duration_months':course.duration_months,
                'description':course.description,
                'is_available':course.is_available,
                'created_at':course.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return jsonify(course_list),200
    except Exception as e:
        return jsonify({'error':'Internal server error','details':str(e)}),500        
       
if __name__=='__main__':
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            print('Database connection successfull')
            db.create_all()
    except Exception as e:
        print (f'Database connection failed:{e}')        
    app.run(debug=True, port=2222)