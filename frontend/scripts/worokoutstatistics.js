document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const day = urlParams.get('day');
    const scheduleId = localStorage.getItem('scheduleId');

    fetch(`http://localhost:5000/api/get-schedule/${scheduleId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const schedule = data.schedule;
                const dayExercises = schedule[day];

                // Example data for charts
                const intensityData = [40, 35, 25];
                const setsData = dayExercises.map(ex => ex.sets);
                const muscleGroups = ['Chest', 'Side Delts', 'Triceps', 'Upper Chest'];

                // Update calories burned and muscles targeted
                document.getElementById('calories-burned').textContent = '536 kcal';
                const musclesList = document.getElementById('muscles-targeted');
                muscleGroups.forEach(muscle => {
                    const listItem = document.createElement('li');
                    listItem.textContent = muscle;
                    musclesList.appendChild(listItem);
                });

                // Pie Chart for Intensity
                var ctx1 = document.getElementById('intensityChart').getContext('2d');
                var intensityChart = new Chart(ctx1, {
                    type: 'pie',
                    data: {
                        labels: ['High', 'Moderate', 'Low'],
                        datasets: [{
                            data: intensityData,
                            backgroundColor: ['#ff9999', '#66b3ff', '#99ff99'],
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                    }
                });

                // Bar Chart for Sets per Muscle Group
                var ctx2 = document.getElementById('setsChart').getContext('2d');
                var setsChart = new Chart(ctx2, {
                    type: 'bar',
                    data: {
                        labels: muscleGroups,
                        datasets: [{
                            label: 'Sets',
                            data: setsData,
                            backgroundColor: ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                    }
                });
            } else {
                console.error('Error fetching schedule:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
