# Project Title
![image](https://github.com/VU-Applied-Programming-for-AI-2024/Group-15/assets/156012070/cc0030de-bc76-4e36-9216-1a8cd9b9c43c)

## Brief description of the project
myFitnessAI Coach is an AI-powered platform designed to create personalized fitness schedules based on users' available time, equipment, and desired difficulty level. We will use an API while accessing user information stored in a MongoDB database, the platform delivers tailored workout plans to help users achieve their fitness goals. The application leverages Azure for deployment, ensuring scalability and reliability. We implemented a CI/CD workflow pipeline for a continuous real-time deployment. App's key features will include an intuitive search interface for discovering exercises, dynamic exercise scheduling, and seamless user data managemen, along with data visualization regarding exercise details. 
## Frontend mockup
![mockup](https://github.com/VU-Applied-Programming-for-AI-2024/Group-15/blob/master/frontend/images/New%20Wireframe%201.png) 
## Team members
#### Felice Faruolo 
#### Timothé Van Damme
## Installation details
Our website is accessible via url link (It was deployed on azure web static app): https://gentle-bay-09953a810.5.azurestaticapps.net/
The backend server is accesible via this li k: https://fitnessaicoach.azurewebsites.net/

For running the application on a local machine the steps are the following: 

1. Install the repository on local;
2. go to the project directory;
3. create a virtual environment;
4. install the dependencies (pip install -r requirements.txt);
5. Set up a .env file with all the keys;
6. go to the backend folder directory and run on terminal "flask run";
7. for running at the same time the frontend, open another terminal and run "python -m http.server", then go on a browser and type in the search bar:"http:localhost:8000". if the port is different, you can specify the port by running:"python -m http.server 8000";


If you want to run and test the servers locally, you need to: 
- Download the github repository
- Open it in your code editor
- Run the backend server by opening your terminal and navigate to the backend folder by doing cd backend. Then, you can do Flask run which will give you your localhost backend url. Keep it, it is important later in the process.
- Open the file you want to test, or index.py if you want to see the landing page.
- For every file in the frontend, you need to adjust the imports, deleting the ../ in front of all the import links (CSS and JavaScript)
- Then, with your code editor, utilize an extension such as live server to visualize your page live. If you want, you should also be able to see the files just from clicking on them. Here again, open index.py if you want to see the main page, or open another file if you want to see that one specifically.
- Once that is done, you should have a url: that is the frontend url.
- Then, you need go modify the JavaScript links. To do so, you have to replace every link that starts with azure-static with your frontend url, and every link starting with myfitnessai with your backend url
- If you have followed those steps correctly, you should have similar experience than on the regular website (which you can access by following the link on top of the readme)

In order to run and test the functionality of the display_exercises file, you need to get a json file that follows this type of architecture:



{
	"_id" : ObjectId("667d9a80f07ca119710ce733"),
	"schedule" : {
		"Workout_Schedule" : {
			"Wednesday" : [
				{
					"Muscle_Group" : "Back",
					"Exercises" : [
     
						{
      
							"Exercise" : "Deadlifts",
							"Sets" : 3,
							"Reps" : 12
						},
						{
							"Exercise" : "Lat Pulldown",
							"Sets" : 3,
							"Reps" : 12
						},
						{
							"Exercise" : "Seated Cable Rows",
							"Sets" : 3,
							"Reps" : 12
						}
					]
				},
				{
					"Muscle_Group" : "Chest",
					"Exercises" : [
						{
							"Exercise" : "Bench Press",
							"Sets" : 3,
							"Reps" : 12
						},
						{
							"Exercise" : "Incline Dumbbell Press",
							"Sets" : 3,
							"Reps" : 12
						},
						{
							"Exercise" : "Chest Fly",
							"Sets" : 3,
							"Reps" : 12
						}
					]
				}
			],
			"Thursday" : [
				{
					"Muscle_Group" : "Legs",
					"Exercises" : [
						{
							"Exercise" : "Squats",
							"Sets" : 3,
							"Reps" : 12
						},
						{
							"Exercise" : "Leg Press",
							"Sets" : 3,
							"Reps" : 12
						},
						{
							"Exercise" : "Lunges",
							"Sets" : 3,
							"Reps" : 12
						}
					]
				},
				{
					"Muscle_Group" : "Arms",
					"Exercises" : [
						{
							"Exercise" : "Bicep Curls",
							"Sets" : 3,
							"Reps" : 12
						},
						{
							"Exercise" : "Tricep Dips",
							"Sets" : 3,
							"Reps" : 12
						},
						{
							"Exercise" : "Hammer Curls",
							"Sets" : 3,
							"Reps" : 12
						}
					]
				}
			]
		}
	}
}



Then, you need to modify the current display_exercises to make it accept a Json file from your localhost instead of the backend server, the first method needs to be changed in this way:




document.addEventListener("DOMContentLoaded", function () {
    let schedule = null;
    let editMode = false;
    let days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    fetch("./scripts/mock_schedule.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            schedule = data.schedule.Workout_Schedule;
            console.log(schedule)
            displaySchedule();
        })
        .catch(error => {
            console.error('Error fetching mock schedule:', error);
        });
    function displaySchedule() {
        days.forEach(day => {
            displayExercises(day);
        });
    }
    function displayExercises(day) {
        const dayExercisesContainer = document.getElementById(`${day}-exercises`);
        if (dayExercisesContainer) {
            dayExercisesContainer.innerHTML = "";
            if (schedule && schedule.hasOwnProperty(day) && schedule[day].length > 0) {
                schedule[day].forEach((group, groupIndex) => {
                    group.Exercises.forEach((exercise, exerciseIndex) => {
                        const exerciseWrapper = document.createElement("div");
                        exerciseWrapper.classList.add("exercise-wrapper");

...

Then the schedule on the Json file will be displayed.

Note that the other links in that file and the other files it's using need to be updated in order to fit the links of the local machine like explained above.

## Architecture
![image](https://github.com/VU-Applied-Programming-for-AI-2024/Group-15/assets/156012070/4bdc002a-67b3-4541-bfed-74f537f3df2a)

