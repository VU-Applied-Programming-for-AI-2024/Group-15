document.addEventListener("DOMContentLoaded", function () {
  const schedule = JSON.parse(localStorage.getItem("schedule")) || {};
  let userToken = getUserToken();
  console.log(userToken);
  const overlay = document.getElementById("start-overlay");

  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  let editMode = false;

  function displayExercises(day) {
      const dayExercisesContainer = document.getElementById(`${day}-exercises`);

      if (dayExercisesContainer) {
          dayExercisesContainer.innerHTML = ""; // Clear previous content

          if (window.location.href.includes(`manual_schedule.html?token=${userToken}`)) {
              if (schedule[day] && schedule[day].length > 0) {
                  schedule[day].forEach((exercise, index) => {
                      const exerciseElement = document.createElement("div");
                      exerciseElement.classList.add("exercise-item");
                      exerciseElement.textContent = exercise.name;

                      // Create rep x set element
                      const repSetElement = document.createElement("div");
                      repSetElement.classList.add("rep-set");
                      repSetElement.textContent = `${exercise.sets} x ${exercise.reps}` || "0 x 0";
                      exerciseElement.appendChild(repSetElement);

                      if (editMode) {
                          // If in edit mode, allow modification
                          const deleteButton = document.createElement("button");
                          deleteButton.textContent = "X";
                          deleteButton.classList.add("btn", "btn-danger", "delete-exercise-btn");
                          deleteButton.dataset.day = day;
                          deleteButton.dataset.index = index;

                          const swapButton = document.createElement("button");
                          swapButton.textContent = "🔀";
                          swapButton.classList.add("btn", "btn-secondary", "swap-exercise-btn");
                          swapButton.dataset.day = day;
                          swapButton.dataset.index = index;

                          deleteButton.addEventListener("click", function () {
                              //deleteExercise(day, index);
                          });

                          swapButton.addEventListener("click", function () {
                              //swapExercise(day, index);
                          });

                          exerciseElement.appendChild(deleteButton);
                          exerciseElement.appendChild(swapButton);

                          // Allow modifying rep x set
                          repSetElement.contentEditable = "true";
                          repSetElement.addEventListener("input", function () {
                              const [newSets, newReps] = repSetElement.textContent.split(' x ');
                              updateRepSet(day, index, newSets, newReps);
                          });
                      }

                      dayExercisesContainer.appendChild(exerciseElement);
                  });
              } else {
                  const noExerciseElement = document.createElement("div");
                  noExerciseElement.textContent = "Rest";
                  dayExercisesContainer.appendChild(noExerciseElement);
              }
          } else {
              // If not on the correct page, clear the content
              dayExercisesContainer.innerHTML = "";
          }
      } else {
          console.error(`Element with ID '${day}-exercises' not found.`);
      }
  }

  days.forEach((day) => {
      displayExercises(day);
  });

  document.querySelectorAll(".add-exercise-btn").forEach((button) => {
      button.addEventListener("click", function (event) {
          const day = event.target.dataset.day;
          localStorage.setItem("selectedDay", day);
          userToken = getUserToken();

          if (!window.location.href.endsWith(userToken)) {
              window.location.href = `https://gentle-bay-09953a810.5.azurestaticapps.net/manual_schedule.html?token=${userToken}`;
          } else {
              openDiscoverModal();
          }
      });
  });

  const clickedExercise = JSON.parse(localStorage.getItem("clickedExercise"));
  const selectedDay = localStorage.getItem("selectedDay");

  if (clickedExercise && selectedDay) {
      if (!schedule[selectedDay]) {
          schedule[selectedDay] = [];
      }
      clickedExercise.sets = 0;
      clickedExercise.reps = "0"; // Initialize reps as a string
      schedule[selectedDay].push(clickedExercise);
      localStorage.setItem("schedule", JSON.stringify(schedule));
      localStorage.removeItem("clickedExercise");

      saveChangesToServerAndReload(); // Call the function to save changes and reload
      if (window.location.href.endsWith(`manual_schedule_${userToken}.html`)) {
          console.log("Open modal or perform actions for the correct URL");
      }
  }

  document.addEventListener("click", function (event) {
      const target = event.target;

      if (target.classList.contains("stats-btn")) {
          const day = target.dataset.day;
          console.log(`Stats button clicked for ${day}`);
      } else if (target.classList.contains("edit-btn")) {
          const day = target.dataset.day;
          console.log(`Edit button clicked for ${day}`);
          editMode = !editMode;
          days.forEach(displayExercises);
      } else if (target.classList.contains("delete-exercise-btn")) {
          const day = target.dataset.day;
          const index = target.dataset.index;
          deleteExercise(day, index);
      } else if (target.classList.contains("swap-exercise-btn")) {
          const day = target.dataset.day;
          const index = parseInt(target.dataset.index, 10);
          swapExercise(day, index);
      }
  });

  function deleteExercise(day, index) {
      schedule[day].splice(index, 1);
      localStorage.setItem("schedule", JSON.stringify(schedule));
      displayExercises(day);
  }

  function swapExercise(day, index) {
      if (index > 0) {
          [schedule[day][index], schedule[day][index - 1]] = [schedule[day][index - 1], schedule[day][index]];
          localStorage.setItem("schedule", JSON.stringify(schedule));
          displayExercises(day);
      }
  }

  function updateRepSet(day, index, newSets, newReps) {
      if (schedule[day] && schedule[day][index]) {
          const sets = parseInt(newSets);
          // Reps should be stored as string
          const reps = newReps;

          // Check if sets is a valid integer
          if (!isNaN(sets)) {
              schedule[day][index].sets = sets;
          } else {
              console.error(`Invalid sets (${newSets}) input.`);
          }

          // Update reps directly as string
          schedule[day][index].reps = reps;
          localStorage.setItem("schedule", JSON.stringify(schedule));

          displayExercises(day); // Update display after modification
      }
  }

  function saveChangesToServerAndReload() {
      const userScheduleUrl = "https://fitnessaicoach.azurewebsites.net/save_schedule";

      // Map schedule to desired structure with Sets and Reps
      const mappedSchedule = {};
      Object.keys(schedule).forEach(day => {
          mappedSchedule[day] = schedule[day].map(exercise => ({
              Muscle_Group: exercise.muscleGroup,
              Exercises: [
                  {
                      Exercise: exercise.name,
                      Sets: exercise.sets,
                      Reps: exercise.reps
                  }
              ]
          }));
      });

      fetch(userScheduleUrl, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({
              email: email,
              scheduleName: scheduleName,
              schedule: {
                  Workout_Schedule: mappedSchedule
              },
          }),
      })
      .then((response) => {
          if (!response.ok) {
              return response.text().then((text) => {
                  throw new Error(text);
              });
          }
          return response.json();
      })
      .then((data) => {
          console.log("Schedule saved successfully:", data);
          window.location.reload(); // Reload the page after successful save
      })
      .catch((error) => {
          console.error("Error saving schedule:", error);
      });
  }

  function getUserToken() {
      let token = localStorage.getItem("userToken");
      if (!token || token === "null" || token === "undefined") {
          token = generateUniqueToken();
          localStorage.setItem("userToken", token);
      }
      return token;
  }

  function generateUniqueToken() {
      return "user-" + Math.random().toString(36).substr(2, 9);
  }

  overlay.addEventListener("click", () => {
      userToken = generateUniqueToken();
      localStorage.setItem("userToken", userToken);
      window.location.href = `https://gentle-bay-09953a810.5.azurestaticapps.net/manual_schedule.html?token=${userToken}`;
  });

  if (!window.location.href.endsWith(userToken)) {
      overlay.style.visibility = "visible";
      overlay.style.opacity = "1";
  } else {
      overlay.style.visibility = "hidden";
      overlay.style.opacity = "0";
  }

  const showFavoritesFormBtn = document.getElementById("show-favorites-form-btn");
  const favoritesForm = document.getElementById("favorites-form");

  showFavoritesFormBtn.addEventListener("click", () => {
      favoritesForm.style.display = "block";
  });

  const addToFavoritesBtn = document.getElementById("add-to-favorites-btn");

  addToFavoritesBtn.addEventListener("click", async function() {
      const email = document.getElementById("favorites-email").value;
      const scheduleName = document.getElementById("favorites-name").value;
      const addToFavesUrl = new URL('https://fitnessaicoach.azurewebsites.net/add_to_favorites');
      if (email && scheduleName) {
          const response = await fetch(addToFavesUrl, {
              method: 'POST',
              mode: 'no-cors',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ email, scheduleName, schedule }),
          });
          const result = await response.json();
          if (result.status === 'success') {
              alert('Schedule added to favorites successfully!');
          } else {
              alert('Failed to add schedule to favorites: ' + result.message);
          }
          document.getElementById('favorites-form').style.display = 'none';
      } else {
          alert("Please fill in both the email and schedule name.");
      }
  });

  function showStats(day) {
      const exercises = schedule[day] || [];
      if (exercises.length === 0) {
          alert("No exercises for this day.");
          return;
      }

      let totalCalories = 0;
      const muscleGroups = {};
      const setsPerMuscleGroup = {};

      exercises.forEach(exercise => {
          const reps = exercise.reps || "0"; // Ensure reps is treated as string
          const sets = exercise.sets || 0;
          const muscleGroup = exercise.muscleGroup || "Other";

          totalCalories += 0.5 * reps * sets;

          if (!muscleGroups[muscleGroup]) {
              muscleGroups[muscleGroup] = 0;
              setsPerMuscleGroup[muscleGroup] = 0;
          }

          muscleGroups[muscleGroup] += reps * sets;
          setsPerMuscleGroup[muscleGroup] += sets;
      });

      const muscleGroupLabels = Object.keys(muscleGroups);
      const muscleGroupData = muscleGroupLabels.map(group => muscleGroups[group]);
      const setsPerMuscleGroupData = muscleGroupLabels.map(group => setsPerMuscleGroup[group]);

      const statsContent = `
          <p>Total Calories Burned: ${totalCalories.toFixed(2)}</p>
          <div class="chart-container">
              <canvas id="muscleGroupChart"></canvas>
          </div>
          <div class="chart-container">
              <canvas id="setsPerMuscleGroupChart"></canvas>
          </div>
      `;

      document.getElementById('statsContent').innerHTML = statsContent;

      const ctx1 = document.getElementById('muscleGroupChart').getContext('2d');
      const ctx2 = document.getElementById('setsPerMuscleGroupChart').getContext('2d');

      new Chart(ctx1, {
          type: 'pie',
          data: {
              labels: muscleGroupLabels,
              datasets: [{
                  data: muscleGroupData,
                  backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0'],
              }]
          },
          options: {
              responsive: true,
              maintainAspectRatio: false
          }
      });

      new Chart(ctx2, {
          type: 'bar',
          data: {
              labels: muscleGroupLabels,
              datasets: [{
                  label: 'Sets per Muscle Group',
                  data: setsPerMuscleGroupData,
                  backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0'],
              }]
          },
          options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });

      const statsModal = new bootstrap.Modal(document.getElementById('statsModal'));
      statsModal.show();
  }
});
