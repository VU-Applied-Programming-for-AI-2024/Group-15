function handleSearch() {
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
    .then(data => displayResults(data))
    .catch(error => {
        console.error('Error:', error);
        displayError(error.message);
    });
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (data.error) {
        resultsDiv.textContent = data.error;
    } else {
        data.forEach(exercise => {
            const exerciseElement = document.createElement('div');
            exerciseElement.classList.add('exercise')
            exerciseElement.innerHTML = `
                <p><strong>${exercise.name}</strong></p>
                <img src="${exercise.gifUrl}" alt="${exercise.name}">
                <p>Equipment: ${exercise.equipment}</p>
                <p>Body Part: ${exercise.bodyPart}</p>
                <p>Target: ${exercise.target}</p>
                <button class="btn btn-primary add-to-schedule-btn">Add to Schedule</button>
            `;
            resultsDiv.appendChild(exerciseElement);

           
            // Add event listener to the "Add to Schedule" button
            const addToScheduleBtn = exerciseElement.querySelector('.add-to-schedule-btn');
            addToScheduleBtn.addEventListener('click', function() {
                addToSchedule(exercise);
            });
        });
    }

    function addToSchedule(exercise) {
        // Get the existing schedule from localStorage or initialize an empty object
        const schedule = JSON.parse(localStorage.getItem('schedule')) || {};
    
        // Assuming you have a way to dynamically select the day (for demonstration, let's use Monday)
        const selectedDay = 'Monday'; // Modify this as per your application logic
    
        // Push the exercise object to the schedule for the selected day
        if (!schedule[selectedDay]) {
            schedule[selectedDay] = [];
        }
        schedule[selectedDay].push(exercise);
    
        // Store the updated schedule back in localStorage
        localStorage.setItem('schedule', JSON.stringify(schedule));
    
        // Update the UI to reflect the new schedule (if necessary)
        updateScheduleUI(schedule);
    
        // Optionally, provide user feedback that the exercise was added to the schedule
        alert(`${exercise.name} added to ${selectedDay}'s schedule!`);
    }
    
function displayError(errorMessage) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<p>Error: ${errorMessage}</p>`;
}
}