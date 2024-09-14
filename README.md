# KU Polls 
![Unit Tests](../../actions/workflows/ku_polls.yml/badge.svg)
<br>
An application to conduct online polls and surveys based on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), 
with additional features.<br>
This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).
<br><br>


## Application UI
![application_ui](application_ui.png)<br><br>


## Installation
See the installation [here](Installation.md)<br><br>

## Running the Application
1. Set up the Environment <br>
```
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
```
2. Run migrations<br>
```
python manage.py migrate
```
3. Load data
```
python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```
4. Run the django development server <br>
```
python manage.py runserver
```
<br>

## Demo User Account
| Username | Password  | 
|:--------:|:---------:|
|  demo1   | Hackme11  |  
|  demo2   | Hackme22  |  
|  demo3   | Hackme33  |  
<br>

## Documents
All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20and%20Scope)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)
- [Domain Model](../../wiki/Domain%20Model)

## Iteration Plan
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)
- [Iteration 2 Plan](../../wiki/Iteration%202%20Plan)
- [Iteration 3 Plan](../../wiki/Iteration%203%20Plan)
- [Iteration 4 Plan](../../wiki/Iteration%204%20Plan)
