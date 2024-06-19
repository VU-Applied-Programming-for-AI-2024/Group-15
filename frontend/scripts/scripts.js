
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

  const muscles = ["Legs", "chest", "back", "arms", "shoulders", "abs"];

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


// Function to validate form and enable button
function validateForm() {
  const age = document.querySelector('.age-input').value;
  const gender = document.querySelector('input[name="gender"]:checked');
  const weight = document.querySelector('.weight-input').value;
  const muscles = document.querySelectorAll('.muscle-item');
  const createScheduleBtn = document.getElementById('create-schedule-btn');
  const muscleErrorText = document.getElementById('muscle-error');

  
  console.log("Gender Selected:", gender !== null);
  
  console.log("Muscles Selected:", muscles.length > 0);

  // Check if all required fields are filled
  const genderSelected = gender !== null;
  const musclesSelected = muscles.length > 0;

  if ( genderSelected && musclesSelected) {
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

  const data = { age, gender, weight, muscles, goal };

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
  })
  .catch(error => {
    console.error('Error:', error);
  });
});