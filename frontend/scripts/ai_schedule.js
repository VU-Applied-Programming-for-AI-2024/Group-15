document.addEventListener('DOMContentLoaded', function () {
    const days = document.querySelectorAll('.day');
    const createScheduleBtn = document.getElementById('submit-btn');
    const waitingPopup = document.getElementById('waiting-popup');

    days.forEach(day => {
        day.addEventListener('click', function () {
            day.classList.toggle('active');
            validateForm();
        });
    });

    function validateForm() {
        const age = document.querySelector('.age-input').value;
        const gender = document.querySelector('input[name="gender"]:checked');
        const weight = document.querySelector('.weight-input').value;
        const goal = document.getElementById('goal').value;
        const selectedDays = Array.from(days).some(day => day.classList.contains('active'));
        const availableTime = document.getElementById('available-time').value;

        const ageFilled = age !== '';
        const genderSelected = gender !== null;
        const weightFilled = weight !== '';
        const goalSelected = goal !== '';
        const timeFilled = availableTime !== '';

        createScheduleBtn.disabled = !(ageFilled && genderSelected && weightFilled && goalSelected && selectedDays && timeFilled);
    }

    document.querySelector('.age-input').addEventListener('input', validateForm);
    document.querySelectorAll('input[name="gender"]').forEach(genderInput => {
        genderInput.addEventListener('change', validateForm);
    });
    document.querySelector('.weight-input').addEventListener('input', validateForm);
    document.getElementById('goal').addEventListener('change', validateForm);
    document.getElementById('available-time').addEventListener('input', validateForm);

    document.getElementById('user-info-form').addEventListener('submit', function (e) {
        e.preventDefault();

        const age = parseInt(document.querySelector('.age-input').value);
        const gender = document.querySelector('input[name="gender"]:checked').value;
        const weight = parseInt(document.querySelector('.weight-input').value);
        const goal = document.getElementById('goal').value;
        const selectedDays = Array.from(days).filter(day => day.classList.contains('active')).map(day => day.getAttribute('data-day'));
        const availableTime = parseInt(document.getElementById('available-time').value);

        const data = { age, gender, weight, goal, days: selectedDays, available_time: availableTime };

        console.log('Sending data:', JSON.stringify(data));

        fetch('https://fitnessaicoach.azurewebsites.net//create-schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(result => {
            console.log('Success:', result);
            waitingPopup.style.display = 'none';
            if (result.status === 'success') {
                const scheduleId = result.schedule_id;
                const scheduleJson = JSON.stringify(result.schedule, null, 2);
                localStorage.setItem('scheduleId', scheduleId);

                window.location.href = `schedule_display.html?scheduleId=${scheduleId}`;
            } else {
                console.error('Error creating schedule:', result.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            waitingPopup.style.display = 'none';
            alert('An error occurred while creating the schedule. Please try again.' + error);
        });
    });

    validateForm();
});