document.addEventListener('DOMContentLoaded', function() {
    const scheduleContainer = document.getElementById('schedule');
    const saveScheduleBtn = document.getElementById('save-schedule-btn');
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    let schedule = JSON.parse(localStorage.getItem('schedule')) || {};

    // Handle click on "Add Exercise" buttons within each day
    daysOfWeek.forEach(day => {
        const addButton = document.querySelector(`[data-day="${day}"] .add-exercise-btn`);
        addButton.addEventListener('click', function() {
            const exercise = {
                name: '',  // Set initial values or leave empty for user input
                sets: 0,
                reps: 0
            };
            addToSchedule(exercise, day);
        });
    });

    // Handle click events within the schedule container
    scheduleContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-exercise-btn')) {
            e.target.parentElement.remove();
            updateLocalStorage();
        } else if (e.target.classList.contains('stats-btn')) {
            const day = e.target.getAttribute('data-day');
            localStorage.setItem('currentDay', day);
            window.location.href = `workoutstatistics.html?day=${day}`;
        } else if (e.target.classList.contains('edit-btn')) {
            // Logic for editing exercises if needed
        }
    });

    // Handle click on "Save Schedule" button
    saveScheduleBtn.addEventListener('click', function() {
        updateLocalStorage();
        fetch('http://localhost:5000/api/save-schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(schedule),
        })
        .then(response => response.json())
        .then(result => {
            console.log('Success:', result);
            if (result.status === 'success') {
                const scheduleId = result.schedule_id;
                localStorage.setItem('scheduleId', scheduleId);
                // Optionally: redirect to a confirmation page or show a message
            } else {
                console.error('Error saving schedule:', result.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Update the UI based on the schedule in localStorage
    updateScheduleUI();

    // Function to add exercise to schedule and update localStorage
    function addToSchedule(exercise, day) {
        if (!schedule[day]) {
            schedule[day] = [];
        }
        schedule[day].push(exercise);
        updateLocalStorage();
        updateScheduleUI();
    }

    // Function to update localStorage with the current schedule
    function updateLocalStorage() {
        localStorage.setItem('schedule', JSON.stringify(schedule));
    }

    // Function to update the UI based on the schedule in localStorage
    function updateScheduleUI() {
        schedule = JSON.parse(localStorage.getItem('schedule')) || {};
        daysOfWeek.forEach(day => {
            const exerciseContainer = document.getElementById(`${day}-exercises`);
            if (exerciseContainer) {
                exerciseContainer.innerHTML = ''; // Clear existing exercises
                const dayExercises = schedule[day] || [];
                dayExercises.forEach((exercise, index) => {
                    const exerciseDiv = document.createElement('div');
                    exerciseDiv.className = 'exercise';
                    exerciseDiv.innerHTML = `
                        <p>${exercise.name}</p>
                        <input type="number" value="${exercise.sets}" placeholder="Sets" class="exercise-sets">
                        <input type="number" value="${exercise.reps}" placeholder="Reps" class="exercise-reps">
                        <button class="btn btn-danger remove-exercise-btn">Remove</button>
                    `;
                    exerciseContainer.appendChild(exerciseDiv);
                });
            } else {
                console.error(`Element with id "${day}-exercises" not found.`);
            }
        });
    }
});
