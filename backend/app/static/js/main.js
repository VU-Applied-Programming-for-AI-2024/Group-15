document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/body-parts')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('body-pparts-list');
            data.forEach(part => {
                const listItem = document.createElement('li');
                listItem.textContent = part;
                list.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching body parts:', error));
});
