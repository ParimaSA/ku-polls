## Installation

1. Clone the git repository
```
git clone https://github.com/ParimaSA/ku-polls
```

2. Change to the repository
```
cd ku-polls
```

3. Create and activate a virtual environment
```
python -m venv env
. env/bin/activate  # use .\env\Scripts\activate if you are on MS Windows
```

4. Install the requirement packages using in this App
```
pip install -r requirements.txt
```

5. Set Values for Externalized Variables <br>
Create .env file in the root of your project by copy the file sample.env and edit the values.
```
# Example value setting in .env file

SECRET_KEY = secret-key-value-without-quotes
DEBUG = True
ALLOWED_HOSTS = localhost, 127.0.0.1, ::1, testserver
TIME_ZONE = Asia/Bangkok
```
6. Run Migration
```
python manage.py migrate
```
7. Run Test
```
python manage.py test
```
8. Install Data from Data Fixtures
```
python manage.py loaddata data/polls-v4.json  # load question and choice
python manage.py loaddata data/votes-v4.json  # load user's vote
python manage.py loaddata data/users.json  # load user information
```