
/*Code for hamburger menu */
const hamMenu = document.querySelector(".ham-menu");
const offScreenMenu = document.querySelector(".off-screen-menu");

hamMenu.addEventListener("click", () => {
  hamMenu.classList.toggle("active");
  offScreenMenu.classList.toggle("active");
});

/* Code for AIschedule modal */
document.addEventListener("DOMContentLoaded", function () {
  const addMuscleBtn = document.getElementById("add-muscle-btn");
  const modal = document.getElementById("muscleModal");
  const closeModal = document.getElementsByClassName("close")[0];
  const saveMuscleBtn = document.getElementById("save-muscle-btn");
  const muscleSelect = document.getElementById("muscle-select");
  const muscleList = document.getElementById("muscle-list");

  const muscles = ["back",
     "cardio", 
     "chest", 
     "lower arms", 
     "lower legs",  
     "neck", 
     "shoulder", 
     "upper arms", 
     "upper legs",
    "waist"
  ];

  muscles.forEach((muscle) => {
    const option = document.createElement("option");
    option.value = muscle;
    option.textContent = muscle;
    muscleSelect.appendChild(option);
  });

  addMuscleBtn.addEventListener("click", function () {
    modal.style.display = "block";
  });

  closeModal.addEventListener("click", function () {
    modal.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  });

  saveMuscleBtn.addEventListener("click", function () {
    const selectedMuscle = muscleSelect.value;

    // Ensure a muscle is selected before proceeding
    if (selectedMuscle) {
      const muscleItem = document.createElement("div");
      muscleItem.className = "muscle-item";
      muscleItem.textContent = selectedMuscle;
      muscleList.appendChild(muscleItem);

      // Add hidden input for muscle to the form
      const hiddenInput = document.createElement('input');
      hiddenInput.type = 'hidden';
      hiddenInput.name = 'target_muscles';
      hiddenInput.value = selectedMuscle;
      muscleList.appendChild(hiddenInput);


      // Remove the selected muscle from the select options
      const options = muscleSelect.querySelectorAll("option");
      options.forEach((option) => {
        if (option.value === selectedMuscle) {
          option.remove();
        }
      });

      modal.style.display = "none";
      validateForm(); // Ensure validation is re-checked
    }
  });
});

// function to activate days of the week
document.addEventListener('DOMContentLoaded', function () {
  const days = document.querySelectorAll('.day');
  const createScheduleBtn = document.getElementById('create-schedule-btn');

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
      const muscleErrorText = document.getElementById('muscle-error');

      const selectedDays = Array.from(days).some(day => day.classList.contains('active'));
      console.log("Gender Selected:", gender !== null);
      console.log("Muscles Selected:", muscles.length > 0);
      console.log("Days Selected:", selectedDays);

      // Check if all required fields are filled
      const genderSelected = gender !== null;
      const musclesSelected = muscles.length > 0;

      if (genderSelected && musclesSelected && selectedDays) {
          createScheduleBtn.disabled = false;
      } else {
          createScheduleBtn.disabled = true;
          if (!musclesSelected) {
              muscleErrorText.style.display = "block"; // Show error text
          } else {
              muscleErrorText.style.display = "none"; // Hide error text if at least 1 muscle is selected
          }
      }
  }

  // Attach event listeners to inputs
  document.querySelector(".age-input").addEventListener("input", validateForm);
  document.querySelectorAll('input[name="gender"]').forEach(genderInput => {
      genderInput.addEventListener("change", validateForm);
  });

  document.querySelector(".weight-input").addEventListener("input", validateForm);

  // Form submission to communicate data to Flask backend
  document.getElementById('user-info-form').addEventListener('submit', function (e) {
      e.preventDefault();

      const age = document.querySelector('.age-input').value;
      const gender = document.querySelector('input[name="gender"]:checked').value;
      const weight = document.querySelector('.weight-input').value;
      const muscles = Array.from(document.querySelectorAll('input[name="target_muscles"]')).map(input => input.value);
      const goal = document.getElementById('goal').value;

      const selectedDays = [];
      days.forEach(day => {
          if (day.classList.contains('active')) {
              selectedDays.push(day.getAttribute('data-day'));
          }
      });

      const data = { age, gender, weight, muscles, goal, days: selectedDays };

      fetch('http://localhost:5000/api/create-schedule', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      })
      .then(response => response.json())
      .then(result => {
          console.log('Success:', result);
          // Redirect to the specified URL after successful submission
          const redirectUrl = document.getElementById("redirect-url").value;
          window.location.href = redirectUrl;
      })
      .catch(error => {
          console.error('Error:', error);
      });
  });

  validateForm(); // Initial validation to disable the button if necessary
});
