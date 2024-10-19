# Import the Canvas class
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://byui.instructure.com"
# Canvas API key
API_KEY = "10706~z3LhXDKeVMLMXv2XhHMVCFJeN9NGZMytLMMKPWxZz8aDyvWLYTRWmRNJURGrT7K9"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

current_teacher = canvas.get_courses(enrollment_state = 'active', enrollment_type = 'teacher' )
courses_ta = canvas.get_courses(enrollment_state = 'active', enrollment_type = 'ta' )

for student in courses_ta[0].get_users(enrollment_type=['student']):
    print(f"{student.short_name} | {student.email} | {courses_ta[0].course_code.replace(" ", "")}{student.email[:3]}!")
    #print(student.__dict__)
