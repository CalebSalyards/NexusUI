# Import APIs and libraries
from flask import Flask, jsonify, request
from canvasapi import Canvas
import json
import random
import string

# Flask app initialization
app = Flask(__name__)

from flask import send_from_directory

# Add this route in your existing Flask app code
@app.route('/index.html')
def serve_index():
    return send_from_directory('C:/Users/Neil Buffham/Documents/NexusUI/NexusUI/neils_bs', 'index.html')

# If you want to serve the entire directory (optional)
@app.route('/')
def serve_root():
    return send_from_directory('C:/Users/Neil Buffham/Documents/NexusUI/NexusUI/neils_bs', 'index.html')

# Keep the existing routes below...


# Canvas API URL
API_URL = "https://byui.instructure.com"
# Canvas API key
API_KEY = "10706~z3LhXDKeVMLMXv2XhHMVCFJeN9NGZMytLMMKPWxZz8aDyvWLYTRWmRNJURGrT7K9"  # Replace with your actual API key

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

@app.route('/')
def index():
    return "Welcome to the Canvas API. Available endpoints: /api/courses, /api/students"

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

import random
import string

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

    # Use the last three digits of the course ID
    course_id_str = str(course.id)  # Convert course.id to string
    last_three_digits = course_id_str[-3:]  # Get the last three characters

    # Get users in the course
    users = course.get_users(enrollment_type=['student'])  # Retrieve students only

    student_list = []
    for user in users:
        # Extract last name from the full name
        last_name = user.name.split()[-1][:5]  # Get the last word as last name, limit to 5 characters

        # Generate a random string of 3 alphanumeric characters
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=3))

        # Create the student entry with available user attributes
        student_entry = {
            'preferred_name': user.name,  # Full name
            'email': user.email if hasattr(user, 'email') else 'N/A',  # Email
            'identifier': f"{last_three_digits}{last_name}{random_string}"  # Unique identifier
        }
        student_list.append(student_entry)

    # Return the student data as JSON
    return jsonify(student_list)



if __name__ == '__main__':
    app.run(debug=True)
