document.addEventListener('DOMContentLoaded', function() {
    const scheduleContainer = document.getElementById('schedule-container');
    const popup = document.getElementById('popup');
    const closePopup = document.getElementById('close-popup');

    closePopup.addEventListener('click', () => {
        popup.style.display = 'none';
    });

    const urlParams = new URLSearchParams(window.location.search);
    const scheduleId = urlParams.get('scheduleId');

    fetch(`http://127.0.0.1:5000/get-schedule/${scheduleId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displaySchedule(data.schedule);
                popup.style.display = 'block';
            } else {
                scheduleContainer.innerHTML = `<p>Error loading schedule: ${data.message}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            scheduleContainer.innerHTML = `<p>Error loading schedule.</p>`;
        });

    function displaySchedule(schedule) {
        for (const [day, workouts] of Object.entries(schedule.Workout_Schedule)) {
            const dayCard = document.createElement('div');
            dayCard.classList.add('day-card');
            dayCard.innerHTML = `<h2>${day}</h2>`;

            workouts.forEach(workout => {
                const muscleGroupCard = document.createElement('div');
                muscleGroupCard.classList.add('muscle-group-card');
                muscleGroupCard.innerHTML = `<h3>${workout.Muscle_Group}</h3>`;

                workout.Exercises.forEach(exercise => {
                    const exerciseCard = document.createElement('div');
                    exerciseCard.classList.add('exercise-card');
                    exerciseCard.innerHTML = `
                        <p><strong>Exercise:</strong> ${exercise.Exercise}</p>
                        <p><strong>Sets:</strong> ${exercise.Sets}</p>
                        <p><strong>Reps:</strong> ${exercise.Reps}</p>
                        <button class="favorite-btn">Add to Favorites</button>
                    `;
                    exerciseCard.querySelector('.favorite-btn').addEventListener('click', () => {
                        addToFavorites(exercise);
                    });
                    muscleGroupCard.appendChild(exerciseCard);
                });

                dayCard.appendChild(muscleGroupCard);
            });

            scheduleContainer.appendChild(dayCard);
        }
    }

    function addToFavorites(exercise) {
        let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
        favorites.push(exercise);
        localStorage.setItem('favorites', JSON.stringify(favorites));
        alert(`${exercise.Exercise} added to favorites!`);
    }
});