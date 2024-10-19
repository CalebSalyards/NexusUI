'''
You will need to install the following api's:
    - flask
    - canvasapi
'''


#import api's and libraries
from flask import Flask, jsonify, request
from canvasapi import Canvas
import json
import random
import string

# Flask app initialization
app = Flask(__name__)

# Canvas API URL
API_URL = "https://byui.instructure.com"
# Canvas API key
API_KEY = "YOUR_API_KEY_HERE10706~z3LhXDKeVMLMXv2XhHMVCFJeN9NGZMytLMMKPWxZz8aDyvWLYTRWmRNJURGrT7K9"  # Replace with your actual API key

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

@app.route('/api/courses', methods=['GET'])
def get_courses():
    # Get current teacher's courses
    current_teacher_courses = canvas.get_courses(enrollment_state='active', enrollment_type='teacher')

    # Get current TA's courses
    current_ta_courses = canvas.get_courses(enrollment_state='active', enrollment_type='ta')

    # Create a list to hold all courses
    all_courses = []

    # Append courses to the list
    for course in current_teacher_courses:
        all_courses.append({
            'course_id': course.id,
            'course_name': course.name,
            'course_code': course.course_code
        })

    for course in current_ta_courses:
        all_courses.append({
            'course_id': course.id,
            'course_name': course.name,
            'course_code': course.course_code
        })

    # Return the JSON data as a response
    return jsonify(all_courses)

@app.route('/api/students', methods=['POST'])
def get_students_by_course_code():
    # Get the course code from the request
    data = request.get_json()
    course_code = data.get('course_code')

    # Find the course by code
    courses = canvas.get_courses(enrollment_state='active')
    course = next((c for c in courses if c.course_code == course_code), None)

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    # Get students in the course
    students = course.get_students()

    student_list = []
    for student in students:
        # Generate a random string of 4 alphanumeric characters
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))

        # Create the desired format
        student_entry = {
            'preferred_name': student.name,
            'email': student.email,
            'identifier': f"{course_code}{student.first_name}{random_string}"
        }
        student_list.append(student_entry)

    # Return the student data as JSON
    return jsonify(student_list)

if __name__ == '__main__':
    app.run(debug=True)