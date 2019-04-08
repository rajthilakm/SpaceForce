Spaceship Power Service

The Spaceship Power Service is needed so that rebel coordinators can keep track of the energy usage of different ships. 

Getting Started

Prerequisties 
Create a python (version 3.5.) virtual environment and install packages from requirements.txt 

Example :
	pip install --upgrade -r requirements.txt

Install Docker 
Instruction to install docker is available here : https://docs.docker.com/install/linux/docker-ce/ubuntu/ 

Starting the Service 
Navigate to the sandbox folder and run the following command. 
	./sandbox up
This initializes service and starts TICK stack that contains influxDB where data persists. 

Next, navigate back to main folder containing space_app.py. Now activate your virtual enviroment. 

Once activated , use the following command to fire up the space_app.py 

	python space_app.py 

Running Tests 

Navigate to the test folder and use the following commands to run tests 

	python space_test.py 

