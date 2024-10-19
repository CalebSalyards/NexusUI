const signedIn = false;
const signInButton = document.getElementById('sign-in');
const url = 'Something should be here maybe';
const courses = 'find out what the courses page is';


async function signInCheck(signedIn) {
    if (signedIn) {
        signInButton.style.display = 'none';
    }
};

signInCheck(signedIn);

async function generateCourses() {
    const main = document.getElementById('mainPage');
    const coursesList = document.createElement('ul');
    main.append(coursesList)
    forEach((url.courses), () => {
        const courseSection = document.createElement('section');
        coursesList.append(courseSection);
    })
};


async function getStudentNames() {
    const main = document.getElementById('mainPage');
    const studentList = document.createElement('ul');
    main.append(studentList)
    forEach((url.courses), () => {
        const studentSection = document.createElement('section');
        studentList.append(studentSection);
    })
}

async function getStuff(params) {

    fetch('/api/courses')
        .then(response => response.json())
        .then(data => {
            const courseListDiv = document.getElementById('course-list');
            data.forEach(course => {
                const courseItem = document.createElement('div');
                courseItem.textContent = `${course.course_code}: ${course.course_name}`;
                courseListDiv.appendChild(courseItem);
            });
        })
        .catch(error => console.error('Error fetching course data:', error));
}