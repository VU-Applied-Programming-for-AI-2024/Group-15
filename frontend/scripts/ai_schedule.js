document.addEventListener('DOMContentLoaded', function() {
  const days = document.querySelectorAll('.day');
  const createScheduleBtn = document.getElementById('submit-btn');

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

    if (ageFilled && genderSelected && weightFilled && goalSelected && selectedDays && timeFilled) {
      createScheduleBtn.disabled = false;
    } else {
      createScheduleBtn.disabled = true;
    }
  }

  // Event listeners for form inputs
  document.querySelector('.age-input').addEventListener('input', validateForm);
  document.querySelectorAll('input[name="gender"]').forEach(genderInput => {
    genderInput.addEventListener('change', validateForm);
  });
  document.querySelector('.weight-input').addEventListener('input', validateForm);
  document.getElementById('goal').addEventListener('change', validateForm);
  document.getElementById('available-time').addEventListener('input', validateForm);

  // Event listener for form submission
  document.getElementById('user-info-form').addEventListener('submit', function (e) {
    e.preventDefault();

    // Gather form data
    const age = parseInt(document.querySelector('.age-input').value);
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const weight = parseInt(document.querySelector('.weight-input').value);
    const goal = document.getElementById('goal').value;
    const selectedDays = Array.from(days).filter(day => day.classList.contains('active')).map(day => day.getAttribute('data-day'));
    const availableTime = parseInt(document.getElementById('available-time').value);

    const data = { age, gender, weight, goal, days: selectedDays, available_time: availableTime };

    // Send data to server
    fetch('https://fitnessaicoach.azurewebsites.net/create-schedule', { 
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
      if (result.status === 'success') {
        const scheduleId = result.schedule_id;
        localStorage.setItem('scheduleId', scheduleId); // Store scheduleId in localStorage
        const scheduleJson = JSON.stringify(result.schedule, null, 2);
        // Redirect to schedule_display.html with scheduleId in query parameter
        window.location.href = `https://gentle-bay-09953a810.5.azurestaticapps.net/schedule_display.html?scheduleId=${scheduleId}`;
      } else {
        console.error('Error creating schedule:', result.message);
        alert('An error occurred while creating the schedule. Please try again.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while creating the schedule. Please try again.');
    });
  });

  validateForm(); // Validate form initially on page load
});
