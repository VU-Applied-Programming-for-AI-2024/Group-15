// Function to check modal context
function checkModalContext() {
    // Check if the page is loaded within an iframe and the parent is the modal
    if (window.self !== window.top && window.parent.document.getElementById('discoverModal')) {
        return true;
    }
    return false;
}

// Function to add the "Add to Schedule" button
function addScheduleButton(exerciseElement, exercise) {
    var buttonHtml = '<button class="btn btn-primary add-to-schedule-btn">Add to Schedule</button>';
    exerciseElement.innerHTML += buttonHtml;

    // Attach click event listener to the button
    const addToScheduleBtn = exerciseElement.querySelector('.add-to-schedule-btn');
    addToScheduleBtn.addEventListener('click', function() {
        const clickedExerciseName = exercise.name;
        localStorage.setItem('clickedExercise', JSON.stringify({ name: clickedExerciseName }));
        console.log(clickedExerciseName)
       
    });
}

// Function to fetch data and display results
function fetchAndDisplayResults() {
    const userInput = document.getElementById('searchInput').value;
    const bodypart = document.getElementById('bodypartSelect').value;
    const equipment = document.getElementById('equipmentSelect').value;

    const url = new URL('https://fitnessaicoach.azurewebsites.net/search_exercises');
    url.searchParams.append('user_input', userInput);
    url.searchParams.append('bodypart', bodypart);
    url.searchParams.append('equipment', equipment);

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';

        if (data.error) {
            resultsDiv.textContent = data.error;
        } else {
            data.forEach(exercise => {
                const exerciseElement = document.createElement('div');
                exerciseElement.classList.add('exercise');

                exerciseElement.innerHTML = `
                    <p><strong>${exercise.name}</strong></p>
                    <img src="${exercise.gifUrl}" alt="${exercise.name}">
                    <p>Equipment: ${exercise.equipment}</p>
                    <p>Body Part: ${exercise.bodyPart}</p>
                    <p>Target: ${exercise.target}</p>
                `;

                // Add "Add to Schedule" button if within modal
                if (checkModalContext()) {
                    addScheduleButton(exerciseElement, exercise);
                }

                resultsDiv.appendChild(exerciseElement);
            });
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        // Display error message in resultsDiv
        const resultsDiv = document.getElementById('results');
        resultsDiv.textContent = 'Error fetching data: ' + error.message;
    });
}

// Automatically fetch and display results when the page loads
document.addEventListener('DOMContentLoaded', function() {
    fetchAndDisplayResults();
});
