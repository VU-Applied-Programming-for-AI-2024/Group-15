document.addEventListener('DOMContentLoaded', function() {
    const scheduleContainer = document.getElementById('schedule');
    const saveScheduleBtn = document.getElementById('save-schedule-btn');
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const schedule = {};

    daysOfWeek.forEach(day => {
        schedule[day] = [];
        const addButton = document.querySelector(`[data-day="${day}"] .add-exercise-btn`);
        addButton.addEventListener('click', function() {
            const exerciseDiv = document.createElement('div');
            exerciseDiv.className = 'exercise';
            exerciseDiv.innerHTML = `
                <input type="text" placeholder="Exercise Name" class="exercise-name">
                <input type="number" placeholder="Sets" class="exercise-sets">
                <input type="number" placeholder="Reps" class="exercise-reps">
                <button class="btn btn-danger remove-exercise-btn">Remove</button>
            `;
            document.getElementById(`${day}-exercises`).insertBefore(exerciseDiv, addButton);
        });
    });

    scheduleContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-exercise-btn')) {
            e.target.parentElement.remove();
        } else if (e.target.classList.contains('stats-btn')) {
            const day = e.target.getAttribute('data-day');
            localStorage.setItem('currentDay', day);
            window.location.href = `workoutstatistics.html?day=${day}`;
        } else if (e.target.classList.contains('edit-btn')) {
            // Logic for editing exercises if needed
        }
    });

    saveScheduleBtn.addEventListener('click', function() {
        daysOfWeek.forEach(day => {
            schedule[day] = [];
            const exercises = document.getElementById(`${day}-exercises`).children;
            for (let exercise of exercises) {
                if (exercise.classList.contains('exercise')) {
                    const name = exercise.querySelector('.exercise-name').value;
                    const sets = exercise.querySelector('.exercise-sets').value;
                    const reps = exercise.querySelector('.exercise-reps').value;
                    if (name && sets && reps) {
                        schedule[day].push({ name, sets: parseInt(sets), reps: parseInt(reps) });
                    }
                }
            }
        });

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
});
