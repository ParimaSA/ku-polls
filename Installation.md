## Installation
Guide on how to install this application.

### 1. Clone the git repository
```
git clone https://github.com/ParimaSA/ku-polls
```

### 2. Change to the repository
```
cd ku-polls
```

### 3. Create a virtual environment
```
python -m venv venv
```
### 4. Activate a virtual environment
**On Mac/Linux**
```
source venv/bin/activate 
``` 
**On Window**
```
.\env\Scripts\activate
```

### 5. Install the requirement packages using in this App
```
pip install -r requirements.txt
```

### 6. Set Values for Externalized Variables
Create .env file in the root of your project by copy the file sample.env, you can edit the values as you needed.<br><br>
**On Mac/Linux**
```
cp sample.env .env
```
**On Window**
```
copy sample.env .env
```
### 7. Run Migration
```
python manage.py migrate
```
### 8. Run Test
```
python manage.py test
```
### 9. Install Data from Data Fixtures
**Polls Data**
```
python manage.py loaddata data/polls-v4.json
```
**Votes Data**
```
python manage.py loaddata data/votes-v4.json
```
**User Data**
```
python manage.py loaddata data/users.json
```
**or load all datas in one line**
```
python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```