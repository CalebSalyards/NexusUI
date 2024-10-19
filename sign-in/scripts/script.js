const signedIn = false;
const signInButton = document.getElementById('sign-in');

async function signInCheck(signedIn) {
    if(signedIn){
        signInButton.style.display = 'none';
    } else{

    }
}

signInCheck(signedIn)