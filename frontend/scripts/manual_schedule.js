document.addEventListener("DOMContentLoaded", function () {
    const schedule = JSON.parse(localStorage.getItem("schedule")) || {};
    let userToken = getUserToken(); // Declare userToken outside the function scope
    console.log(userToken)
    const overlay = document.getElementById("start-overlay");

    const isOnUserTokenPage = window.location.href.includes(`manual_schedule.html?token=${userToken}`);

  
    const days = [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday",
    ];
    let editMode = false; // Track if edit mode is active
  
    function displayExercises(day) {
        const dayExercisesContainer = document.getElementById(`${day}-exercises`);
      
        if (dayExercisesContainer) {
          dayExercisesContainer.innerHTML = ""; // Clear previous content
      
          // Check if current URL matches the expected manual_schedule.html with userToken
          if (window.location.href.includes(`manual_schedule.html?token=${userToken}`)) {
            if (schedule[day] && schedule[day].length > 0) {
              schedule[day].forEach((exercise, index) => {
                const exerciseElement = document.createElement("div");
                exerciseElement.classList.add("exercise-item");
                exerciseElement.textContent = exercise.name;
      
                if (editMode) {
                  const deleteButton = document.createElement("button");
                  deleteButton.textContent = "Delete";
                  deleteButton.classList.add("btn", "btn-danger", "delete-exercise-btn");
                  deleteButton.dataset.day = day;
                  deleteButton.dataset.index = index;
      
                  const swapButton = document.createElement("button");
                  swapButton.textContent = "Swap";
                  swapButton.classList.add("btn", "btn-secondary", "swap-exercise-btn");
                  swapButton.dataset.day = day;
                  swapButton.dataset.index = index;
      
                  deleteButton.addEventListener("click", function () {
                    deleteExercise(day, index);
                  });
      
                  swapButton.addEventListener("click", function () {
                    swapExercise(day, index);
                  });
      
                  exerciseElement.appendChild(deleteButton);
                  exerciseElement.appendChild(swapButton);
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
          userToken = getUserToken(); // Update userToken if necessary
      
          // Check if already on the correct modal page
          if ((!isOnUserTokenPage) ) {
            // Redirect to the manual_schedule.html with userToken
            window.location.href = `https://fitnessaicoach.azurewebsites.net/manual_schedule.html?token=${userToken}`;
          } else {
            // Open DiscoverModal or perform other actions as needed
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
      schedule[selectedDay].push(clickedExercise);
      localStorage.setItem("schedule", JSON.stringify(schedule));
      localStorage.removeItem("clickedExercise");
  
      saveChangesToServer(); // Call saveChangesToServer function immediately
      if (window.location.href.endsWith(`manual_schedule_${userToken}.html`)) {
        // Open your modal here or perform necessary actions
        console.log("Open modal or perform actions for the correct URL");
      }
    }
  
    
  //EDIT AND STATS BUTTONS
    document.addEventListener("click", function (event) {
      const target = event.target;
  
      if (target.classList.contains("stats-btn")) {
        const day = target.dataset.day;
        console.log(`Stats button clicked for ${day}`);
      } else if (target.classList.contains("edit-btn")) {
        const day = target.dataset.day;
        console.log(`Edit button clicked for ${day}`);
        editMode = !editMode; // Toggle edit mode
        days.forEach(displayExercises); // Refresh the exercise list with edit buttons
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
      schedule[day].splice(index, 1); // Remove the exercise
      localStorage.setItem("schedule", JSON.stringify(schedule));
      displayExercises(day); // Refresh the exercise list
    }
  
    function swapExercise(day, index) {
      if (index > 0) {
        [schedule[day][index], schedule[day][index - 1]] = [
          schedule[day][index - 1],
          schedule[day][index],
        ]; // Swap with the previous item
        localStorage.setItem("schedule", JSON.stringify(schedule));
        displayExercises(day); // Refresh the exercise list
      }
    }
  
    //SENDING TO BACKEND
    // function saveChangesToServer() {
    //   const userScheduleUrl = "https://fitnessaicoach.azurewebsites.net/save_schedule"; // Replace with your actual URL
  
    //   fetch(userScheduleUrl, {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({
    //       token: userToken,
    //       schedule: schedule,
    //     }),
    //   })
    //     .then((response) => {
    //       if (!response.ok) {
    //         return response.text().then((text) => {
    //           throw new Error(text);
    //         });
    //       }
    //       return response.json();
    //     })
    //     .then((data) => {
    //       console.log("Schedule saved successfully:", data);
    //       window.location.href = `manual_schedule_${userToken}.html`;
    //     })
    //     .catch((error) => {
    //       console.error("Error saving schedule:", error);
    //     });
    // }
  

    //TOKEN STUFF
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

    if (!isOnUserTokenPage) {
        overlay.style.visibility = "visible";
        overlay.style.opacity = "1";
        overlay.addEventListener("click", () => {
          window.location.href = `https://fitnessaicoach.azurewebsites.net/manual_schedule.html?token=${userToken}`;
        });
      } else {
        overlay.style.visibility = "hidden";
        overlay.style.opacity = "0";
      }
  });
  

