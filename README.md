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

## Architecture
![image](https://github.com/VU-Applied-Programming-for-AI-2024/Group-15/assets/156012070/4bdc002a-67b3-4541-bfed-74f537f3df2a)

