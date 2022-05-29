// Obtain Saber 11 grades from inputs
const mathInput = document.getElementById("math-grade");
const naturalInput = document.getElementById("natural-grade");
const socialInput = document.getElementById("social-grade");

mathInput.addEventListener('change', (event) => {
    validateGrade(mathInput);
});

naturalInput.addEventListener('change', (event) => {
    validateGrade(naturalInput);
});

socialInput.addEventListener('change', (event) => {
    validateGrade(socialInput);
});

/**
 * Upload Saber 11 grades (button pressed event)
 */
function uploadGrades_pressed() {

    // Get input values
    let mathGrade = mathInput.value;
    let naturalGrade = naturalInput.value;
    let socialGrade = socialInput.value;

    // Resultant category
    let mathCat, naturalCat, socialCat;

    // Send grades to Flask server and obtain reponse
    fetch(`/getgrades/?math=${mathGrade}&natural=${naturalGrade}&social=${socialGrade}`)
    .then(function (response) {
        return response.json();
    }).then(function (text) {
        // Parse flask message
        mathCat = text.math;
        naturalCat = text.natural;
        socialCat = text.social;

        // Mathematics category alert
        let mathDiv = document.getElementById("math-cat");
        while (mathDiv.firstChild) {
            mathDiv.removeChild(mathDiv.lastChild);
        }
        let mathCatDiv = document.createElement("div");
        mathCatDiv.classList.add('alert', getAlertClass('math', mathCat));
        mathCatDiv.appendChild(document.createTextNode(`Category ${mathCat}.`));
        mathDiv.appendChild(mathCatDiv);

        // Natural Sciences category alert
        let naturalDiv = document.getElementById("natural-cat");
        while (naturalDiv.firstChild) {
            naturalDiv.removeChild(naturalDiv.lastChild);
        }
        let naturalCatDiv = document.createElement("div");
        naturalCatDiv.classList.add('alert', getAlertClass('natural', naturalCat));
        naturalCatDiv.appendChild(document.createTextNode(`Category ${naturalCat}.`));
        naturalDiv.appendChild(naturalCatDiv);

        // Social Sciences category alert
        let socialDiv = document.getElementById("social-cat");
        while (socialDiv.firstChild) {
            socialDiv.removeChild(socialDiv.lastChild);
        }
        let socialCatDiv = document.createElement("div");
        socialCatDiv.classList.add('alert', getAlertClass('social', socialCat));
        socialCatDiv.appendChild(document.createTextNode(`Category ${socialCat}.`));
        socialDiv.appendChild(socialCatDiv);

        updateChoices();
        updateInference();

        console.log(text);
    })

    // Enable user preferences button
    document.getElementById("btn-preferences").classList.remove('disabled');
    // Diable the grades button itself
    document.getElementById('btn-grades').classList.add('disabled');

    // Once submitted clear input fields
    cleanForm();
}

/**
 * Validate input grade value: integer number between 0 and 100
 * @param inputField - Input document element
 */
function validateGrade(inputField) {

    let gradeValue = inputField.value;

    if (gradeValue < 0 || gradeValue > 100 || isNaN(gradeValue)) {
        // Case invalid
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
    } else {
        // Case valid
        inputField.classList.add('is-valid');
        inputField.classList.remove('is-invalid');
    }

    // Enable upload grades button only when all fields are valid
    if (mathInput.classList.contains('is-invalid') ||
        naturalInput.classList.contains('is-invalid') ||
        naturalInput.classList.contains('is-invalid')) {
        // Diable the grades button
        document.getElementById('btn-grades').classList.add('disabled');
    } else {
        // Enable the grades button
        document.getElementById('btn-grades').classList.remove('disabled');
    }
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

    updateChoices();
    updateInference();

    // Diable the preferences button itself
    document.getElementById('btn-preferences').classList.add('disabled');
}

function resetBtn_pressed() {
    // Enable grades button
    document.getElementById("btn-grades").classList.remove('disabled');
    // Disable preferences button
    document.getElementById("btn-preferences").classList.add('disabled');

    cleanProject();
}

/**
 * Get alert class (box color) by subject and category
 * @param {String} subject - Could be 'math', 'natural' or 'social'
 * @param {String} category - Subject category to get alert class
 * @return {String} Alert class 
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
 * Update career choices
 */
function updateChoices() {
    // Get choices from Flask server
    fetch("/choice")
    .then(function (response) {
        return response.json();
    }).then(function (text) {
        // Update humanities choice
        let humanitiesItem = document.getElementById('choose-humanities');
        if (text.humanities == 0) {
            humanitiesItem.classList.add('disabled');
        } else if (text.humanities == 2) {
            humanitiesItem.classList.add('active');
            buildConclusion("humanities");
        } else {
            humanitiesItem.classList.remove('disabled', 'active');
        }

        // Update engineering choice
        let engineeringItem = document.getElementById('choose-engineering');
        if (text.engineering == 0) {
            engineeringItem.classList.add('disabled');
        } else if (text.engineering == 2) {
            engineeringItem.classList.add('active');
            buildConclusion("engineering");
        } else {
            engineeringItem.classList.remove('disabled', 'active');
        }

        // Update science choice
        let scienceItem = document.getElementById('choose-science');
        if (text.science == 0) {
            scienceItem.classList.add('disabled');
        } else if (text.science == 2) {
            scienceItem.classList.add('active');
            buildConclusion("science");
        } else {
            scienceItem.classList.remove('disabled', 'active');
        }

        // Update health choice
        let healthItem = document.getElementById('choose-health');
        if (text.health == 0) {
            healthItem.classList.add('disabled');
        } else if (text.health == 2) {
            healthItem.classList.add('active');
            buildConclusion("health");
        } else {
            healthItem.classList.remove('disabled', 'active');
        }
    })
}

/**
 * Build conclusions section
 * @param {String} profession - Profession to get conclusion message
 */
function buildConclusion(profession) {
    let conclusionSec = document.getElementById("conclusion");
    let message = document.createElement("p");
    message.classList.add("lead", "pt-3");
    let text = "";

    if (profession == 'humanities') {
        text = `You should choose Humanities! It would be great for you. 
        At Universidad El Bosque you will find a varied offer within the Ciencias Sociales program. 
        You can find more information <a href="https://www.unbosque.edu.co/carreras-universitarias">here</a>.`;
    } else if (profession == 'engineering') {
        text = `You should choose Engineering! It would be great for you. 
        At Universidad El Bosque you will find a varied offer within the Ingenierías y Administración program. 
        You can find more information <a href="https://www.unbosque.edu.co/carreras-universitarias">here</a>.`;
    } else if (profession == 'science') {
        text = `You should choose Science! It would be great for you. 
        At Universidad El Bosque you will find a varied offer within the Ciencias Naturales program. 
        You can find more information <a href="https://www.unbosque.edu.co/carreras-universitarias">here</a>.`;
    } else if (profession == 'health') {
        text = `You should choose Health! It would be great for you. 
        At Universidad El Bosque you will find a varied offer within the Ciencias de la Salud program. 
        You can find more information <a href="https://www.unbosque.edu.co/carreras-universitarias">here</a>.`;
    }

    message.innerHTML = text;
    conclusionSec.appendChild(message);
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

        // Clean previous inferences
        removeChilds(inferenceUl);

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

/**
 * Reset the page on load and when reset button is pressed
 */
function cleanProject() {
    // Clean Saber 11 input fields
    cleanForm();

    // Clean grades categories alert
    removeChilds(document.getElementById("math-cat"));
    removeChilds(document.getElementById("natural-cat"));
    removeChilds(document.getElementById("social-cat"));

    // Clean preferences checkboxes
    /*
    document.getElementById("pref-humanities").checked = false;
    document.getElementById("pref-engineering").checked = false;
    document.getElementById("pref-sciences").checked = false;
    document.getElementById("pref-health").checked = false;
    */

    // Clean choices menu
    document.getElementById('choose-humanities').classList.remove('disabled', 'active');
    document.getElementById('choose-engineering').classList.remove('disabled', 'active');
    document.getElementById('choose-science').classList.remove('disabled', 'active');
    document.getElementById('choose-health').classList.remove('disabled', 'active');

    // Clean conclusions section
    removeChilds(document.getElementById("conclusion"));

    // Remove old inferences
    let inferenceUl = document.getElementById("reason-list");

    while (inferenceUl.firstChild) {
        inferenceUl.removeChild(inferenceUl.lastChild);
    }

    // Initialize knowledge engine
    fetch("/initialize")
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log(text);
    })
}

/**
 * Clean Saber 11 input fields
 */
function cleanForm() {
    mathInput.classList.remove("is-valid");
    mathInput.classList.remove("is-invalid");
    naturalInput.classList.remove("is-valid");
    naturalInput.classList.remove("is-invalid");
    socialInput.classList.remove("is-valid");
    socialInput.classList.remove("is-invalid");
}

/**
 * Remove all docuement element childs
 * @param docElement - Document element to remove childs
 */
function removeChilds(docElement) {
    while (docElement.firstChild) {
        docElement.removeChild(docElement.lastChild);
    }
}