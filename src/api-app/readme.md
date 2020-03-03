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

- POST <base_url>/categories

Parameters

- category=Elephant
- slug=elephant

### Get all categories

- GET <base_url>/categories


### Get a single category

- GET <base_url>/category/<category_id>


## Sample

### Add Sample

- POST <base_url>/samples

Parameters

- sample_audio=Multipart audio file


### Get all Samples

- GET <base_url>/samples

Parameters

- no_of_reviews = how many classification reviews this sample has had. If you want to classifiy the freshly uploaded one, use 0. Default is None. it gets all
- limit = how many to get, default 10

And

- If the API retunes only the file name `sample_file_name`
- Actual file url will be <base_url>/download<sample_file_name>


### Get a single sample

- GET <base_url>/sample/<sample_id>



## Classification
### Add Classification

- POST <base_url>/classifications

Parameters

- sample_id=
- user_id=
- category_id=
- start_time=
- end_time=


### Get all Classification

- GET <base_url>/classifications

- Get the first 10 samples


### Get a single sample

- GET <base_url>/classification/<classification_id>



## Prediction
- Yet to be done