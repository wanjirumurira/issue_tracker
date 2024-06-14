# Issue Tracker

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS3-563D7C?style=for-the-badge&logo=css3&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)



An issue tracker is a software tool that helps individuals and teams track and manage issues or bugs that arise during software development or other projects. The purpose of this issue tracker is to provide a centralized location for recording, tracking, and resolving issues, which can help ensure that they are addressed in a timely and efficient manner.




## Installation

Clone This Repository or Download on your local machine

git clone https://github.com/wanjirumurira/issuetracker.git

Activate Your Virtual Enviornment Then Type python manage.py migrate

Install Requirements.txt file
```
pip install -r requirements.txt
```
Now Run Your Server
```
python manage.py runserver
```
Visit Following Url in Any Browser

```
http://127.0.0.1:8000/
```
# Contenarization:

To run this app as a container, run the command

```
docker-compose up --build
```
View the images 
```
docker image
```
view the running containers
```
docker ps
```

To access the Contenarized application, 

If running on local host:

```
http://localhost:8080/
```
If running on a Virtual Machine:

```
http://[IP OF YOUR VM]:8080/
```

# Contribution
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.Report bugs: If you encounter any bugs, please let us know. Open up an issue and let us know the problem.

2.Contribute code: If you are a developer and want to contribute, follow the instructions below to get started!

3.Suggestions: If you don't want to code but have some awesome ideas, open up an issue explaining some updates or imporvements you would like to see!

4.Documentation: If you see the need for some additional documentation, feel free to add some!
