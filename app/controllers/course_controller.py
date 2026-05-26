from app.config import db
from app.models.course_model import Course


def create_course(data):
    if not data:
        return {"error": "no data provided"}, 400
    if not data.get("course_title"):
        return {"error": "course_title is required"}, 400

    existing_course_title = Course.query.filter_by(
        course_title=data["course_title"]
    ).first()
    if existing_course_title:
        return {"error": "course_title is exists"}, 400

    if not data.get("course_fee"):
        return {"error": "course_fee is required"}, 400
    if float(data["course_fee"]) <= 0:
        return {"error": "course_fee must be positive number"}, 400

    if not data.get("duration_months"):
        return {"error": "duration_months is required"}, 400
    if int(data["duration_months"]) <= 0:
        return {"error": "duration_months must be positive integer"}, 400

    course = Course(
        course_title=data["course_title"],
        course_fee=data["course_fee"],
        duration_months=data["duration_months"],
        description=data.get("description"),
        is_available=data.get("is_available", True),
    )

    db.session.add(course)
    db.session.commit()

    return {"message": "Course created successfully"}, 201


def get_courses():
    courses = Course.query.all()
    if not courses:
        return {"message": "No courses found"}, 404

    course_list = []
    for course in courses:
        course_list.append(
            {
                "id": course.id,
                "course_title": course.course_title,
                "course_fee": course.course_fee,
                "duration_months": course.duration_months,
                "description": course.description,
                "is_available": course.is_available,
                "created_at": course.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return course_list, 200


def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return {"error": "Course not found."}, 404

    return {
        "id": course.id,
        "course_title": course.course_title,
        "course_fee": course.course_fee,
        "duration_months": course.duration_months,
        "description": course.description,
        "is_available": course.is_available,
        "created_at": course.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }, 200


def update_course(course_id, data):
    course = Course.query.get(course_id)
    if not course:
        return {"error": "Course not found."}, 404

    if not data:
        return {"error": "No data provided."}, 400

    if "course_title" in data:
        existing_course = Course.query.filter(
            Course.course_title == data["course_title"], Course.id != course_id
        ).first()
        if existing_course:
            return {"error": "Course title already exists."}, 409

    if "course_fee" in data and float(data["course_fee"]) <= 0:
        return {"error": "Course fee must be a positive number."}, 400

    if "duration_months" in data and int(data["duration_months"]) <= 0:
        return {"error": "Duration months must be a positive integer."}, 400

    if "course_title" in data:
        course.course_title = data["course_title"]
    if "course_fee" in data:
        course.course_fee = data["course_fee"]
    if "duration_months" in data:
        course.duration_months = data["duration_months"]
    if "description" in data:
        course.description = data["description"]
    if "is_available" in data:
        course.is_available = data["is_available"]

    db.session.commit()
    return {"message": "Course updated successfully."}, 200


def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return {"error": "Course not found."}, 404

    db.session.delete(course)
    db.session.commit()
    return {"message": "Course deleted successfully."}, 200
