from datetime import datetime

from app.config import db
from app.models.student_model import Student


def create_student(data):
    if not data:
        return {"error": "NO data provided"}, 400
    if not data.get("full_name"):
        return {"error": "Full name is required"}, 400
    if not data.get("email"):
        return {"error": "Email is required"}, 400

    existing_email = Student.query.filter_by(email=data["email"]).first()
    if existing_email:
        return {"error": "Email is already exists"}, 400

    if not data.get("age"):
        return {"error": "Age is required"}, 400
    if int(data["age"]) <= 0:
        return {"error": "age want to be positive integer"}, 400

    if not data.get("joined_date"):
        return {"error": "joined date is required"}, 400

    student = Student(
        full_name=data["full_name"],
        email=data["email"],
        age=data["age"],
        cgpa=data.get("cgpa", 0.0),
        is_active=data.get("is_active", True),
        joined_date=datetime.strptime(data["joined_date"], "%Y-%m-%d").date(),
    )

    db.session.add(student)
    db.session.commit()

    return {"message": "Student created successfully"}, 201


def get_students():
    students = Student.query.all()
    if not students:
        return {"message": "No students found"}, 404

    student_list = []
    for student in students:
        student_list.append(
            {
                "id": student.id,
                "full_name": student.full_name,
                "email": student.email,
                "age": student.age,
                "cgpa": student.cgpa,
                "is_active": student.is_active,
                "joined_date": student.joined_date.strftime("%Y-%m-%d"),
                "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return student_list, 200


def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return {"error": "Student not found"}, 400

    return {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email,
        "age": student.age,
        "cgpa": student.cgpa,
        "is_active": student.is_active,
        "joined_date": student.joined_date.strftime("%Y-%m-%d"),
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }, 200


def update_student(student_id, data):
    student = Student.query.get(student_id)
    if not student:
        return {"error": "Student not found."}, 404

    if not data:
        return {"error": "No data provided."}, 400

    if "email" in data:
        existing_student = Student.query.filter(
            Student.email == data["email"], Student.id != student_id
        ).first()
        if existing_student:
            return {"error": "Email address already exists."}, 409

    if "age" in data and int(data["age"]) <= 0:
        return {"error": "Age must be a positive integer."}, 400

    if "full_name" in data:
        student.full_name = data["full_name"]
    if "email" in data:
        student.email = data["email"]
    if "age" in data:
        student.age = data["age"]
    if "cgpa" in data:
        student.cgpa = data["cgpa"]
    if "is_active" in data:
        student.is_active = data["is_active"]
    if "joined_date" in data:
        student.joined_date = datetime.strptime(data["joined_date"], "%Y-%m-%d").date()

    db.session.commit()
    return {"message": "Student updated successfully."}, 200


def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return {"error": "Student not found."}, 404

    db.session.delete(student)
    db.session.commit()
    return {"message": "Student deleted successfully."}, 200
