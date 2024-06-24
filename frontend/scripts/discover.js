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

function displayError(errorMessage) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<p>Error: ${errorMessage}</p>`;
}


// function handleSearch() {
//     const userInput = document.getElementById('searchInput').value;
//     const bodypart = document.getElementById('bodypartSelect').value;
//     const equipment = document.getElementById('equipmentSelect').value;

//     fetch('https://fitnessaicoach.azurewebsites.net/search_exercises', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ user_input: userInput, bodypart: bodypart, equipment: equipment })
//     })
//     .then(response => response.json())
//     .then(data => displayResults(data))
//     .catch(error => console.error('Error:', error));
// }

// function displayResults(data) {
//     const resultsDiv = document.getElementById('results');
//     resultsDiv.innerHTML = '';

//     if (data.error) {
//         resultsDiv.textContent = data.error;
//     } else {
//         data.forEach(exercise => {
//             const exerciseElement = document.createElement('div');
//             exerciseElement.innerHTML = `
//                 <p><strong>${exercise.name}</strong></p>
//                 <img src="${exercise.gifUrl}" alt="${exercise.name}">
//                 <p>Equipment: ${exercise.equipment}</p>
//                 <p>Body Part: ${exercise.bodyPart}</p>
//                 <p>Target: ${exercise.target}</p>
//             `;
//             resultsDiv.appendChild(exerciseElement);
//         });
//     }
// }