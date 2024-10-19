'''
You will need to install the following api's:
    - flask
    - canvasapi
'''


#import the necessary api's and libraries
from flask import Flask, jsonify
from canvasapi import Canvas
import json

# Flask app initialization
app = Flask(__name__)

# Canvas API URL
API_URL = "https://byui.instructure.com"
# Canvas API key
API_KEY = "10706~z3LhXDKeVMLMXv2XhHMVCFJeN9NGZMytLMMKPWxZz8aDyvWLYTRWmRNJURGrT7K9"

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

    # Save the JSON output to a file (optional)
    output_file_name = "courses_list.json"
    with open(output_file_name, 'w') as json_file:
        json.dump(all_courses, json_file, indent=4)

    # Return the JSON data as a response
    return jsonify(all_courses)

if __name__ == '__main__':
    app.run(debug=True)
