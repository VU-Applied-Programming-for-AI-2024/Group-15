function handleSearch() {
    const userInput = document.getElementById('searchInput').value;
    const bodypart = document.getElementById('bodypartSelect').value;
    const equipment = document.getElementById('equipmentSelect').value;

    fetch('https://fitnessaicoach.azurewebsites.net/search_exercises', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: userInput, bodypart: bodypart, equipment: equipment })
    })
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error('Error:', error));
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (data.error) {
        resultsDiv.textContent = data.error;
    } else {
        data.forEach(exercise => {
            const exerciseElement = document.createElement('div');
            exerciseElement.innerHTML = `
                <p><strong>${exercise.name}</strong></p>
                <img src="${exercise.gifUrl}" alt="${exercise.name}">
                <p>Equipment: ${exercise.equipment}</p>
                <p>Body Part: ${exercise.bodyPart}</p>
                <p>Target: ${exercise.target}</p>
            `;
            resultsDiv.appendChild(exerciseElement);
        });
    }
}