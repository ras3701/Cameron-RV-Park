  # Cameron RV Park

## Description

A portal to manage RV Park bookings.

# Getting Started:

### Step 1: Clone the GitHub Repository - 
```
git clone https://github.com/ras3701/Cameron-RV-Park
cd Cameron-RV-Park
```

### Step 2: Install the following dependencies:

* [Python 3.9.x](https://www.python.org/downloads/release/python-3910/)
* [Postgres 14.x](https://www.postgresql.org/download/)
* [Redis 6.x](https://redis.io/download)

To install required python modules:
```
 pip install -r requirements.txt
```

### Step 3: Setup the following Config Vars on Heroku and in your local environment, based on the values specified in Heroku
* AWS_ACCESS_KEY_ID
* AWS_BUCKET_NAME
* AWS_HOME_METADATA_KEY
* AWS_REGION_NAME
* AWS_SECRET_ACCESS_KEY
* DATABASE_URL
* ENV_HOST
* DISABLE_COLLECTSTATIC

### Step 4: Create DB in Postgres using the following command:
```
create database test_park_db;
```

### Step 5: Run database migrations using the following commands:
```
python manage.py migrate
```

### Step 6: Launching the web server

##### (a) on your local machine -
```
python manage.py runserver
```

##### (b) Deploy to Heroku:

Note: Using the following guide, to get started with Heroku - https://devcenter.heroku.com/articles/getting-started-with-python#set-up.

Run the following commands to deploy your changes -
```
heroku run python manage.py migrate
git push heroku main
```

## Other Commands:

Create admin superuser
```
 python manage.py createsuperuser
```

Whenever DB model is changed, run the following commands:
```
python manage.py makemigrations
python manage.py migrate
```

Run all unit tests:
```
python manage.py test
```

Run tests with coverage:
```
coverage run --source="." manage.py test
```

Generate test coverage report:
```
coverage report
```


## Link to web-app:
https://cameron-rv-park.herokuapp.com/


## Authors:
1. Alekhya Duba
2. Manik Taneja
3. Mudit Maheshwari
4. Rishabh Bhardwaj
5. Rohan Shah
