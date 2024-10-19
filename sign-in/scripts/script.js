const signedIn = false;
const signInButton = document.getElementById('sign-in');
const url = 'Something should be here maybe';
const courses = 'find out what the courses page is';


async function signInCheck(signedIn) {
    if(signedIn){
        signInButton.style.display = 'none';
    } else{

    }
};

signInCheck(signedIn)

async function generateCourses(){
    const main = document.getElementById('mainPage');
    const coursesList = document.createElement('ul');
    main.appendChild(coursesList)
    forEach((url.courses), () => {
        if(url.courses.role == 'teacher' || url.courses.role == 'TA'){
            const courseSection = document.createElement('section');
            coursesList.appendChild(courseSection);
        }
    })
}