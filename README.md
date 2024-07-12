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

Running the application on a local machine;

 1. Clone the repository and navigate to the project directory:
   - Run the following command in your terminal:
`git clone https://github.com/VU-Applied-Programming-for-AI-2024/Group-15.git`
   - Change to the project directory with: `cd Group-15`
     
 2. Create and activate a virtual environment using conda:
   - Create the environment with: `conda create --name myfitnessai_env python=3.8`
   - Activate the environment with: `conda activate myfitnessai_env`
     
 3. Install the dependencies listed in the requirements.txt file:
   - Run the command: `pip install -r requirements.txt`
     
 4. Set up a `.env` file in the `backend` directory with all the necessary environment variables.
    
 6. Navigate to the backend folder directory and run the Flask server:
   - Change to the backend directory with: `cd backend`
   - Start the server with: `flask run`
   - This will start the backend server at `http://127.0.0.1:5000`
     
 6. Open a new terminal window, navigate to the frontend directory, and start a local HTTP server:
   - Change to the frontend directory with: `cd frontend`
     
Running the application on a local machine
   - Start the server with: `python -m http.server`
   - This will start the frontend server at `http://localhost:8000

## Architecture
![image](https://github.com/VU-Applied-Programming-for-AI-2024/Group-15/assets/156012070/4bdc002a-67b3-4541-bfed-74f537f3df2a)

