
/* Code for AIschedule modal */
document.addEventListener("DOMContentLoaded", function () {
  const addMuscleBtn = document.getElementById("add-muscle-btn");
  const modal = document.getElementById("muscleModal");
  const closeModal = document.getElementsByClassName("close")[0];
  const saveMuscleBtn = document.getElementById("save-muscle-btn");
  const muscleSelect = document.getElementById("muscle-select");
  const muscleList = document.getElementById("muscle-list");

  const muscles = [
    "abductors",
    "abs",
    "adductors",
    "biceps",
    "calves",
    "cardiovascular system",
    "delts",
    "forearms",
    "glutes",
    "hamstrings",
    "lats",
    "levator scapulae",
    "pectorals",
    "quads",
    "serratus anterior",
    "spine",
    "traps",
    "triceps",
    "upper back",
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

      // Remove the selected muscle from the select options
      const options = muscleSelect.querySelectorAll("option");
      options.forEach((option) => {
        if (option.value === selectedMuscle) {
          option.remove();
        }
      });

      modal.style.display = "none";
    }
  });
});

/*Code for hamburger menu */
const hamMenu = document.querySelector(".ham-menu");
const offScreenMenu = document.querySelector(".off-screen-menu");

hamMenu.addEventListener("click", () => {
  hamMenu.classList.toggle("active");
  offScreenMenu.classList.toggle("active");
});

/*Code to save the information from the ai schedule*/

// Function to save data to local storage
function saveDataToLocalStorage() {
  const ageValue = document.querySelector(".age-input").value;
  const genderValue = document.querySelector(
    'input[name="gender"]:checked'
  ).value;
  const weightValue = document.querySelector(".weight-input").value;

  localStorage.setItem("userAge", ageValue);
  localStorage.setItem("userGender", genderValue);
  localStorage.setItem("userWeight", weightValue);
}

// Function to validate form and enable button
function validateForm() {
  const age = document.querySelector(".age-input").value;
  const gender = document.querySelector('input[name="gender"]:checked');
  const weight = document.querySelector(".weight-input").value;
  const createScheduleBtn = document.getElementById("create-schedule-btn");

  if (age && gender && weight) {
    createScheduleBtn.disabled = false;
  } else {
    createScheduleBtn.disabled = true;
  }
}