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

# Web
 All the web is defined inside the  `controller - application.py`. All the static files for the standard web - say images and js are in static folder. All the html templates are in templates folder

 On dev the web is at http://localhost:5000/

# API

## User

We have not added an API to this yet. PLease add to the DB directly. As of now its not used for anything special. There are already two users 
```
1- thejeshgn
2- romit
```

## Category

### Add category

- POST <base_url>/api/categories

Parameters

- category=Elephant
- slug=elephant

### Get all categories

- GET <base_url>/api/categories


### Get a single category

- GET <base_url>/api/category/<category_id>


## Sample

### Add Sample

- POST <base_url>/api/samples

Parameters

- sample_audio=Multipart audio file


### Get all Samples

- GET <base_url>/api/samples

Parameters

- no_of_reviews = how many classification reviews this sample has had. If you want to classifiy the freshly uploaded one, use 0. Default is None. it gets all
- limit = how many to get, default 10

And

- If the API retunes only the file name `sample_file_name`
- Actual file url will be <base_url>/api/download<sample_file_name>


### Get a single sample

- GET <base_url>/api/sample/<sample_id>



## Classification
### Add Classification

- POST <base_url>/api/classifications

Parameters

- sample_id=
- user_id=
- category_id=
- start_time=
- end_time=


### Get all Classification

- GET <base_url>/api/classifications

- Get the first 10 samples


### Get a single sample

- GET <base_url>/api/classification/<classification_id>



## Prediction
- Yet to be done