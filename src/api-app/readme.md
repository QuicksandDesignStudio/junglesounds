# Setup
- Setup virtual env `python3 -m junglesounds_venv`
- Activate `source junglesounds_venv/bin/activate`
- Install `pip install -r requirements`

# Setup db
- `python3 manage.py db upgrate`


# Start 
- Start `python3 manage.py run`


# Dev 
- In dev all the app specific data will be in data folder. In production it will be outside the project path
- data/dev.db is the database
- data/sample_audio is the sample audio folder - in prod it will be S3
- data/predict_audio is the audio folder which users have sent for prediction. This is not done yet



# API

## User

We have not added an API to this yet. PLease add to the DB directly. As of now its not used for anything special. There are already two users 
```
1- thejeshgn
2- romit
```

## Category
### Add category
POST <base_url>/categories

send

category=Elephant
slug=elephant



## Sample


## Classification


## Prediction