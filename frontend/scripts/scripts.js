document.addEventListener('DOMContentLoaded', function() {
  // Function to activate days of the week
  const days = document.querySelectorAll('.day');
  const createScheduleBtn = document.getElementById('create-schedule-btn');
  const muscleErrorText = document.getElementById('muscle-error');

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
    const muscles = document.querySelectorAll('.muscle-item');
    const selectedDays = Array.from(days).some(day => day.classList.contains('active'));

    const ageFilled = age !== '';
    const genderSelected = gender !== null;
    const weightFilled = weight !== '';
    const musclesSelected = muscles.length > 0;

    if (ageFilled && genderSelected && weightFilled && musclesSelected && selectedDays) {
      createScheduleBtn.disabled = false;
      muscleErrorText.style.display = 'none'; // Hide error text if all conditions are met
    } else {
      createScheduleBtn.disabled = true;
      muscleErrorText.style.display = musclesSelected ? 'none' : 'block'; // Show error text if no muscle is selected
    }
  }

  // Attach event listeners to inputs
  document.querySelector('.age-input').addEventListener('input', validateForm);
  document.querySelectorAll('input[name="gender"]').forEach(genderInput => {
    genderInput.addEventListener('change', validateForm);
  });
  document.querySelector('.weight-input').addEventListener('input', validateForm);

  // Code for AI Schedule Modal
  const addMuscleBtn = document.getElementById('add-muscle-btn');
  const modal = document.getElementById('muscleModal');
  const closeModal = document.getElementsByClassName('close')[0];
  const saveMuscleBtn = document.getElementById('save-muscle-btn');
  const muscleSelect = document.getElementById('muscle-select');
  const muscleList = document.getElementById('muscle-list');

  const muscles = [
    'back', 'cardio', 'chest', 'lower arms', 'lower legs', 'neck', 'shoulder', 'upper arms', 'upper legs', 'waist'
  ];

  muscles.forEach(muscle => {
    const option = document.createElement('option');
    option.value = muscle;
    option.textContent = muscle;
    muscleSelect.appendChild(option);
  });

  addMuscleBtn.addEventListener('click', function () {
    modal.style.display = 'block';
  });

  closeModal.addEventListener('click', function () {
    modal.style.display = 'none';
  });

  window.addEventListener('click', function (event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });

  saveMuscleBtn.addEventListener('click', function () {
    const selectedMuscle = muscleSelect.value;

    if (selectedMuscle) {
      const muscleItem = document.createElement('div');
      muscleItem.className = 'muscle-item';
      muscleItem.textContent = selectedMuscle;
      muscleList.appendChild(muscleItem);

      const hiddenInput = document.createElement('input');
      hiddenInput.type = 'hidden';
      hiddenInput.name = 'target_muscles';
      hiddenInput.value = selectedMuscle;
      muscleList.appendChild(hiddenInput);

      const options = muscleSelect.querySelectorAll('option');
      options.forEach(option => {
        if (option.value === selectedMuscle) {
          option.remove();
        }
      });

      modal.style.display = 'none';
      validateForm();
    }
  });

  // Form submission to communicate data to Flask backend
  document.getElementById('user-info-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const age = document.querySelector('.age-input').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const weight = document.querySelector('.weight-input').value;
    const muscles = Array.from(document.querySelectorAll('input[name="target_muscles"]')).map(input => input.value);
    const goal = document.getElementById('goal').value;
    const selectedDays = Array.from(days).filter(day => day.classList.contains('active')).map(day => day.getAttribute('data-day'));

    const data = { age, gender, weight, muscles, goal, days: selectedDays };

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
        localStorage.setItem('scheduleId', scheduleId); // Store the schedule ID for future use
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

  validateForm(); // Initial validation to disable the button if necessary
});