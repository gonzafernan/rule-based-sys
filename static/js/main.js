// Saber 11 grades
var mathGrade = 0, naturalGrade = 0, socialGrade = 0;

// Upload Saber 11 grades
function uploadGrades_pressed() {
    mathGrade = document.getElementById("math-grade").value;
    naturalGrade = document.getElementById("natural-grade").value;
    socialGrade = document.getElementById("social-grade").value;

    // Send that to Flask server
    fetch(`/getgrades/?math=${mathGrade}&natural=${naturalGrade}&social=${socialGrade}`).then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log(text); 
    })

    document.getElementById("btn-preferences").classList.remove('disabled');
}

function uploadPreferences_pressed() {
    let prefHumanities = document.getElementById("pref-humanities").checked;
    let prefEngineering = document.getElementById("pref-engineering").checked;
    let prefSciences = document.getElementById("pref-sciences").checked;
    let prefHealth = document.getElementById("pref-health").checked;
    console.log(prefHumanities);
}


fetch('/test')
.then(function (response) {
    return response.json();
}).then(function (text) {
    console.log('GET response:');
    console.log(text.greeting); 
});