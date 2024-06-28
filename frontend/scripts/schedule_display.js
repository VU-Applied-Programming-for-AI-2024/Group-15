document.addEventListener("DOMContentLoaded", function () {
    const scheduleId = new URLSearchParams(window.location.search).get("schedule_id");
    const email = new URLSearchParams(window.location.search).get("email");
    const scheduleName = new URLSearchParams(window.location.search).get("schedule_name");
  
    if (scheduleId || (email && scheduleName)) {
      fetchSchedule(scheduleId, email, scheduleName);
    }
  
  
    let schedule = {};
    let editMode = false;
        let days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]; // Define days here
    function fetchSchedule(scheduleId, email, scheduleName) {
      let url = `https://fitnessaicoach.azurewebsites.net/get-schedule?`;
      if (scheduleId) {
        url += `schedule_id=${scheduleId}`;
      } else if (email && scheduleName) {
        url += `email=${email}&schedule_name=${scheduleName}`;
      }
  
      fetch(url)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            schedule = data.schedule;
            localStorage.setItem("schedule", JSON.stringify(schedule));
            displaySchedule();
          } else {
            console.error("Error fetching schedule:", data.message);
          }
        })
        .catch(error => {
          console.error("Error fetching schedule:", error);
        });
    }

  function displaySchedule() {
      days.forEach(day => {
          displayExercises(day);
      });
  }
   
    function displayExercises(day) {
      const dayExercisesContainer = document.getElementById(`${day}-exercises`);
  
      if (dayExercisesContainer) {
          dayExercisesContainer.innerHTML = ""; // Clear previous content
  
          if (schedule && schedule.hasOwnProperty(day) && schedule[day].length > 0) {
              schedule[day].forEach((group, groupIndex) => {
                  group.Exercises.forEach((exercise, exerciseIndex) => {
                      const exerciseWrapper = document.createElement("div");
                      exerciseWrapper.classList.add("exercise-wrapper");
  
                      const exerciseElement = document.createElement("div");
                      exerciseElement.classList.add("exercise-item");
                      exerciseElement.textContent = exercise.Exercise;
  
                      const detailsWrapper = document.createElement("div");
                      detailsWrapper.classList.add("exercise-details");
  
                      const repSetElement = document.createElement("div");
                      repSetElement.classList.add("rep-set");
                      repSetElement.textContent = `${exercise.Sets} x ${exercise.Reps}` || "0 x 0";
  
                      detailsWrapper.appendChild(repSetElement);
  
                      const buttonsWrapper = document.createElement("div");
                      buttonsWrapper.classList.add("buttons-wrapper");
  
                      if (editMode) {
                          const deleteButton = document.createElement("button");
                          deleteButton.textContent = "X";
                          deleteButton.classList.add("btn", "btn-danger", "delete-exercise-btn");
                          deleteButton.dataset.day = day;
                          deleteButton.dataset.groupIndex = groupIndex;
                          deleteButton.dataset.exerciseIndex = exerciseIndex;
  
                          const swapButton = document.createElement("button");
                          swapButton.textContent = "🔀";
                          swapButton.classList.add("btn", "btn-secondary", "swap-exercise-btn");
                          swapButton.dataset.day = day;
                          swapButton.dataset.groupIndex = groupIndex;
                          swapButton.dataset.exerciseIndex = exerciseIndex;
  
                          deleteButton.addEventListener("click", function () {
                            console.log("bug")
                             // deleteExercise(day, groupIndex, exerciseIndex);
                          });
  
                          swapButton.addEventListener("click", function () {
                              swapExercise(day, groupIndex, exerciseIndex);
                          });
  
                          buttonsWrapper.appendChild(deleteButton);
                          buttonsWrapper.appendChild(swapButton);
  
                          // Make repSetElement editable
                          repSetElement.contentEditable = "true";
                          repSetElement.addEventListener("input", function () {
                              const [newSets, newReps] = repSetElement.textContent.split(' x ');
                              updateRepSet(day, groupIndex, exerciseIndex, newSets, newReps);
                          });
                      }
  
                      exerciseWrapper.appendChild(exerciseElement);
                      exerciseWrapper.appendChild(detailsWrapper);
                      exerciseWrapper.appendChild(buttonsWrapper);
  
                      // Add a line break after each exercise item
                      const lineBreak = document.createElement("br");
                      exerciseWrapper.appendChild(lineBreak);
  
                      dayExercisesContainer.appendChild(exerciseWrapper);
                  });
  
              });
          } else {
              const noExerciseElement = document.createElement("div");
              noExerciseElement.textContent = "Rest";
              dayExercisesContainer.appendChild(noExerciseElement);
          }
      } else {
          console.error(`Element with ID '${day}-exercises' not found.`);
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
          days.forEach(day => displayExercises(day)); // Call displayExercises for each day
      } else if (target.classList.contains("delete-exercise-btn")) {
        const day = target.dataset.day;
        const groupIndex = parseInt(target.dataset.groupIndex);
        const exerciseIndex = parseInt(target.dataset.exerciseIndex);
        console.log(day, groupIndex, "134")
        deleteExercise(day, groupIndex, exerciseIndex);
    
      } else if (target.classList.contains("swap-exercise-btn")) {
          const day = target.dataset.day;
          const groupIndex = parseInt(target.dataset.groupIndex, 10);
          const exerciseIndex = parseInt(target.dataset.exerciseIndex, 10);
          swapExercise(day, groupIndex, exerciseIndex);
      }
  });

  function deleteExercise(day, groupIndex, exerciseIndex) {
    if (schedule[day] && schedule[day][groupIndex] && schedule[day][groupIndex].Exercises) {
        schedule[day][groupIndex].Exercises.splice(exerciseIndex, 1);
        console.log(day, groupIndex, exerciseIndex )
        localStorage.setItem("schedule", JSON.stringify(schedule));
        displayExercises(day); // Refresh display after deletion
    }
}

  function swapExercise(day, groupIndex, exerciseIndex) {
      if (exerciseIndex > 0) {
          [schedule[day][groupIndex].Exercises[exerciseIndex], schedule[day][groupIndex].Exercises[exerciseIndex - 1]] =
              [schedule[day][groupIndex].Exercises[exerciseIndex - 1], schedule[day][groupIndex].Exercises[exerciseIndex]];
          localStorage.setItem("schedule", JSON.stringify(schedule));
          displayExercises(day);
      }
  }

  function updateRepSet(day, groupIndex, exerciseIndex, newSets, newReps) {
      if (schedule[day] && schedule[day][groupIndex] && schedule[day][groupIndex].Exercises[exerciseIndex]) {
          schedule[day][groupIndex].Exercises[exerciseIndex].Sets = newSets; // Update Sets and Reps
          schedule[day][groupIndex].Exercises[exerciseIndex].Reps = newReps;
          localStorage.setItem("schedule", JSON.stringify(schedule));
      }
  }

  
    function saveChangesToServer() {
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
        })
        .catch((error) => {
          console.error("Error saving schedule:", error);
        });
    }
  
    // Show the favorites form when the button is clicked
    const showFavoritesFormBtn = document.getElementById("show-favorites-form-btn");
    const favoritesForm = document.getElementById("favorites-form");
  
    showFavoritesFormBtn.addEventListener("click", () => {
      favoritesForm.style.display = "block";
    });
  
    // Handle the add to favorites form submission
    const addToFavoritesBtn = document.getElementById("add-to-favorites-btn");
  
    addToFavoritesBtn.addEventListener("click", async function() {
      const email = document.getElementById("favorites-email").value;
      const scheduleName = document.getElementById("favorites-name").value;
      const addToFavesUrl = new URL('https://fitnessaicoach.azurewebsites.net/add_to_favorites');
      if (email && scheduleName) {
        const response = await fetch(addToFavesUrl, {
          method: 'POST',
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
  });
  