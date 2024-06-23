document.addEventListener('DOMContentLoaded', function() {
  // Function to activate days of the week
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

  // Attach event listeners to inputs
  document.querySelector('.age-input').addEventListener('input', validateForm);
  document.querySelectorAll('input[name="gender"]').forEach(genderInput => {
    genderInput.addEventListener('change', validateForm);
  });
  document.querySelector('.weight-input').addEventListener('input', validateForm);
  document.getElementById('goal').addEventListener('change', validateForm);
  document.getElementById('available-time').addEventListener('input', validateForm);

  // Form submission to communicate data to Flask backend
  document.getElementById('user-info-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const age = document.querySelector('.age-input').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const weight = document.querySelector('.weight-input').value;
    const goal = document.getElementById('goal').value;
    const selectedDays = Array.from(days).filter(day => day.classList.contains('active')).map(day => day.getAttribute('data-day'));
    const availableTime = document.getElementById('available-time').value;

    const data = { age, gender, weight, goal, days: selectedDays, available_time: availableTime };

    fetch('https://fitnessaicoach.azurewebsites.net/create-schedule', { 
      method: 'POST',
      headers: {
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
      console.log('Success:', result);
      if (result.status === 'success') {
        const scheduleId = result.schedule_id;
        const scheduleJson = JSON.stringify(result.schedule, null, 2); // Pretty-print the JSON
        localStorage.setItem('scheduleId', scheduleId); // Store the schedule ID for future use

        // Redirect to the next page with schedule_id in ID
        window.location.href = `schedule_page.component.html?scheduleId=${scheduleId}`; 
        // Display success message and schedule JSON
        const successMessage = document.createElement('div');
        successMessage.innerHTML = `<p>Schedule created successfully!</p><pre>${scheduleJson}</pre>`;
        document.body.appendChild(successMessage);
      } else {
        console.error('Error creating schedule:', result.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });

  validateForm(); // Initial validation to disable the button if necessary
});
