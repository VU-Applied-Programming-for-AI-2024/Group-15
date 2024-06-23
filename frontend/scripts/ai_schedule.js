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

  document.querySelector('.age-input').addEventListener('input', validateForm);
  document.querySelectorAll('input[name="gender"]').forEach(genderInput => {
    genderInput.addEventListener('change', validateForm);
  });
  document.querySelector('.weight-input').addEventListener('input', validateForm);
  document.getElementById('goal').addEventListener('change', validateForm);
  document.getElementById('available-time').addEventListener('input', validateForm);
  document.getElementById('user-info-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const age = document.querySelector('.age-input').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const weight = document.querySelector('.weight-input').value;
    const goal = document.getElementById('goal').value;
    const selectedDays = Array.from(days).filter(day => day.classList.contains('active')).map(day => day.getAttribute('data-day'));
    const availableTime = document.getElementById('available-time').value;

    const data = { age, gender, weight, goal, days: selectedDays, available_time: availableTime };

    fetch('https://fitnessaicoach.azurewebsites.net/api/create-schedule', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
      console.log('Success:', result);
      if (result.status === 'success') {
        const scheduleId = result.schedule_id;
        localStorage.setItem('scheduleId', scheduleId);
        const redirectUrl = document.getElementById('redirect-url').value;
        window.location.href = redirectUrl;
      } else {
        console.error('Error creating schedule:', result.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });

  validateForm();
});
