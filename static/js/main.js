/**
 * Upload Saber 11 grades (button pressed event)
 */
function uploadGrades_pressed() {

    // Obtain Saber 11 grades from inputs
    let mathGrade = document.getElementById("math-grade").value;
    let naturalGrade = document.getElementById("natural-grade").value;
    let socialGrade = document.getElementById("social-grade").value;

    // Resultant category
    let mathCat, naturalCat, socialCat;

    // If empty string complete with 0
    if (mathGrade == '') {mathGrade = 0;}
    if (naturalGrade == '') {naturalGrade = 0;}
    if (socialGrade == '') {socialGrade = 0;}

    // Send grades to Flask server and obtain reponse
    fetch(`/getgrades/?math=${mathGrade}&natural=${naturalGrade}&social=${socialGrade}`)
    .then(function (response) {
        return response.json();
    }).then(function (text) {
        mathCat = text.math;
        naturalCat = text.natural;
        socialCat = text.social;

        // Show categories on screen
        let catDiv = document.getElementById("div-cat");

        // Remove all alerts already on screen
        while (catDiv.firstChild) {
            catDiv.removeChild(catDiv.lastChild);
        }

        // Create div elements for each subject
        let mathCatDiv = document.createElement("div");
        let naturalCatDiv = document.createElement("div");
        let socialCatDiv = document.createElement("div");

        mathCatDiv.classList.add('alert', getAlertClass('math', mathCat));
        mathCatDiv.appendChild(document.createTextNode(`Mathematics category ${mathCat}.`));
        naturalCatDiv.classList.add('alert', getAlertClass('natural', naturalCat));
        naturalCatDiv.appendChild(document.createTextNode(`Natural Sciences category ${naturalCat}.`));
        socialCatDiv.classList.add('alert', getAlertClass('social', socialCat));
        socialCatDiv.appendChild(document.createTextNode(`Social Sciences category ${socialCat}.`));

        // Add the alerts
        catDiv.appendChild(mathCatDiv);
        catDiv.appendChild(naturalCatDiv);
        catDiv.appendChild(socialCatDiv);

        console.log(`Mathematics category: ${mathCat}, Natural Sciences category: ${naturalCat}, 
            Social Sciences category: ${socialCat}`);
    })

    // Remove old inferences
    let inferenceUl = document.getElementById("reason-list");

    while (inferenceUl.firstChild) {
        inferenceUl.removeChild(inferenceUl.lastChild);
    }

    updateInference();

    // Enable user preferences button
    document.getElementById("btn-preferences").classList.remove('disabled');
}

/**
 * Upload user carrer preferences (button pressed event)
 */
function uploadPreferences_pressed() {

    // Obtain user carrer preferences
    let prefHumanities = document.getElementById("pref-humanities").checked;
    let prefEngineering = document.getElementById("pref-engineering").checked;
    let prefSciences = document.getElementById("pref-sciences").checked;
    let prefHealth = document.getElementById("pref-health").checked;

    // Send preferences to Flask server and obtain reponse
    fetch(`/getpref/?human=${prefHumanities}&engine=${prefEngineering}&science=${prefSciences}&health=${prefHealth}`)
        .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log(text); 
    })
}

/**
 * Get alert class (box color) by subject and category
*/
function getAlertClass(subject, category) {
    if (category == 'A') {
        return 'alert-danger';
    } else if (
        (category == 'B' && subject == 'social') || (category == 'D' && subject == 'math')
        || (category == 'C' && subject == 'natural')) {
        return 'alert-success';
    } else if ((category == 'B' && subject == 'natural') || (category == 'C' && subject == 'math')) {
        return 'alert-warning';
    } else {
        return 'alert-primary';
    }
}

/**
 * Update trigguered rules' message buffer
 */
function updateInference() {
    // Send grades to Flask server and obtain reponse
    fetch("/reasonlist")
    .then(function (response) {
        return response.json();
    }).then(function (text) {

        // Get inferences section element
        let inferenceUl = document.getElementById("reason-list");

        let i = 0;
        while (text[i] != undefined) {
            let inferenceItem = document.createElement("li");
            inferenceItem.classList.add('list-group-item');
            inferenceItem.appendChild(document.createTextNode(text[i]));
            inferenceUl.appendChild(inferenceItem);

            i++;
        }
    })
}